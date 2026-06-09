# Hasil Pelatihan dan Peramalan Artificial Neural Network (ANN)

Berikut adalah ringkasan hasil pengujian model Jaringan Saraf Tiruan (ANN) yang dilatih menggunakan data historis 17 bulan untuk **KOTA BANDA ACEH**.

---

## 1. Nilai Peramalan (Bulan ke-18 - Juni 2026)

| Variabel | Nilai Ramalan | Nilai Terakhir (Mei 2026) | Trend / Keterangan |
| :--- | :---: | :---: | :--- |
| **Inflasi** | `0.1410%` | `0.9300%` | Turun |
| **IHK** | `113.5586` | `113.7800` | Turun |

---

## 2. Tabel Data Input Historis & Hasil Peramalan (Inflasi & IHK)

Tabel di bawah ini menampilkan 17 data masuk (input historis) yang digunakan untuk melatih model ANN, diikuti oleh hasil peramalan untuk Bulan ke-18 (Juni 2026) pada variabel utama:

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
| 18 | **Jun 2026** | **`0.1410%`** | **`113.5586`** | **Hasil Ramalan (ANN)** |


---

## 3. Tabel Data Input Historis & Hasil Peramalan Komoditas (Kelompok I)

Tabel di bawah ini menampilkan data masuk historis (17 bulan) dan hasil peramalan (Bulan 18) untuk Kelompok Komoditas Utama bagian I:

| Bulan Ke- | Periode | Makanan & Tembakau | Pakaian & Alas Kaki | Perumahan & Energi | Perlengkapan RT | Kesehatan |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Jan 2025 | `2.7800%` | `0.1300%` | `-7.9500%` | `0.1700%` | `0.0000%` |
| 2 | Feb 2025 | `-0.4700%` | `-0.9400%` | `-3.6600%` | `0.1600%` | `0.3000%` |
| 3 | Mar 2025 | `0.6500%` | `0.6300%` | `7.0900%` | `-0.5000%` | `0.1600%` |
| 4 | Apr 2025 | `1.7600%` | `0.7500%` | `5.3300%` | `-0.2000%` | `0.3900%` |
| 5 | Mei 2025 | `-1.1200%` | `-0.1300%` | `0.1900%` | `-0.2100%` | `0.0000%` |
| 6 | Jun 2025 | `-0.6000%` | `0.1300%` | `-0.0100%` | `0.4500%` | `-0.0200%` |
| 7 | Jul 2025 | `1.2200%` | `3.2500%` | `0.0000%` | `-0.0300%` | `0.4200%` |
| 8 | Ags 2025 | `1.5400%` | `-0.5700%` | `0.0000%` | `0.1000%` | `1.0100%` |
| 9 | Sep 2025 | `0.8500%` | `-0.8700%` | `-0.0200%` | `0.0100%` | `0.9100%` |
| 10 | Okt 2025 | `-0.4700%` | `0.1100%` | `0.0000%` | `0.1700%` | `0.0000%` |
| 11 | Nov 2025 | `-1.6400%` | `-2.4100%` | `0.0000%` | `-0.3500%` | `0.7100%` |
| 12 | Des 2025 | `7.0200%` | `-0.1000%` | `1.9500%` | `0.0100%` | `-0.2400%` |
| 13 | Jan 2026 | `-2.8600%` | `-0.0200%` | `-1.7500%` | `0.0600%` | `0.4500%` |
| 14 | Feb 2026 | `0.8600%` | `0.3800%` | `-0.4000%` | `-0.0100%` | `-0.0300%` |
| 15 | Mar 2026 | `0.1600%` | `-2.9000%` | `0.0200%` | `-0.2000%` | `-0.0200%` |
| 16 | Apr 2026 | `-0.6800%` | `-0.0500%` | `0.5400%` | `1.6300%` | `-0.0600%` |
| 17 | Mei 2026 | `1.8900%` | `0.0400%` | `1.0700%` | `0.3100%` | `0.1600%` |
| 18 | **Jun 2026** | **`-0.2949%`** | **`0.4674%`** | **`0.1232%`** | **`0.0017%`** | **`0.5690%`** |


---

## 4. Tabel Data Input Historis & Hasil Peramalan Komoditas (Kelompok II)

Tabel di bawah ini menampilkan data masuk historis (17 bulan) dan hasil peramalan (Bulan 18) untuk Kelompok Komoditas Utama bagian II:

