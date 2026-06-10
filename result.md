# Hasil Pelatihan dan Peramalan Artificial Neural Network (ANN)

Berikut adalah ringkasan hasil pengujian model Jaringan Saraf Tiruan (ANN) yang dilatih menggunakan data historis 17 bulan untuk **KOTA METRO**.

---

## 1. Nilai Peramalan (Bulan ke-18 - Juni 2026)

| Variabel | Nilai Ramalan | Nilai Terakhir (Mei 2026) | Trend / Keterangan |
| :--- | :---: | :---: | :--- |
| **Inflasi** | `-0.7738%` | `1.1300%` | Turun |
| **IHK** | `106.5200` | `110.4100` | Turun |

---

## 2. Tabel Data Input Historis & Hasil Peramalan (Inflasi & IHK)

Tabel di bawah ini menampilkan 17 data masuk (input historis) yang digunakan untuk melatih model ANN, diikuti oleh hasil peramalan untuk Bulan ke-18 (Juni 2026) pada variabel utama:

| Bulan Ke- | Periode | Data Masuk: Inflasi | Data Masuk: IHK | Status Data |
| :---: | :---: | :---: | :---: | :--- |
| 1 | Jan 2025 | `-0.2800%` | `106.1300` | Historis (YoY) |
| 2 | Feb 2025 | `-0.8900%` | `105.1900` | Historis (YoY) |
| 3 | Mar 2025 | `1.9600%` | `107.2500` | Historis (YoY) |
| 4 | Apr 2025 | `0.6600%` | `107.9600` | Historis (YoY) |
| 5 | Mei 2025 | `-0.5300%` | `107.3900` | Historis (YoY) |
| 6 | Jun 2025 | `0.0400%` | `107.4300` | Historis (YoY) |
| 7 | Jul 2025 | `0.3200%` | `107.7700` | Historis (YoY) |
| 8 | Ags 2025 | `-0.6600%` | `107.0600` | Historis (YoY) |
| 9 | Sep 2025 | `0.3900%` | `107.4800` | Historis (YoY) |
| 10 | Okt 2025 | `0.2300%` | `107.7300` | Historis (YoY) |
| 11 | Nov 2025 | `0.1900%` | `107.9300` | Historis (YoY) |
| 12 | Des 2025 | `0.6700%` | `108.6500` | Historis (YoY) |
| 13 | Jan 2026 | `-0.3400%` | `108.2800` | Historis (Berjalan) |
| 14 | Feb 2026 | `0.4800%` | `108.8000` | Historis (Berjalan) |
| 15 | Mar 2026 | `0.1700%` | `108.9900` | Historis (Berjalan) |
| 16 | Apr 2026 | `0.1700%` | `109.1800` | Historis (Berjalan) |
| 17 | Mei 2026 | `1.1300%` | `110.4100` | Historis (Berjalan) |
| 18 | **Jun 2026** | **`-0.7738%`** | **`106.5200`** | **Hasil Ramalan (ANN)** |


---

## 3. Tabel Data Input Historis & Hasil Peramalan Komoditas (Kelompok I)

Tabel di bawah ini menampilkan data masuk historis (17 bulan) dan hasil peramalan (Bulan 18) untuk Kelompok Komoditas Utama bagian I:

| Bulan Ke- | Periode | Makanan & Tembakau | Pakaian & Alas Kaki | Perumahan & Energi | Perlengkapan RT | Kesehatan |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Jan 2025 | `3.5500%` | `0.5000%` | `-15.6400%` | `0.1400%` | `0.2900%` |
| 2 | Feb 2025 | `-1.4100%` | `-0.0700%` | `-5.9200%` | `-0.3100%` | `0.1100%` |
| 3 | Mar 2025 | `1.6500%` | `-0.2900%` | `16.4100%` | `0.3600%` | `-0.0200%` |
| 4 | Apr 2025 | `-1.1500%` | `0.0300%` | `9.4800%` | `-0.5600%` | `0.2000%` |
| 5 | Mei 2025 | `-1.5900%` | `-0.2000%` | `-0.0500%` | `-0.2700%` | `0.3900%` |
| 6 | Jun 2025 | `-0.0500%` | `0.0100%` | `0.0000%` | `0.2100%` | `0.0000%` |
| 7 | Jul 2025 | `0.6700%` | `-0.1800%` | `0.0200%` | `-0.5100%` | `0.0700%` |
| 8 | Ags 2025 | `-0.8200%` | `0.0200%` | `0.0000%` | `-0.4000%` | `-0.2000%` |
| 9 | Sep 2025 | `1.3500%` | `0.0100%` | `0.0500%` | `-0.6600%` | `-0.2700%` |
| 10 | Okt 2025 | `-0.0200%` | `-0.0100%` | `0.0200%` | `0.0200%` | `0.3000%` |
| 11 | Nov 2025 | `0.3300%` | `0.0000%` | `0.0200%` | `-0.5500%` | `0.2100%` |
| 12 | Des 2025 | `1.8500%` | `0.0000%` | `0.0600%` | `-0.1300%` | `0.4600%` |
| 13 | Jan 2026 | `-1.6200%` | `-0.1300%` | `0.1600%` | `0.5500%` | `0.0000%` |
| 14 | Feb 2026 | `1.0700%` | `-0.0200%` | `-0.0100%` | `0.0500%` | `0.0300%` |
| 15 | Mar 2026 | `0.6800%` | `-0.0300%` | `0.0300%` | `-0.3400%` | `-0.1300%` |
| 16 | Apr 2026 | `-0.0100%` | `0.6600%` | `0.2100%` | `0.0000%` | `0.0300%` |
| 17 | Mei 2026 | `2.1900%` | `0.0300%` | `0.0200%` | `1.4700%` | `0.0000%` |
| 18 | **Jun 2026** | **`-1.8295%`** | **`-0.4338%`** | **`-0.9990%`** | **`-1.3466%`** | **`-0.3291%`** |


