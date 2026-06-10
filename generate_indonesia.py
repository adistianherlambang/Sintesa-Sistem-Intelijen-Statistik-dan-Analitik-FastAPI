import httpx
import asyncio
import matplotlib.pyplot as plt
import numpy as np
import os

async def main():
    url = "http://localhost:8000/api/forecast"
    payload = {
        "kota": "Indonesia",
        "lag": 3,
        "epochs": 150,
        "batch_size": 2,
        "learning_rate": 0.01,
        "dropout_rate": 0.1
    }
    
    print("Mengirim request ke FastAPI untuk melatih model dan meramal Indonesia...")
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json=payload)
            if response.status_code != 200:
                print(f"Error dari server: {response.text}")
                return
            
            res = response.json()
            forecast = res["forecast"]
            
            # --- Extract data for Inflasi ---
            inf_data = forecast["inflasi"]
            inf_actual = inf_data["actual_targets"]
            inf_pred = inf_data["train_predictions"]
            inf_forecast = inf_data["forecast_value"]
            inf_loss = inf_data["loss_history"]
            
            # --- Extract data for IHK ---
            ihk_data = forecast["ihk"]
            ihk_actual = ihk_data["actual_targets"]
            ihk_pred = ihk_data["train_predictions"]
            ihk_forecast = ihk_data["forecast_value"]
            ihk_loss = ihk_data["loss_history"]
            
            print("Membuat grafik loss function...")
            # 1. Plot Loss Function Chart
            plt.figure(figsize=(10, 5))
            plt.plot(inf_loss, label="Inflasi MSE Loss", color="#1f77b4", linewidth=2)
            plt.plot(ihk_loss, label="IHK MSE Loss", color="#2ca02c", linewidth=2)
            plt.title("ANN Model Training Loss (MSE) per Epoch - Indonesia", fontsize=14, fontweight='bold', pad=15)
            plt.xlabel("Epoch", fontsize=12)
            plt.ylabel("Mean Squared Error (MSE)", fontsize=12)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.legend(fontsize=11)
            plt.tight_layout()
            plt.savefig("loss_chart_indonesia.png", dpi=150)
            plt.close()
            
            print("Membuat grafik perbandingan peramalan...")
            # 2. Plot Inflasi Prediction vs Actual
            x_axis = np.arange(1, len(inf_actual) + 1)
            plt.figure(figsize=(10, 5))
            plt.plot(x_axis, inf_actual, 'o-', label="Data Aktual (Target)", color="#1f77b4", linewidth=2)
            plt.plot(x_axis, inf_pred, 'x--', label="Prediksi Jaringan (Train)", color="#ff7f0e", linewidth=1.8)
            plt.plot(len(inf_actual) + 1, inf_forecast, 'r*', markersize=14, label=f"Hasil Ramalan (Bulan 18): {inf_forecast:.4f}")
            plt.title("Peramalan Inflasi Indonesia: Data Aktual vs Hasil Fitting ANN", fontsize=14, fontweight='bold', pad=15)
            plt.xlabel("Index Sampel Latih (Sliding Window)", fontsize=12)
            plt.ylabel("Tingkat Inflasi (%)", fontsize=12)
            plt.xticks(np.append(x_axis, len(inf_actual) + 1))
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.legend(fontsize=11)
            plt.tight_layout()
            plt.savefig("inflasi_forecast_chart_indonesia.png", dpi=150)
            plt.close()
            
            # 3. Plot IHK Prediction vs Actual
            plt.figure(figsize=(10, 5))
            plt.plot(x_axis, ihk_actual, 'o-', label="Data Aktual (Target)", color="#2ca02c", linewidth=2)
            plt.plot(x_axis, ihk_pred, 'x--', label="Prediksi Jaringan (Train)", color="#d62728", linewidth=1.8)
            plt.plot(len(ihk_actual) + 1, ihk_forecast, 'r*', markersize=14, label=f"Hasil Ramalan (Bulan 18): {ihk_forecast:.4f}")
            plt.title("Peramalan IHK Indonesia: Data Aktual vs Hasil Fitting ANN", fontsize=14, fontweight='bold', pad=15)
            plt.xlabel("Index Sampel Latih (Sliding Window)", fontsize=12)
            plt.ylabel("Indeks Harga Konsumen (IHK)", fontsize=12)
            plt.xticks(np.append(x_axis, len(ihk_actual) + 1))
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.legend(fontsize=11)
            plt.tight_layout()
            plt.savefig("ihk_forecast_chart_indonesia.png", dpi=150)
            plt.close()
            
            # Generate IHK & Inflasi table
            months_labels = [
                "Jan 2025", "Feb 2025", "Mar 2025", "Apr 2025", "Mei 2025", "Jun 2025",
                "Jul 2025", "Ags 2025", "Sep 2025", "Okt 2025", "Nov 2025", "Des 2025",
                "Jan 2026", "Feb 2026", "Mar 2026", "Apr 2026", "Mei 2026"
            ]
            inf_series = inf_data["historical_series"]
            ihk_series = ihk_data["historical_series"]
            
            table_rows_general = ""
            for i in range(17):
                status = "Historis (YoY)" if i < 12 else "Historis (Berjalan)"
                table_rows_general += f"| {i+1} | {months_labels[i]} | `{inf_series[i]:.4f}%` | `{ihk_series[i]:.4f}` | {status} |\n"
            table_rows_general += f"| 18 | **Jun 2026** | **`{inf_forecast:.4f}%`** | **`{ihk_forecast:.4f}`** | **Hasil Ramalan (ANN)** |\n"
            
            # Commodity group lists
            c1_names = [
                "Makanan, Minuman dan Tembakau",
                "Pakaian dan Alas Kaki",
                "Perumahan, Air, Listrik dan Bahan Bakar Rumah Tangga",
                "Perlengkapan, Peralatan dan Pemeliharaan Rutin Rumah Tangga",
                "Kesehatan"
            ]
            c2_names = [
                "Informasi, Komunikasi dan Jasa Keuangan",
                "Transportasi",
                "Rekreasi, Olahraga dan Budaya",
                "Pendidikan",
                "Penyediaan Makanan dan Minuman / Restoran",
                "Perawatan Pribadi dan Jasa Lainnya"
            ]
            
            # Generate Commodity C1 Table
            table_rows_c1 = ""
            for i in range(17):
                row_str = f"| {i+1} | {months_labels[i]} "
                for name in c1_names:
                    val = forecast["komoditas"][name]["historical_series"][i]
                    row_str += f"| `{val:.4f}%` "
                row_str += "|\n"
                table_rows_c1 += row_str
            
            row_str_f = "| 18 | **Jun 2026** "
            for name in c1_names:
                val = forecast["komoditas"][name]["forecast_value"]
                row_str_f += f"| **`{val:.4f}%`** "
            row_str_f += "|\n"
            table_rows_c1 += row_str_f
            
            # Generate Commodity C2 Table
            table_rows_c2 = ""
            for i in range(17):
                row_str = f"| {i+1} | {months_labels[i]} "
                for name in c2_names:
                    val = forecast["komoditas"][name]["historical_series"][i]
                    row_str += f"| `{val:.4f}%` "
                row_str += "|\n"
                table_rows_c2 += row_str
            
            row_str_f = "| 18 | **Jun 2026** "
            for name in c2_names:
                val = forecast["komoditas"][name]["forecast_value"]
                row_str_f += f"| **`{val:.4f}%`** "
            row_str_f += "|\n"
            table_rows_c2 += row_str_f
            
            # Write resultIndonesia.md
            print("Menulis dokumen hasil ke resultIndonesia.md...")
            md_content = f"""# Hasil Pelatihan dan Peramalan Artificial Neural Network (ANN) - Nasional
            
Berikut adalah ringkasan hasil pengujian model Jaringan Saraf Tiruan (ANN) yang dilatih menggunakan data historis 17 bulan untuk **{res['kota']}**.

---

## 1. Nilai Peramalan (Bulan ke-18 - Juni 2026)

| Variabel | Nilai Ramalan | Nilai Terakhir (Mei 2026) | Trend / Keterangan |
| :--- | :---: | :---: | :--- |
| **Inflasi** | `{inf_forecast:.4f}%` | `{inf_actual[-1]:.4f}%` | {"Naik" if inf_forecast > inf_actual[-1] else "Turun"} |
| **IHK** | `{ihk_forecast:.4f}` | `{ihk_actual[-1]:.4f}` | {"Naik" if ihk_forecast > ihk_actual[-1] else "Turun"} |

---

## 2. Tabel Data Input Historis & Hasil Peramalan (Inflasi & IHK)

Tabel di bawah ini menampilkan 17 data masuk (input historis) yang digunakan untuk melatih model ANN, diikuti oleh hasil peramalan untuk Bulan ke-18 (Juni 2026) pada variabel utama:

| Bulan Ke- | Periode | Data Masuk: Inflasi | Data Masuk: IHK | Status Data |
| :---: | :---: | :---: | :---: | :--- |
{table_rows_general}

---

## 3. Tabel Data Input Historis & Hasil Peramalan Komoditas (Kelompok I)

Tabel di bawah ini menampilkan data masuk historis (17 bulan) dan hasil peramalan (Bulan 18) untuk Kelompok Komoditas Utama bagian I:

| Bulan Ke- | Periode | Makanan & Tembakau | Pakaian & Alas Kaki | Perumahan & Energi | Perlengkapan RT | Kesehatan |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
{table_rows_c1}

---

## 4. Tabel Data Input Historis & Hasil Peramalan Komoditas (Kelompok II)

Tabel di bawah ini menampilkan data masuk historis (17 bulan) dan hasil peramalan (Bulan 18) untuk Kelompok Komoditas Utama bagian II:

| Bulan Ke- | Periode | Info & Keuangan | Transportasi | Rekreasi & Budaya | Pendidikan | Restoran | Perawatan & Jasa |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
{table_rows_c2}

---

## 5. Grafik Hasil Pelatihan (Loss Function)

Grafik di bawah menunjukkan kurva penurunan tingkat error (**Mean Squared Error / MSE**) model Inflasi dan IHK selama 150 epoch pelatihan. Loss yang mengecil mendekati nol menandakan model berhasil belajar secara optimal.

![Kurva Loss MSE](loss_chart_indonesia.png)

---

## 6. Perbandingan Data Aktual vs Prediksi Model

Grafik di bawah ini membandingkan data aktual historis dengan hasil fitting (prediksi) model ANN saat fase latihan, serta menampilkan proyeksi nilai hasil ramalan untuk bulan ke-18.

### A. Grafik Peramalan Inflasi
![Grafik Inflasi](inflasi_forecast_chart_indonesia.png)

### B. Grafik Peramalan IHK
![Grafik IHK](ihk_forecast_chart_indonesia.png)

---

## 7. Hasil Ringkasan Peramalan Komoditas

Berikut adalah estimasi nilai inflasi untuk 11 kelompok komoditas utama di **{res['kota']}** pada bulan ke-18 beserta tingkat MSE loss-nya:

| Kelompok Komoditas | Nilai Ramalan (%) | Final Training Loss (MSE) |
| :--- | :---: | :---: |
"""
            for name, details in forecast["komoditas"].items():
                md_content += f"| {name} | `{details['forecast_value']:.4f}%` | `{details['final_loss']:.6f}` |\n"
                
            with open("resultIndonesia.md", "w") as f:
                f.write(md_content)
                
            print("Hasil sukses disimpan di resultIndonesia.md dan grafik PNG telah digenerate!")

    except Exception as e:
        import traceback
        print("Gagal memproses hasil:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