| Bulan Ke- | Periode | Info & Keuangan | Transportasi | Rekreasi & Budaya | Pendidikan | Restoran | Perawatan & Jasa |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Jan 2025 | `-0.0200%` | `1.1100%` | `-0.9900%` | `0.0000%` | `0.1300%` | `0.6200%` |
| 2 | Feb 2025 | `0.0000%` | `1.3700%` | `0.0000%` | `0.0000%` | `0.0300%` | `2.0700%` |
| 3 | Mar 2025 | `0.0000%` | `0.1200%` | `-0.0200%` | `0.0000%` | `0.0300%` | `1.9800%` |
| 4 | Apr 2025 | `-0.2800%` | `0.2600%` | `0.3700%` | `0.0000%` | `0.0000%` | `4.8300%` |
| 5 | Mei 2025 | `0.3700%` | `0.1900%` | `-0.0100%` | `0.0000%` | `0.0000%` | `-1.2600%` |
| 6 | Jun 2025 | `-0.3300%` | `-0.3600%` | `0.0000%` | `0.0000%` | `0.0000%` | `0.6600%` |
| 7 | Jul 2025 | `0.0000%` | `0.0500%` | `0.0000%` | `-2.0100%` | `0.1500%` | `-0.1700%` |
| 8 | Ags 2025 | `0.0000%` | `-0.3400%` | `0.0100%` | `0.0900%` | `0.1200%` | `-0.2200%` |
| 9 | Sep 2025 | `0.0000%` | `-0.0100%` | `0.0000%` | `0.0600%` | `0.1200%` | `2.2800%` |
| 10 | Okt 2025 | `0.0500%` | `0.6600%` | `0.0000%` | `0.0000%` | `0.0000%` | `5.6800%` |
| 11 | Nov 2025 | `-0.0200%` | `0.3600%` | `0.0400%` | `0.0000%` | `0.1200%` | `0.3400%` |
| 12 | Des 2025 | `0.0000%` | `0.0700%` | `0.0000%` | `0.0000%` | `4.3700%` | `2.7400%` |
| 13 | Jan 2026 | `0.1000%` | `-0.1400%` | `0.0000%` | `0.0000%` | `0.9600%` | `3.8100%` |
| 14 | Feb 2026 | `0.4100%` | `-0.0400%` | `0.0000%` | `0.0000%` | `0.1500%` | `2.5700%` |
| 15 | Mar 2026 | `0.6700%` | `0.8500%` | `0.0000%` | `0.0000%` | `1.7100%` | `-1.2900%` |
| 16 | Apr 2026 | `1.8300%` | `1.9400%` | `1.6400%` | `0.0000%` | `0.4800%` | `-2.4300%` |
| 17 | Mei 2026 | `0.6400%` | `0.0200%` | `0.0000%` | `0.0000%` | `1.5300%` | `-0.4400%` |
| 18 | **Jun 2026** | **`2.9473%`** | **`0.0167%`** | **`0.1955%`** | **`-0.2336%`** | **`0.6839%`** | **`4.7027%`** |


---

## 5. Grafik Hasil Pelatihan (Loss Function)

Grafik di bawah menunjukkan kurva penurunan tingkat error (**Mean Squared Error / MSE**) model Inflasi dan IHK selama 150 epoch pelatihan. Loss yang mengecil mendekati nol menandakan model berhasil belajar secara optimal.

![Kurva Loss MSE](loss_chart.png)

---

## 6. Perbandingan Data Aktual vs Prediksi Model

Grafik di bawah ini membandingkan data aktual historis dengan hasil fitting (prediksi) model ANN saat fase latihan, serta menampilkan proyeksi nilai hasil ramalan untuk bulan ke-18.

### A. Grafik Peramalan Inflasi
![Grafik Inflasi](inflasi_forecast_chart.png)

### B. Grafik Peramalan IHK
![Grafik IHK](ihk_forecast_chart.png)

---

## 7. Hasil Ringkasan Peramalan Komoditas

Berikut adalah estimasi nilai inflasi untuk 11 kelompok komoditas utama di **KOTA BANDA ACEH** pada bulan ke-18 beserta tingkat MSE loss-nya:

| Kelompok Komoditas | Nilai Ramalan (%) | Final Training Loss (MSE) |
| :--- | :---: | :---: |
| Makanan, Minuman dan Tembakau | `-0.2949%` | `0.027368` |
| Pakaian dan Alas Kaki | `0.4674%` | `0.048991` |
| Perumahan, Air, Listrik dan Bahan Bakar Rumah Tangga | `0.1232%` | `0.011980` |
| Perlengkapan, Peralatan dan Pemeliharaan Rutin Rumah Tangga | `0.0017%` | `0.049269` |
| Kesehatan | `0.5690%` | `0.038873` |
| Informasi, Komunikasi dan Jasa Keuangan | `2.9473%` | `0.034496` |
| Transportasi | `0.0167%` | `0.024450` |
| Rekreasi, Olahraga dan Budaya | `0.1955%` | `0.065174` |
| Pendidikan | `-0.2336%` | `0.063183` |
| Penyediaan Makanan dan Minuman / Restoran | `0.6839%` | `0.065598` |
| Perawatan Pribadi dan Jasa Lainnya | `4.7027%` | `0.015695` |
