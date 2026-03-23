# Analisis Kualitas Udara Beijing

**Penulis:** Muhamad Rizki Rifaldi  
**Proyek:** Submission Kelas Dicoding - Analisis Data  
**Status:** Proyek Individu

---

## 📖 Deskripsi Proyek

Proyek ini merupakan analisis data end-to-end untuk memahami pola distribusi dan karakteristik polusi udara di Beijing, China. Dataset yang digunakan mencakup pengukuran kualitas udara dari **12 stasiun** di Beijing selama periode **Maret 2013 hingga Februari 2017**.

Analisis ini bertujuan untuk menjawab dua pertanyaan bisnis utama:

1. **Stasiun mana yang memiliki rata-rata polusi PM2.5 paling tinggi**, dan bagaimana perbandingan tingkat polusi di seluruh 12 stasiun?

2. **Bagaimana pola polusi PM2.5 berubah sepanjang musim** (Semi, Panas, Gugur, Dingin) **dan waktu dalam sehari** (Pagi, Siang, Sore, Malam)?

Selain itu, proyek ini juga mencakup **analisis geospasial** untuk memvisualisasikan distribusi polusi di seluruh Beijing menggunakan peta interaktif.

---

## 📊 Sumber Data

Dataset yang digunakan adalah **Air Quality Dataset** dari Beijing, China yang tersedia secara publik. Data ini berisi pengukuran kualitas udara per jam yang meliputi:

| Kolom | Deskripsi |
|-------|-----------|
| PM2.5 | Partikel halus dengan diameter ≤ 2.5 μm |
| PM10 | Partikel dengan diameter ≤ 10 μm |
| SO2 | Sulfur Dioxide |
| NO2 | Nitrogen Dioxide |
| CO | Carbon Monoxide |
| O3 | Ozone |
| TEMP | Temperatur (°C) |
| PRES | Tekanan udara (hPa) |
| DEWP | Titik embun (°C) |
| RAIN | Curah hujan (mm) |
| WSPM | Kecepatan angin (m/s) |
| wd | Arah angin |
| station | Nama stasiun pengukuran |


---

## 🚀 Instalasi

### Prasyarat

Pastikan Anda telah menginstall **Python 3.8** atau versi yang lebih baru.

### Langkah Instalasi

1. **Clone atau download repository ini**

2. **Buka terminal/command prompt dan navigasi ke folder `submission`:**
   ```bash
   cd submission
   ```

3. **Install semua dependencies yang diperlukan:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 📁 Struktur Folder

```
submission/
├── assets/                    # Folder untuk visualisasi (PNG, HTML)
│   ├── *.png                 # Grafik dan chart
│   └── beijing_air_quality_map.html  # Peta interaktif
├── dashboard/
│   ├── main_data.csv         # Data yang sudah diproses untuk dashboard
│   └── dashboard.py          # Aplikasi Streamlit dashboard
├── data/
│   └── Air-quality-dataset/  # Data mentah dari 12 stasiun
│       └── PRSA_Data_20130301-20170228/
│           └── *.csv         # File CSV per stasiun
├── notebook.ipynb            # Jupyter Notebook dengan analisis lengkap
├── README.md                 # Dokumentasi proyek (file ini)
├── requirements.txt          # Daftar dependencies
└── url.txt                   # URL deployment Streamlit Cloud
```

---

## 📊 Cara Menjalankan Dashboard

### Menjalankan Secara Lokal

Setelah menginstall semua dependencies, jalankan dashboard dengan perintah:

```bash
cd submission
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka secara otomatis di browser Anda pada alamat `http://localhost:8501`.

### Fitur Dashboard

Dashboard interaktif ini memiliki **4 tab utama**:

1. **📊 Ringkasan Umum** - Menampilkan metrik utama dan tabel ringkasan per stasiun
2. **📈 Tren & Pola Polusi** - Visualisasi tren bulanan, pola musiman, dan pola harian
3. **🗺️ Peta Sebaran Polusi** - Peta interaktif folium dengan distribusi spasial polusi
4. **💡 Kesimpulan & Rekomendasi** - Insight utama dan rekomendasi kebijakan

### Filter yang Tersedia

