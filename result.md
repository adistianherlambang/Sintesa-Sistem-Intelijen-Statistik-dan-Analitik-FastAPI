# Hasil Pelatihan dan Peramalan Artificial Neural Network (ANN)

Berikut adalah ringkasan hasil pengujian model Jaringan Saraf Tiruan (ANN) yang dilatih menggunakan data historis 17 bulan untuk **KOTA BANDA ACEH**.

---

## 1. Nilai Peramalan (Bulan ke-18 - Juni 2026)

| Variabel | Nilai Ramalan | Nilai Terakhir (Mei 2026) | Trend / Keterangan |
| :--- | :---: | :---: | :--- |
| **Inflasi** | `0.1386%` | `0.9300%` | Turun |
| **IHK** | `113.2400` | `113.7800` | Turun |

---

## 2. Tabel Data Input Historis & Hasil Peramalan

Tabel di bawah ini menampilkan 17 data masuk (input historis) yang digunakan untuk melatih model ANN, diikuti oleh hasil peramalan untuk Bulan ke-18 (Juni 2026):

| Bulan Ke- | Periode | Data Masuk: Inflasi | Data Masuk: IHK | Status Data |
| :---: | :---: | :---: | :---: | :--- |
| 1 | Jan 2025 | `-0.4700%` | `105.9100` | Historis (YoY) |
| 2 | Feb 2025 | `-0.4900%` | `105.3900` | Historis (YoY) |
| 3 | Mar 2025 | `1.5500%` | `107.0200` | Historis (YoY) |
| 4 | Apr 2025 | `1.8400%` | `108.9900` | Historis (YoY) |
| 5 | Mei 2025 | `-0.3600%` | `108.6000` | Historis (YoY) |
| 6 | Jun 2025 | `-0.1700%` | `108.4100` | Historis (YoY) |
| 7 | Jul 2025 | `0.4200%` | `108.8600` | Historis (YoY) |
| 8 | Ags 2025 | `0.4000%` | `109.3000` | Historis (YoY) |
| 9 | Sep 2025 | `0.3900%` | `109.7300` | Historis (YoY) |
| 10 | Okt 2025 | `0.3500%` | `110.1100` | Historis (YoY) |
| 11 | Nov 2025 | `-0.5300%` | `109.5300` | Historis (YoY) |
| 12 | Des 2025 | `3.0800%` | `112.9000` | Historis (YoY) |
| 13 | Jan 2026 | `-0.8100%` | `111.9800` | Historis (Berjalan) |
| 14 | Feb 2026 | `0.4200%` | `112.4500` | Historis (Berjalan) |
| 15 | Mar 2026 | `0.1200%` | `112.5800` | Historis (Berjalan) |
| 16 | Apr 2026 | `0.1300%` | `112.7300` | Historis (Berjalan) |
| 17 | Mei 2026 | `0.9300%` | `113.7800` | Historis (Berjalan) |
| 18 | **Jun 2026** | **`0.1386%`** | **`113.2400`** | **Hasil Ramalan (ANN)** |


---

## 3. Grafik Hasil Pelatihan (Loss Function)

Grafik di bawah menunjukkan kurva penurunan tingkat error (**Mean Squared Error / MSE**) model Inflasi dan IHK selama 150 epoch pelatihan. Loss yang mengecil mendekati nol menandakan model berhasil belajar secara optimal.

![Kurva Loss MSE](loss_chart.png)

---

## 4. Perbandingan Data Aktual vs Prediksi Model

Grafik di bawah ini membandingkan data aktual historis dengan hasil fitting (prediksi) model ANN saat fase latihan, serta menampilkan proyeksi nilai hasil ramalan untuk bulan ke-18.

### A. Grafik Peramalan Inflasi
![Grafik Inflasi](inflasi_forecast_chart.png)

### B. Grafik Peramalan IHK
![Grafik IHK](ihk_forecast_chart.png)

---

## 5. Hasil Peramalan Kelompok Komoditas Utama

Berikut adalah estimasi nilai inflasi untuk 11 kelompok komoditas utama di **KOTA BANDA ACEH** pada bulan ke-18:

| Kelompok Komoditas | Nilai Ramalan (%) | Final Training Loss (MSE) |
| :--- | :---: | :---: |
| Makanan, Minuman dan Tembakau | `-0.1029%` | `0.010636` |
| Pakaian dan Alas Kaki | `-0.0585%` | `0.029581` |
| Perumahan, Air, Listrik dan Bahan Bakar Rumah Tangga | `0.0963%` | `0.021069` |
| Perlengkapan, Peralatan dan Pemeliharaan Rutin Rumah Tangga | `0.0568%` | `0.054866` |
| Kesehatan | `0.5475%` | `0.010730` |
| Informasi, Komunikasi dan Jasa Keuangan | `3.2664%` | `0.006686` |
| Transportasi | `0.2078%` | `0.029737` |
| Rekreasi, Olahraga dan Budaya | `0.1754%` | `0.065199` |
| Pendidikan | `-0.1953%` | `0.064247` |
| Penyediaan Makanan dan Minuman / Restoran | `0.7307%` | `0.055138` |
| Perawatan Pribadi dan Jasa Lainnya | `1.7500%` | `0.024735` |
