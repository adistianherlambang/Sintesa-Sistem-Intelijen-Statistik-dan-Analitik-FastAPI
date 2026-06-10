from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from fastapi import HTTPException
import httpx
import os
import asyncio
from services.data_service import get_cleaned_city_data
from services.ann_service import train_and_forecast

# Backend URL configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")

# Pydantic models for request validation
class ForecastRequest(BaseModel):
    kota: str = Field(..., examples=["Kota Banda Aceh"])
    lag: Optional[int] = Field(default=3, ge=1, le=5)
    epochs: Optional[int] = Field(default=150, ge=10, le=1000)
    batch_size: Optional[int] = Field(default=2, ge=1, le=16)
    learning_rate: Optional[float] = Field(default=0.01, ge=0.0001, le=0.5)
    dropout_rate: Optional[float] = Field(default=0.1, ge=0.0, le=0.9)
    hidden_neurons: Optional[List[int]] = Field(default=[16, 8])

async def handle_forecasting_request(body: ForecastRequest) -> Dict[str, Any]:
    """
    Main controller to handle forecasting: fetches data, trains model, 
    and predicts next values for Inflasi, IHK, and all Commodity groups.
    """
    try:
        # 1. Fetch cleaned historical data (17 months) from backend Node.js
        city_data = await get_cleaned_city_data(body.kota)
    except RuntimeError as run_err:
        raise HTTPException(status_code=400, detail=str(run_err))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan saat memproses data kota: {str(e)}")

    series_data = city_data["series"]
    resolved_kota = city_data["kota"]

    # 2. Perform forecasting for Inflasi
    inflasi_series = series_data["inflasi"]
    if len(inflasi_series) < (body.lag + 1):
        raise HTTPException(
            status_code=400, 
            detail=f"Data inflasi untuk {resolved_kota} terlalu sedikit ({len(inflasi_series)} data) untuk lag = {body.lag}."
        )
        
    inflasi_res = train_and_forecast(
        series=inflasi_series,
        city_name=resolved_kota,
        var_name="Inflasi",
        lag=body.lag,
        epochs=body.epochs,
        batch_size=body.batch_size,
        learning_rate=body.learning_rate,
        dropout_rate=body.dropout_rate,
        hidden_neurons=body.hidden_neurons
    )

    # 3. Perform forecasting for IHK
    ihk_series = series_data["ihk"]
    if len(ihk_series) < (body.lag + 1):
        raise HTTPException(
            status_code=400, 
            detail=f"Data IHK untuk {resolved_kota} terlalu sedikit ({len(ihk_series)} data) untuk lag = {body.lag}."
        )

    ihk_res = train_and_forecast(
        series=ihk_series,
        city_name=resolved_kota,
        var_name="IHK",
        lag=body.lag,
        epochs=body.epochs,
        batch_size=body.batch_size,
        learning_rate=body.learning_rate,
        dropout_rate=body.dropout_rate,
        hidden_neurons=body.hidden_neurons
    )

    # 4. Perform forecasting for Komoditas (each of the 11 groups)
    komoditas_series_dict = series_data["komoditas"]
    komoditas_results = {}

    for name, komo_series in komoditas_series_dict.items():
        if len(komo_series) < (body.lag + 1):
            continue # Skip if data is too small for some reason
        
        komo_res = train_and_forecast(
            series=komo_series,
            city_name=resolved_kota,
            var_name=name,
            lag=body.lag,
            epochs=body.epochs,
            batch_size=body.batch_size,
            learning_rate=body.learning_rate,
            dropout_rate=body.dropout_rate,
            hidden_neurons=body.hidden_neurons
        )
        komoditas_results[name] = {
            "historical_series": komo_series,
            "forecast_value": komo_res["forecast_value"],
            "loss_history": komo_res["loss_history"],
            "final_loss": komo_res["final_loss"]
        }

    # 5. Assemble final response
    return {
        "status": "success",
        "kota": resolved_kota,
        "regionVal_ihk": city_data["regionVal_ihk"],
        "regionVal_inflasi": city_data["regionVal_inflasi"],
        "forecast": {
            "inflasi": {
                "historical_series": inflasi_series,
                "forecast_value": inflasi_res["forecast_value"],
                "loss_history": inflasi_res["loss_history"],
                "final_loss": inflasi_res["final_loss"],
                "train_predictions": inflasi_res["train_predictions"],
                "actual_targets": inflasi_res["actual_values"]
            },
            "ihk": {
                "historical_series": ihk_series,
                "forecast_value": ihk_res["forecast_value"],
                "loss_history": ihk_res["loss_history"],
                "final_loss": ihk_res["final_loss"],
                "train_predictions": ihk_res["train_predictions"],
                "actual_targets": ihk_res["actual_values"]
            },
            "komoditas": komoditas_results
        },
        "hyperparameters": {
            "lag": body.lag,
            "epochs": body.epochs,
            "batch_size": body.batch_size,
            "learning_rate": body.learning_rate,
            "dropout_rate": body.dropout_rate,
            "hidden_neurons": body.hidden_neurons
        }
    }

async def handle_batch_forecasting_task():
    """
    Background worker that runs forecasting on all 150+ cities sequentially 
    and posts results back to Express backend MongoDB.
    """
    print("[Batch Tasks] Memulai proses peramalan massal latar belakang...")
    try:
        # Fetch cities
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(f"{BACKEND_URL}/api/kota")
            response.raise_for_status()
            cities = response.json()
    except Exception as e:
        print(f"[Batch Tasks] CRITICAL ERROR: Gagal mengambil daftar kota: {str(e)}")
        return

    success_count = 0
    failed_count = 0
    
    print(f"[Batch Tasks] Ditemukan {len(cities)} kota. Memulai training...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for idx, city in enumerate(cities):
            city_name = city.get("name")
            print(f"[Batch Tasks] ({idx+1}/{len(cities)}) Memproses {city_name}...", end="")
            try:
                # Reuse the single request logic
                req = ForecastRequest(
                    kota=city_name,
                    lag=3,
                    epochs=150,
                    batch_size=2,
                    learning_rate=0.01,
                    dropout_rate=0.1,
                    hidden_neurons=[16, 8]
                )
                res = await handle_forecasting_request(req)
                
                # Save to backend
                save_resp = await client.post(f"{BACKEND_URL}/api/dashboard/overview/forecast/save", json=res)
                save_resp.raise_for_status()
                print(" -> OK!")
                success_count += 1
            except Exception as err:
                print(f" -> ❌ FAILED: {str(err)}")
                failed_count += 1
                
            # Yield control briefly
            await asyncio.sleep(0.05)

    print(f"[Batch Tasks] PROSES MASSAL SELESAI! Sukses: {success_count}, Gagal: {failed_count}")
