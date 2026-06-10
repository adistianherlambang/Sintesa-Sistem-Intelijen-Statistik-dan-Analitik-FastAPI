import httpx
import asyncio
import os
import sys
from typing import Dict, Any, List
from controllers.forecasting_controller import ForecastRequest, handle_forecasting_request

# Set backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")

async def get_all_cities() -> List[Dict[str, Any]]:
    """
    Fetch all cities from Node.js backend
    """
    url = f"{BACKEND_URL}/api/kota"
    print(f"Fetching cities from {url}...")
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

async def save_forecast_to_backend(client: httpx.AsyncClient, data: Dict[str, Any]):
    """
    Send forecast result to Node.js backend to save in MongoDB
    """
    url = f"{BACKEND_URL}/api/dashboard/overview/forecast/save"
    response = await client.post(url, json=data)
    response.raise_for_status()
    return response.json()

async def run_city_forecast(city_name: str) -> Dict[str, Any]:
    """
    Runs the full ANN training and forecasting for a single city on-the-fly.
    """
    # Instantiate default request parameters
    req = ForecastRequest(
        kota=city_name,
        lag=3,
        epochs=150,
        batch_size=2,
        learning_rate=0.01,
        dropout_rate=0.1,
        hidden_neurons=[16, 8]
    )
    # Re-use our handle_forecasting_request logic directly!
    return await handle_forecasting_request(req)

async def main():
    try:
        cities = await get_all_cities()
    except Exception as e:
        print(f"CRITICAL ERROR: Gagal memuat daftar kota: {str(e)}")
        sys.exit(1)

    print(f"Ditemukan {len(cities)} kota/kabupaten.")
    print("Memulai proses batch training & peramalan menggunakan model ANN...")
    
    success_count = 0
    failed_count = 0
    failed_cities = []
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for idx, city in enumerate(cities):
            city_name = city.get("name")
            city_id = city.get("id")
            
            # Simple progress log
            print(f"[{idx+1}/{len(cities)}] Memproses {city_name} ({city_id})...", end="", flush=True)
            
            try:
                # 1. Train models and get forecast
                forecast_result = await run_city_forecast(city_name)
                
                # 2. Post result back to Express to store in MongoDB
                await save_forecast_to_backend(client, forecast_result)
                
                print(" OK! (Tersimpan di DB)")
                success_count += 1
            except Exception as err:
                # Catch individual city failures so the whole batch doesn't halt
                print(f" FAILED! (Error: {str(err)})")
                failed_count += 1
                failed_cities.append((city_name, str(err)))
                
    print("\n" + "="*40)
    print("PROSES BATCH SELESAI!")
    print(f"Total Sukses : {success_count}/{len(cities)} kota")
    print(f"Total Gagal  : {failed_count}/{len(cities)} kota")
    if failed_count > 0:
        print("\nDaftar kota yang gagal:")
        for name, reason in failed_cities:
            print(f" - {name}: {reason}")
    print("="*40)

if __name__ == "__main__":
    # Ensure event loop can locate imports properly by appending current dir to path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    asyncio.run(main())
