import httpx
import asyncio

async def test_endpoint():
    url = "http://localhost:8000/api/forecast"
    payload = {
        "kota": "Kota Banda Aceh",
        "lag": 3,
        "epochs": 50,
        "batch_size": 2,
        "learning_rate": 0.01,
        "dropout_rate": 0.1
    }
    
    print(f"Mengirim POST request ke: {url}")
    print(f"Payload: {payload}\n")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                print("=== RESPON SUKSES ===")
                print(f"Kota yang diramal: {data['kota']}")
                print(f"Region Val IHK: {data['regionVal_ihk']}")
                
                forecast = data["forecast"]
                
                # Print inflasi forecast
                inf_f = forecast["inflasi"]
                print(f"\n[Inflasi] Historis 17 bulan: {inf_f['historical_series']}")
                print(f"[Inflasi] Ramalan Bulan Depan: {inf_f['forecast_value']}")
                print(f"[Inflasi] Final Training Loss (MSE): {inf_f['final_loss']:.6f}")
                
                # Print IHK forecast
                ihk_f = forecast["ihk"]
                print(f"\n[IHK] Historis 17 bulan: {ihk_f['historical_series']}")
                print(f"[IHK] Ramalan Bulan Depan: {ihk_f['forecast_value']}")
                print(f"[IHK] Final Training Loss (MSE): {ihk_f['final_loss']:.6f}")
                
                # Print some commodity forecasts
                print("\n[Komoditas] Contoh Hasil Ramalan Kelompok Utama:")
                for name, details in list(forecast["komoditas"].items())[:3]:
                    print(f"  - {name}: {details['forecast_value']} (Final Loss: {details['final_loss']:.6f})")
                    
            else:
                print(f"=== RESPON ERROR === (Status: {response.status_code})")
                print(response.text)
    except Exception as e:
        print(f"Gagal menghubungkan ke server FastAPI: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_endpoint())
