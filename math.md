# Pemodelan Matematika Artificial Neural Network (ANN)

Dokumen ini menjelaskan model matematika dari Artificial Neural Network (ANN) tipe Multi-Layer Perceptron (MLP) yang digunakan untuk melakukan peramalan (forecasting) data deret waktu (univariate time series) seperti IHK, Inflasi, dan nilai komoditas.

---

## 1. Representasi Input (Sliding Window / Lag)

Diberikan data deret waktu historis $X = \{x_1, x_2, \dots, x_N\}$ dengan $N = 17$ titik data (12 data bulanan YoY tahun lalu + 5 data bulanan tahun berjalan).

Kita mengubah masalah deret waktu ini menjadi pembelajaran terawasi (supervised learning) dengan pendekatan **Sliding Window (Lag)** sebesar $L$ (misal $L = 3$). 

Setiap sampel ke-$t$ terdiri dari vektor input $\mathbf{x}_t$ dan target $y_t$:
- **Vektor Input (Fitur)**:
  $$\mathbf{x}_t = \begin{bmatrix} x_{t-L} \\ x_{t-L+1} \\ \vdots \\ x_{t-1} \end{bmatrix} \in \mathbb{R}^{L}$$
- **Nilai Target (Label)**:
  $$y_t = x_t \in \mathbb{R}$$

Banyaknya pasangan data latih $(M)$ yang terbentuk dari data berukuran $N$ adalah:
$$M = N - L$$

---

## 2. Arsitektur Jaringan (Forward Propagation)

Arsitektur jaringan terdiri dari 1 Input Layer (ukuran $L$), $H$ Hidden Layer (Layer Tersembunyi), dan 1 Output Layer (ukuran 1 untuk regresi).

### A. Input Layer (Layer 0)
Aktivasi pada layer input sama dengan vektor fitur input itu sendiri:
$$\mathbf{a}^{(0)} = \mathbf{x}_t$$

### B. Hidden Layer $l$ ($l = 1, 2, \dots, H$)
Untuk setiap Hidden Layer $l$, nilai pra-aktivasi $\mathbf{z}^{(l)}$ dihitung dengan perkalian dot matriks bobot $\mathbf{W}^{(l)}$ dengan aktivasi layer sebelumnya $\mathbf{a}^{(l-1)}$ ditambah bias $\mathbf{b}^{(l)}$:
$$\mathbf{z}^{(l)} = \mathbf{W}^{(l)} \mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}$$

Dimana:
- $\mathbf{W}^{(l)} \in \mathbb{R}^{n_l \times n_{l-1}}$ adalah matriks bobot untuk layer $l$.
- $\mathbf{b}^{(l)} \in \mathbb{R}^{n_l}$ adalah vektor bias untuk layer $l$.
- $n_l$ adalah jumlah neuron pada layer $l$.

#### Fungsi Aktivasi (ReLU)
Untuk layer tersembunyi, fungsi aktivasi yang digunakan adalah **Rectified Linear Unit (ReLU)**:
$$\mathbf{a}^{(l)} = \text{ReLU}(\mathbf{z}^{(l)}) = \max(\mathbf{0}, \mathbf{z}^{(l)})$$

#### Regularisasi (Dropout)
Saat proses pelatihan (training), lapisan Dropout diterapkan pada aktivasi $\mathbf{a}^{(l)}$ untuk mencegah overfitting dengan mematikan neuron secara acak dengan probabilitas $p$:
$$\mathbf{a}^{(l)} = \mathbf{a}^{(l)} \odot \mathbf{m}^{(l)} \cdot \frac{1}{1-p}$$
Dimana $\mathbf{m}^{(l)}$ adalah vektor biner masker Bernoulli dengan probabilitas sukses $1-p$, dan $\odot$ menyatakan perkalian elemen-demi-elemen (Hadamard product).

### C. Output Layer (Layer $H+1$)
Untuk peramalan/regresi nilai kontinu, lapisan output menggunakan aktivasi linear (tanpa fungsi aktivasi non-linear):
$$\hat{y}_t = z^{(H+1)} = \mathbf{W}^{(H+1)} \mathbf{a}^{(H)} + b^{(H+1)}$$
Dimana $\hat{y}_t \in \mathbb{R}$ adalah nilai estimasi/prediksi untuk waktu ke-$t$.

---

## 3. Fungsi Kerugian (Loss Function)

Untuk mengukur performa model dalam melakukan regresi, digunakan **Mean Squared Error (MSE)** sebagai kriteria kerugian:
$$\mathcal{L}(\mathbf{W}, \mathbf{b}) = \frac{1}{M} \sum_{i=1}^{M} (y_i - \hat{y}_i)^2$$

Dimana:
- $y_i$ adalah nilai target aktual.
- $\hat{y}_i$ adalah nilai hasil prediksi model.
- $M$ adalah total jumlah sampel pelatihan.

---

## 4. Backpropagation & Optimasi

Proses pembaruan parameter (bobot $\mathbf{W}$ dan bias $\mathbf{b}$) dilakukan melalui metode **Backpropagation** berbasis gradien dengan algoritma optimasi **Adam (Adaptive Moment Estimation)**.

### Gradien Kerugian
Gradien parsial dihitung menggunakan aturan rantai (chain rule) untuk mengalirkan error dari layer output kembali ke layer input:
$$\delta^{(H+1)} = \frac{\partial \mathcal{L}}{\partial \mathbf{z}^{(H+1)}} = -2(y - \hat{y})$$
$$\delta^{(l)} = \left( (\mathbf{W}^{(l+1)})^T \delta^{(l+1)} \right) \odot f'(\mathbf{z}^{(l)})$$
Dimana $f'(\mathbf{z})$ adalah turunan dari fungsi aktivasi ReLU:
$$f'(z_j) = \begin{cases} 1 & \text{jika } z_j > 0 \\ 0 & \text{jika } z_j \leq 0 \end{cases}$$

Turunan parsial terhadap bobot dan bias pada layer $l$:
$$\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(l)}} = \delta^{(l)} (\mathbf{a}^{(l-1)})^T$$
$$\frac{\partial \mathcal{L}}{\partial \mathbf{b}^{(l)}} = \delta^{(l)}$$

### Pembaruan Parameter dengan Adam Optimizer
Adam memelihara nilai rata-rata eksponensial dari gradien terdahulu ($m$) dan kuadrat gradien terdahulu ($v$):
$$m_k^{(t)} = \beta_1 m_k^{(t-1)} + (1 - \beta_1) g_k^{(t)}$$
$$v_k^{(t)} = \beta_2 v_k^{(t-1)} + (1 - \beta_2) (g_k^{(t)})^2$$

Dimana $g_k^{(t)}$ adalah gradien terhadap parameter $\theta_k$ pada langkah $t$. Langkah koreksi bias:
$$\hat{m}_k^{(t)} = \frac{m_k^{(t)}}{1 - \beta_1^t}$$
$$\hat{v}_k^{(t)} = \frac{v_k^{(t)}}{1 - \beta_2^t}$$

Parameter diperbarui dengan aturan:
$$\theta_k^{(t+1)} = \theta_k^{(t)} - \frac{\eta}{\sqrt{\hat{v}_k^{(t)}} + \epsilon} \hat{m}_k^{(t)}$$

Dimana:
- $\eta$ adalah learning rate (laju pembelajaran).
- $\epsilon$ adalah konstanta stabilitas numerik ($10^{-7}$).
- $\beta_1, \beta_2$ adalah koefisien peluruhan eksponensial (default: $0.9$ dan $0.999$).