---

## 4. Tabel Data Input Historis & Hasil Peramalan Komoditas (Kelompok II)

Tabel di bawah ini menampilkan data masuk historis (17 bulan) dan hasil peramalan (Bulan 18) untuk Kelompok Komoditas Utama bagian II:

| Bulan Ke- | Periode | Info & Keuangan | Transportasi | Rekreasi & Budaya | Pendidikan | Restoran | Perawatan & Jasa |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Jan 2025 | `-0.1800%` | `0.3900%` | `0.4500%` | `0.1500%` | `0.3500%` | `0.1000%` |
| 2 | Feb 2025 | `-0.5700%` | `0.3200%` | `0.0000%` | `0.0000%` | `0.0000%` | `0.6300%` |
| 3 | Mar 2025 | `0.0000%` | `0.3000%` | `0.0000%` | `0.0000%` | `0.2700%` | `1.6100%` |
| 4 | Apr 2025 | `-0.2200%` | `0.2300%` | `0.3100%` | `0.0000%` | `0.1900%` | `2.2900%` |
| 5 | Mei 2025 | `-0.0300%` | `-0.3200%` | `-0.0400%` | `0.0000%` | `0.0000%` | `0.2800%` |
| 6 | Jun 2025 | `-0.0500%` | `-0.0600%` | `0.0500%` | `0.0000%` | `0.0000%` | `0.7900%` |
| 7 | Jul 2025 | `0.2100%` | `0.6500%` | `-0.3900%` | `0.4700%` | `0.0000%` | `0.2800%` |
| 8 | Ags 2025 | `0.0200%` | `-0.1400%` | `0.0000%` | `-6.8700%` | `0.0700%` | `0.9500%` |
| 9 | Sep 2025 | `-0.0600%` | `0.0300%` | `0.0000%` | `0.0000%` | `0.0000%` | `0.4300%` |
| 10 | Okt 2025 | `-0.0300%` | `0.0000%` | `0.0000%` | `0.0000%` | `0.0000%` | `3.1400%` |
| 11 | Nov 2025 | `0.0500%` | `0.0100%` | `0.0000%` | `0.0000%` | `0.0000%` | `1.3100%` |
| 12 | Des 2025 | `0.0200%` | `0.4100%` | `0.0000%` | `0.0000%` | `0.0000%` | `0.4900%` |
| 13 | Jan 2026 | `-0.3400%` | `0.1900%` | `0.0000%` | `0.0000%` | `0.0000%` | `1.4800%` |
| 14 | Feb 2026 | `0.0500%` | `-0.2600%` | `-1.6000%` | `0.0000%` | `0.0000%` | `2.8800%` |
| 15 | Mar 2026 | `0.3100%` | `0.7000%` | `0.0000%` | `0.0000%` | `0.0000%` | `-1.5000%` |
| 16 | Apr 2026 | `0.3700%` | `0.1800%` | `0.4700%` | `0.0000%` | `1.1200%` | `-0.7100%` |
| 17 | Mei 2026 | `5.2400%` | `0.3200%` | `0.0000%` | `0.0000%` | `0.7700%` | `-0.5500%` |
| 18 | **Jun 2026** | **`-7.3282%`** | **`-0.3761%`** | **`-2.0603%`** | **`-8.2349%`** | **`-0.1937%`** | **`-1.6463%`** |


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

Berikut adalah estimasi nilai inflasi untuk 11 kelompok komoditas utama di **KOTA METRO** pada bulan ke-18 beserta tingkat MSE loss-nya:

| Kelompok Komoditas | Nilai Ramalan (%) | Final Training Loss (MSE) |
| :--- | :---: | :---: |
| Makanan, Minuman dan Tembakau | `-1.8295%` | `0.411140` |
| Pakaian dan Alas Kaki | `-0.4338%` | `0.145633` |
| Perumahan, Air, Listrik dan Bahan Bakar Rumah Tangga | `-0.9990%` | `0.123414` |
| Perlengkapan, Peralatan dan Pemeliharaan Rutin Rumah Tangga | `-1.3466%` | `0.231420` |
| Kesehatan | `-0.3291%` | `0.426532` |
| Informasi, Komunikasi dan Jasa Keuangan | `-7.3282%` | `0.123939` |
| Transportasi | `-0.3761%` | `0.419665` |
| Rekreasi, Olahraga dan Budaya | `-2.0603%` | `0.846762` |
| Pendidikan | `-8.2349%` | `1.124812` |
| Penyediaan Makanan dan Minuman / Restoran | `-0.1937%` | `0.154430` |
| Perawatan Pribadi dan Jasa Lainnya | `-1.6463%` | `0.453187` |
