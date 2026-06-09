# Parameter Pelatihan Jaringan Saraf Tiruan (ANN)

Dokumen ini mendokumentasikan parameter dan konfigurasi hyperparameter yang digunakan untuk melatih model Artificial Neural Network (ANN) pada layanan peramalan (forecasting).

---

## 1. Spesifikasi Hyperparameter

Berikut adalah parameter latih yang disetel secara default untuk melatih model peramalan IHK, Inflasi, dan Nilai Komoditas:

| Parameter | Nilai Default | Penjelasan |
| :--- | :---: | :--- |
| **Learning Rate (Laju Pembelajaran)** | `0.01` | Mengontrol ukuran langkah optimasi bobot pada setiap iterasi. Nilai `0.01` dipilih agar proses konvergensi berjalan cepat pada data berukuran kecil. |
| **Epochs (Jumlah Iterasi)** | `150` | Jumlah iterasi penuh melewati seluruh dataset latih selama pelatihan. `150` epoch memberikan waktu yang cukup bagi model untuk belajar tanpa mengalami overfitting ekstrem. |
| **Batch Size (Ukuran Batch)** | `2` | Jumlah sampel data yang diproses sebelum bobot diperbarui. Menggunakan batch kecil (`2`) memberikan efek regulasi stokastik yang baik untuk dataset berukuran kecil. |
| **Lag / Window Size (Ukuran Jendela)** | `3` | Jumlah bulan historis yang digunakan sebagai input untuk memprediksi bulan berikutnya. Dengan 17 data poin, lag `3` menghasilkan $17 - 3 = 14$ data latih terawasi. |
| **Hidden Layers (Lapisan Tersembunyi)** | `2` | Jumlah layer antara input dan output. Dua layer tersembunyi memberikan kapasitas yang cukup untuk mempelajari pola tren non-linear. |
| **Neuron per Layer** | `[16, 8]` | Layer tersembunyi pertama memiliki `16` neuron, dan layer tersembunyi kedua memiliki `8` neuron (arsitektur menyempit untuk kompresi fitur). |
| **Activation Function (Hidden)** | `ReLU` | Fungsi aktivasi *Rectified Linear Unit* ($f(x) = \max(0, x)$) untuk memperkenalkan sifat non-linear pada model dan menghindari *vanishing gradient*. |
| **Activation Function (Output)** | `Linear` | Digunakan untuk regresi nilai kontinu tanpa membatasi rentang nilai keluaran. |
| **Loss Function (Fungsi Kerugian)** | `MSE` | *Mean Squared Error* (MSE) digunakan sebagai fungsi tujuan untuk meminimalkan selisih kuadrat antara hasil ramalan dan target aktual. |
| **Dropout Rate** | `0.1` | Probabilitas menonaktifkan neuron secara acak sebesar `10%` pada setiap layer tersembunyi selama pelatihan untuk mengurangi risiko overfitting. |
| **Optimizer** | `Adam` | Algoritma optimasi adaptif yang sangat andal dan menggabungkan keunggulan momentum RMSProp dan SGD. |

---

## 2. Justifikasi Konfigurasi untuk Data Kecil (17 Data Point)

Karena data latih yang tersedia relatif kecil (17 data poin bulanan: 12 data dari YoY tahun lalu + 5 data tahun berjalan), model ANN rentan terhadap **overfitting** (kondisi di mana model menghafal data latih namun gagal melakukan generalisasi pada data baru).

Oleh karena itu, strategi berikut diterapkan:
1. **Model Ringan (Arsitektur Dangkal)**: Jumlah neuron dibatasi maksimal `16` pada layer pertama dan `8` pada layer kedua agar model tidak terlalu kompleks.
2. **Adanya Dropout (0.1)**: Memaksa jaringan untuk belajar representasi fitur yang redundan dan kokoh, alih-alih bergantung pada neuron tertentu.
3. **Optimasi Berbasis Adam**: Algoritma Adam menyesuaikan learning rate secara otomatis per parameter, yang membantu menstabilkan proses training pada data yang terbatas.
4. **Validasi Kualitatif via MSE**: Riwayat nilai MSE per epoch akan dikembalikan ke API untuk divisualisasikan dalam bentuk grafik loss function, memberikan transparansi kualitas pelatihan model kepada pengguna.