- **Filter Stasiun:** Pilih satu atau lebih stasiun untuk dianalisis
- **Filter Tahun:** Pilih tahun tertentu (2013-2017)
- **Filter Musim:** Filter berdasarkan musim (Semi, Panas, Gugur, Dingin)

---

## ☁️ Deployment Streamlit Cloud

Dashboard ini dapat diakses secara online melalui Streamlit Cloud:

**[Masukkan URL Deployment Di Sini]**

> *Catatan: Ganti placeholder di atas dengan URL deployment actual setelah melakukan deploy ke Streamlit Cloud.*

### Cara Deploy ke Streamlit Cloud

1. Push kode ke repository GitHub
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Hubungkan repository GitHub Anda
4. Pilih file `dashboard/dashboard.py` sebagai file utama
5. Klik "Deploy"

---

## 📈 Metodologi Analisis

### 1. Data Wrangling

- **Gathering:** Menggabungkan data dari 12 file CSV stasiun menjadi satu DataFrame
- **Assessing:** Mengecek missing values, duplikat, tipe data, dan outlier
- **Cleaning:** 
  - Menghapus duplikat
  - Menghandle missing values dengan forward fill (ffill) dan backward fill (bfill)
  - Membuat kolom datetime dari kolom year, month, day, hour

### 2. Exploratory Data Analysis (EDA)

- **Analisis Statistik Deskriptif:** Menghitung rata-rata, median, dan distribusi polutan
- **Visualisasi:** Bar chart, boxplot, heatmap untuk memahami pola data
- **Analisis Temporal:** Pola berdasarkan musim dan waktu dalam sehari

### 3. Analisis Geospasial

- **Peta Interaktif (Folium):** Visualisasi distribusi spasial dengan circle markers
- **Klasifikasi AQI:** Kategorisasi berdasarkan konsentrasi PM2.5
- **Scatter Plot Geospasial:** Visualisasi statis dengan matplotlib

---

## 🎯 Kesimpulan Utama

Berdasarkan analisis yang dilakukan, berikut adalah temuan utama:

### Stasiun Paling Tercemar
1. **Changping** - Rata-rata PM2.5 tertinggi
2. **Dingling** - Wilayah utara-barat Beijing
3. **Wanliu** - Kawasan suburban berkembang

### Stasiun Paling Bersih
1. **Huairou** - Wilayah timur-laut dengan ruang terbuka hijau
2. **Shunyi** - Jauh dari kawasan industri
3. **Tiantan** - Pusat kota dengan monitoring baik

### Pola Temporal
- **Musim Dingin** menunjukkan polusi tertinggi akibat pemanas berbahan bakar batu bara
- **Musim Panas** memiliki kualitas udara terbaik
- **Malam hari (00-05)** memiliki konsentrasi PM2.5 tertinggi
- **Siang hari (12-17)** memiliki kualitas udara terbaik

---

## 🛠️ Teknologi yang Digunakan

| Teknologi | Fungsi |
|-----------|--------|
| Python 3.x | Bahasa pemrograman utama |
| Pandas | Manipulasi dan analisis data |
| NumPy | Operasi numerik |
| Matplotlib | Visualisasi data |
| Seaborn | Visualisasi statistik |
| Folium | Peta interaktif |
| Streamlit | Framework dashboard web |
| Streamlit-Folium | Integrasi Folium dengan Streamlit |
| Jupyter Notebook | Development dan dokumentasi analisis |

---

## 📝 Lisensi

Proyek ini dibuat untuk tujuan edukasi sebagai submission kelas Dicoding - Analisis Data.

---

## 📧 Kontak

**Penulis:** Muhamad Rizki Rifaldi

---

## ⚠️ Catatan Penting

- Proyek ini **tidak menggunakan machine learning**. Semua analisis berbasis statistik deskriptif dan rule-based.
- Koordinat stasiun di-hardcode langsung dalam kode (tidak menggunakan geocoding API).
- Semua teks dalam proyek ini (markdown, dashboard, insight) ditulis dalam **Bahasa Indonesia** yang natural.
- Ini adalah **proyek individu** yang dikerjakan oleh satu orang.

---

*Terima kasih telah mengunjungi proyek ini! 🙏*
