import os
import httpx
from typing import Dict, List, Any

# Port and server URL configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")

# Commodity groups configurations (matching verKelompokIHK.json)
KOMODITAS_CONFIGS = [
    {"nama": "Makanan, Minuman dan Tembakau", "var": 2223, "turvar": 1551},
    {"nama": "Pakaian dan Alas Kaki", "var": 2224, "turvar": 1555},
    {"nama": "Perumahan, Air, Listrik dan Bahan Bakar Rumah Tangga", "var": 2225, "turvar": 1558},
    {"nama": "Perlengkapan, Peralatan dan Pemeliharaan Rutin Rumah Tangga", "var": 2226, "turvar": 1563},
    {"nama": "Kesehatan", "var": 2227, "turvar": 1570},
    {"nama": "Informasi, Komunikasi dan Jasa Keuangan", "var": 2228, "turvar": 1580},
    {"nama": "Transportasi", "var": 2229, "turvar": 1575},
    {"nama": "Rekreasi, Olahraga dan Budaya", "var": 2230, "turvar": 1585},
    {"nama": "Pendidikan", "var": 2231, "turvar": 1592},
    {"nama": "Penyediaan Makanan dan Minuman / Restoran", "var": 2232, "turvar": 1597},
    {"nama": "Perawatan Pribadi dan Jasa Lainnya", "var": 2233, "turvar": 1599}
]

async def fetch_raw_data(client: httpx.AsyncClient, endpoint: str, kota: str) -> Dict[str, Any]:
    """
    Helper to post and fetch raw json from backend
    """
    response = await client.post(f"{BACKEND_URL}/api/dashboard/overview/{endpoint}", json={"kota": kota})
    response.raise_for_status()
    return response.json()

async def get_cleaned_city_data(kota: str) -> Dict[str, Any]:
    """
    Fetches raw data for inflasi, ihk, and komoditas from Node.js backend
    and cleans it to return a 17-month series for each variable.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Fetch in parallel
        try:
            inflasi_raw = await fetch_raw_data(client, "inflasi", kota)
            ihk_raw = await fetch_raw_data(client, "ihk", kota)
            komoditas_raw = await fetch_raw_data(client, "komoditas", kota)
        except Exception as e:
            raise RuntimeError(f"Gagal mengambil data dari Node.js backend: {str(e)}")

        # Extract resolved city name and region value
        # Note: regionVal in ihk is the key to match IHK and Komoditas
        resolved_kota = inflasi_raw.get("kota", kota)
        region_val_inflasi = inflasi_raw.get("regionVal", "")
        region_val_ihk = ihk_raw.get("regionVal", "")

        # 1. Clean Inflasi Data (12 YoY + 5 Current = 17 points)
        # Filter key format: region_val_inflasi + "101" + ...
        # (var.val is 1, prefix is 1, so prefix + varVal is 11, wait, starts with regionVal + "101")
        inflasi_filter = f"{region_val_inflasi}101"
        
        raw_inf_yoy = [item for item in inflasi_raw.get("yoy", []) if item.get("key", "").startswith(inflasi_filter)]
        raw_inf_cur = [item for item in inflasi_raw.get("data", []) if item.get("key", "").startswith(inflasi_filter)]
        
        # Sort chronologically by key (numeric value of key)
        raw_inf_yoy_sorted = sorted(raw_inf_yoy, key=lambda x: int(x["key"]))
        raw_inf_cur_sorted = sorted(raw_inf_cur, key=lambda x: int(x["key"]))
        
        # Merge lists
        inflasi_series = [float(item["value"]) for item in (raw_inf_yoy_sorted + raw_inf_cur_sorted)]

        # 2. Clean IHK Data (12 YoY + 5 Current = 17 points)
        # Filter key format: region_val_ihk + "224501" + ...
        # (var.val is 2245, prefix is 2, so regionVal + "224501")
        ihk_filter = f"{region_val_ihk}224501"
        
        raw_ihk_yoy = [item for item in ihk_raw.get("yoy", []) if item.get("key", "").startswith(ihk_filter)]
        raw_ihk_cur = [item for item in ihk_raw.get("data", []) if item.get("key", "").startswith(ihk_filter)]
        
        # Sort chronologically
        raw_ihk_yoy_sorted = sorted(raw_ihk_yoy, key=lambda x: int(x["key"]))
        raw_ihk_cur_sorted = sorted(raw_ihk_cur, key=lambda x: int(x["key"]))
        
        ihk_series = [float(item["value"]) for item in (raw_ihk_yoy_sorted + raw_ihk_cur_sorted)]

        # 3. Clean Komoditas Data (11 main groups, each with 12 YoY + 5 Current = 17 points)
        # We match each config group name in raw data and clean its time series
        komoditas_series_dict = {}
        
        # Group raw data by label for easier lookup
        hierarki_by_label = {item["label"]: item for item in komoditas_raw.get("hierarki", [])}
        yoy_by_label = {item["label"]: item for item in komoditas_raw.get("yoy", [])}

        for idx, config in enumerate(KOMODITAS_CONFIGS):
            name = config["nama"]
            var_val = config["var"] # 2223 + idx
            turvar_val = config["turvar"]
            
            # Key filter prefix: region_val_ihk + "2" + varVal without first digit + turvarVal
            # varVal without first digit is str(223 + idx)
            # E.g., for i = 0 (var = 2223): "2" + "223" + str(turvar) = "2223" + str(turvar)
            komoditas_filter = f"{region_val_ihk}2{223 + idx}{turvar_val}"
            
            # Extract current year data
            cur_group = hierarki_by_label.get(name, {})
            cur_data_dict = cur_group.get("data", {})
            cur_items = [{"key": k, "value": v} for k, v in cur_data_dict.items() if k.startswith(komoditas_filter)]
            
            # Extract YoY data
            yoy_group = yoy_by_label.get(name, {})
            yoy_data_dict = yoy_group.get("data", {})
            yoy_items = [{"key": k, "value": v} for k, v in yoy_data_dict.items() if k.startswith(komoditas_filter)]
            
            # Sort chronologically
            yoy_sorted = sorted(yoy_items, key=lambda x: int(x["key"]))
            cur_sorted = sorted(cur_items, key=lambda x: int(x["key"]))
            
            # Merge
            merged_series = [float(item["value"]) for item in (yoy_sorted + cur_sorted)]
            komoditas_series_dict[name] = merged_series

        return {
            "kota": resolved_kota,
            "regionVal_ihk": region_val_ihk,
            "regionVal_inflasi": region_val_inflasi,
            "series": {
                "inflasi": inflasi_series,
                "ihk": ihk_series,
                "komoditas": komoditas_series_dict
            }
        }
