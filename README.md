# Dashboard Analisis Pola Indeks Harga Konsumen (IHK) 38 Provinsi di Indonesia

**Proyek Akhir Visualisasi Data (VISDAT) · Semester Ganjil 2025/2026**  
**Politeknik Statistika STIS**

---

## Identitas Pengembang
- **Nama**: Syadza Khumairah Akmul
- **NIM**: 222313387
- **Kelas**: 3SD1
- **Institusi**: Politeknik Statistika STIS
- **Mata Kuliah**: Visualisasi Data (VISDAT)
- **Wilayah Analisis Fokus**: Provinsi Sulawesi Selatan

---

## Ringkasan Proyek
Aplikasi ini merupakan dashboard analitik interaktif berbasis **Streamlit** dan **Plotly** yang dirancang untuk menganalisis, memetakan, dan memvisualisasikan disparitas serta pola perilaku **Indeks Harga Konsumen (IHK)** di 38 provinsi di Indonesia (Tahun Dasar 2022 = 100) menggunakan data resmi publikasi **Badan Pusat Statistik (BPS) 2025**.

Dashboard ini menjawab pertanyaan riset utama:  
> *"Apakah pola perubahan harga konsumen di Indonesia memiliki karakteristik yang sama di setiap provinsi?"*

Melalui pendekatan multivariat, analisis jaringan spasial, dan dekomposisi hierarki 3 level, dashboard membuktikan bahwa pergerakan harga konsumen di Indonesia **tidak seragam**, melainkan terpolarisasi secara spasial dan sektoral akibat disparitas biaya logistik, struktur pasar pangan pokok, dan tingkat modernitas wilayah.

---

## Fitur Utama Dashboard

Aplikasi disusun ke dalam **4 Tab Utama** dengan layout penuh (*full-width*) dan sistem navigasi proporsional:

### 1. Macro Overview (Disparitas Spasial & Distribusi Agregat)
- **Dua Tampilan Alternatif Peta Geospasial**:
  - **Peta Choropleth (Area Poligon)**: Memvisualisasikan sebaran IHK agregat pada batas wilayah 38 provinsi menggunakan GeoJSON resmi dan basemap *OpenStreetMap*.
  - **Peta Simbol Proporsional (*Proportional Symbol Map*)**: Memetakan sebaran titik sentroid provinsi (`PROVINCE_COORDS`) dengan ukuran lingkaran (*size*) dan skala warna (*color*) yang terkalibrasi secara kontinu dan proporsional terhadap besaran IHK.
  - Dilengkapi penanda khusus provinsi sorotan (*brushing*) dan *hover tooltip* informatif (selisih terhadap rata-rata nasional).
- **Clustered Heatmap (38 Provinsi vs 11 Kelompok Pengeluaran)**:
  - Memetakan spektrum harga komoditas makro antarwilayah.
  - Dilengkapi kontrol pengurutan baris: *Rata-rata IHK*, *Klaster Pola (K-Means)*, atau *Abjad (A-Z)*.
- **Horizontal Ranking Bar Chart**:
  - Peringkat komprehensif 38 provinsi dari indeks terendah ke tertinggi.
  - Penanda batang khusus provinsi sorotan dan garis benchmark rata-rata nasional (*dash line*).
- **Dot Plot Sebaran Distribusi IHK**:
  - Menampilkan kepadatan dispersi nilai provinsi dan titik anomali regional terhadap garis patokan nasional.

### 2. Multivariate Analysis (Reduksi Dimensi & Pola Pengeluaran)
- **PCA Biplot Berbasis 38 Subkelompok Komoditas**:
  - Model reduksi dimensi dilatih menggunakan 38 variabel mikro subkelompok (`df_sub`) untuk presisi analitik optimal.
  - Sumbu PC1 memproksikan polarisasi modernitas konsumsi (furnitur, perlengkapan RT, perawatan pribadi), sedangkan sumbu PC2 memisahkan sandang/tekstil terhadap komoditas pangan pokok.
  - Fitur kontrol tampilan vektor *loadings*: *10 Subkelompok Paling Berpengaruh*, *Seluruh 38 Subkelompok*, atau *Sembunyikan Vektor*.
- **Tabel Detail Loadings PCA**:
  - Menampilkan matriks bobot loadings PC1, PC2, dan magnitudo kontribusi seluruh 38 subkelompok beserta kelompok induknya.
- **Parallel Coordinates (11 Kelompok Pengeluaran)**:
  - Profil visual komparatif melintasi 11 sumbu kebutuhan hidup.
  - Membandingkan profil provinsi fokus (`selected_prov`), provinsi pembanding pilihan pengguna, rata-rata nasional, dan sebaran provinsi lain.

### 3. Network Analysis (Topologi Kemiripan Antarprovinsi)
- **Ringkasan Metrik Jaringan**:
  - Kartu metrik sekunder: *Total Edge Aktif*, *Rata-rata Derajat*, *Jumlah Komponen Terhubung*, dan *Derajat Koneksi Provinsi Fokus*.
- **Force-Directed Graph (Spring Layout)**:
  - Graf fisika pegas interaktif di mana node merepresentasikan provinsi dan edge merepresentasikan hubungan korelasi kuat ($r \ge \text{threshold}$).
  - Ukuran node proporsional terhadap jumlah derajat koneksi; warna node mengikuti hasil klasterisasi K-Means.
  - Penyorotan garis koneksi langsung (*edge brushing*) untuk provinsi fokus.
- **Tampilan Alternatif: Adjacency Matrix**:
  - Ditempatkan persis di bawah graf network untuk memberikan sudut pandang struktural matriks adjacency (`px.imshow`).
  - Menampilkan blok homogenitas intra-klaster dan asimetri keterputusan kawasan timur.
  - Dilengkapi opsi pengurutan berbasis klaster/abjad serta filter ambang batas $r$.
- **Profil Kemiripan & Tabel Pasangan**:
  - Menampilkan daftar 8 provinsi paling serupa (korelasi tertinggi) dan 4 provinsi paling berbeda (korelasi terendah) terhadap provinsi fokus.

### 4. Hierarchical Drill-Down (Struktur Dekomposisi 3 Level)
- **Breadcrumb Navigation**:
  - Menampilkan hierarki navigasi: `Indonesia (Nasional) -> [Provinsi] -> 11 Kelompok -> 38 Subkelompok`.
- **Dua Visualisasi Sunburst Terpisah (3 Level)**:
  - **Sunburst Nasional**: Menggunakan root node statis `Indonesia` dengan jalur `['Root', 'Kelompok', 'Subkelompok']`.
  - **Sunburst Provinsi Terpilih**: Menggunakan root node dinamis sesuai provinsi fokus (`selected_prov`) dengan jalur `['Root', 'Kelompok', 'Subkelompok']`.
  - **Orientasi Teks Horizontal**: Kedua diagram menggunakan parameter `insidetextorientation='horizontal'` agar label dapat dibaca dengan mudah dan cepat tanpa memutar orientasi kognitif.
  - **Pemisahan Variabel Estetik**:
    - Ukuran sektor (`values`): Menggunakan **Bobot Diagram Timbang BPS (%)** (Tahun Dasar 2022 = 100).
    - Warna sektor (`color`): Menggunakan **Nilai Rata-rata IHK 2025** dengan skala kontras `SEQUENTIAL_BURGUNDY_GOLD`.
- **Treemap Chart 3 Level**:
  - Representasi proporsi luas kotak spasial berbasis bobot pengeluaran dan rona warna IHK dengan kemampuan *zoom-in/zoom-out*.

---

## Desain UI/UX & Kepatuhan Rubrik

1. **Tema Desain Editorial Glassmorphic**:
   - Latar belakang gradien Deep Burgundy (`#3B0A13` ke `#4A0D18`) dipadukan dengan kartu KPI Warm Cream (`#FDF5EC`) dan aksen Amber Gold (`#F5D6A8`).
2. **Sticky STIS Header**:
   - Header bagian atas menetap saat halaman digulir (*sticky*), memuat logo resmi Politeknik Statistika STIS dan lencana identitas mahasiswa (Nama, NIM, Kelas).
3. **Responsivitas Perangkat Mobile (*Mobile-Friendly*)**:
   - Dilengkapi CSS `@media screen and (max-width: 768px)`:
     - Header otomatis beralih ke tata letak vertikal (*stacking*) dengan padding khusus tombol sidebar.
     - Tab navigasi atas menjadi *scrollable* horizontal tanpa teks terpotong atau bertumpuk (`white-space: nowrap !important; overflow-x: auto !important`).
4. **Interaktivitas Global (*Brushing & Linking*)**:
   - Pilihan provinsi pada dropdown sidebar secara instan memperbarui dan menyorot (*highlight*) data di seluruh visualisasi: Peta, Heatmap, Ranking, Dot Plot, PCA Biplot, Parallel Coordinates, Graf Network, dan Sunburst/Treemap Provinsi.
5. **Ekspor Data Mandiri**:
   - Setiap visualisasi dilengkapi tombol unduh file CSV terpisah di bagian kiri bawah chart.
6. **Integritas Akademis & Standar Formal**:
   - Antarmuka visual bersih dari emotikon informal pada badan chart.
   - Seluruh visualisasi mencantumkan atribusi sumber resmi:  
     `Sumber: Badan Pusat Statistik (BPS) - Indeks Harga Konsumen 2025`.

---

## Struktur Direktori Proyek

```text
UAS-VISDAT/
│
├── app.py                               # Skrip utama aplikasi Streamlit dashboard
├── Preprocessing.py                     # Skrip pembersihan, imputasi, dan standardisasi data
├── requirements.txt                     # Daftar pustaka dependensi Python
├── README.md                            # Dokumentasi lengkap proyek
├── logo stis.png                        # Asset logo resmi Politeknik Statistika STIS
├── indonesia-38-provinces.geojson       # Data spasial batas poligon 38 provinsi Indonesia
├── IHK_38_Provinsi_2025_Cleaned.xlsx    # Data tabular hasil cleaning awal dari BPS
│
├── hasil_preprocessing_IHK/             # Folder output data hasil tahapan preprocessing
│   ├── 00_kamus_hierarki.csv            # Kamus hierarki kelompok dan subkelompok
│   ├── 01_data_asli.csv                 # Data mentah sebelum imputasi (38 prov x 38 sub)
│   ├── 02_data_imputed.csv              # Data hasil imputasi median per variabel
│   ├── 03_data_standardized.csv         # Data hasil transformasi Z-score (StandardScaler)
│   ├── 04_hierarchy_long.csv            # Format long untuk visualisasi hierarki Sunburst & Treemap
│   ├── 05_flag_imputasi.csv             # Audit flag biner data yang diimputasi
│   ├── 06_audit_missing.csv             # Laporan ringkasan persentase missing value
│   ├── 07_kamus_variabel.csv            # Kamus relasi 11 kelompok ke 38 subkelompok
│   └── IHK_38_Provinsi_2025_Preprocessed.xlsx  # Rekapitulasi seluruh sheet hasil preprocessing
│
└── .streamlit/
    └── config.toml                      # Konfigurasi server Streamlit
```

---

## Instalasi & Cara Menjalankan

### 1. Prasyarat Sistem
- Python versi **3.10** atau lebih baru.
- Peramban web modern (Google Chrome, Mozilla Firefox, Microsoft Edge, atau Safari).

### 2. Kloning atau Unduh Repositori
Buka terminal / PowerShell dan arahkan ke direktori proyek:
```bash
cd "D:/SEM 6/VISDAT/UAS"
```

### 3. Buat dan Aktifkan Virtual Environment (Opsional namun Disarankan)
```bash
# Membuat virtual environment
python -m venv .venv

# Aktivasi di Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Aktivasi di Linux / macOS
source .venv/bin/activate
```

### 4. Instalasi Dependensi
Instal seluruh pustaka yang tercantum pada `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 5. Jalankan Aplikasi Streamlit
Jalankan server aplikasi lokal:
```bash
streamlit run app.py
```
Setelah perintah dijalankan, peramban web akan terbuka secara otomatis di alamat:  
`http://localhost:8501`

---

## Pipeline Preprocessing Data (`Preprocessing.py`)

Proses penyiapan data dijalankan melalui tahapan metodologis terstruktur:
1. **Pembersihan Entitas Wilayah**: Standardisasi penamaan 38 provinsi di Indonesia agar sinkron dengan GeoJSON.
2. **Audit & Penanganan Missing Value**:
   - Variabel dengan persentase missing > 50% dieliminasi untuk menjaga validitas statistik (misalnya *Minuman Beralkohol*, *Asuransi*, *Barang Rekreasi Tahan Lama*, *Perlengkapan Kebudayaan*).
   - Menghasilkan 38 subkelompok komoditas valid di bawah 11 kelompok pengeluaran.
3. **Imputasi Nilai Hilang**: Menggunakan *Median Imputation* pada data level subkelompok (`02_data_imputed.csv`).
4. **Standardisasi Data**: Penskalaan fitur menggunakan `StandardScaler` (Z-score standardisation) untuk kebutuhan reduksi dimensi PCA dan klasterisasi K-Means (`03_data_standardized.csv`).
5. **Restrukturisasi Hierarki**: Transformasi data dari format lebar (*wide*) ke format panjang (*long*) untuk visualisasi konsentris Sunburst dan Treemap (`04_hierarchy_long.csv`).

---

## Temuan Utama & Kesimpulan Riset

1. **Pola Harga Antarprovinsi Tidak Seragam (Hasil PCA 38 Subkelompok)**:  
   Variasi harga di Indonesia terbagi ke dalam dua dimensi dominan: sumbu PC1 digerakkan oleh modernitas dan kebutuhan rumah tangga perkotaan, sedangkan PC2 merefleksikan disparitas harga sandang dan komoditas pangan pokok primer.
2. **Kedekatan Pola Tidak Mutlak Dibatasi Geografis**:  
   Pasangan provinsi dengan koefisien korelasi pola konsumsi tertinggi adalah **DI Yogyakarta dan Sulawesi Selatan ($r = 0,988$)**, disusul **NTB dan Sumatera Selatan ($r = 0,985$)** serta **Jawa Barat dan Jawa Timur ($r = 0,985$)**, membuktikan integrasi pola konsumsi perkotaan lintas pulau.
3. **Topologi Jaringan Mengungkap Keterputusan Kawasan Timur**:  
   Pada ambang batas korelasi standar $r \ge 0,80$, sebanyak 23 provinsi membentuk satu komponen raksasa (*giant component*), sementara provinsi di kawasan Papua (**Papua Tengah, Papua Pegunungan, Papua**) dan **Maluku Utara** terisolasi akibat tingginya biaya pasok logistik dan struktur pasar kepulauan.
4. **Disparitas Makro Berakar dari Komoditas Spesifik**:  
   Dekomposisi Sunburst dan Treemap 3 level menunjukkan bahwa lonjakan indeks provinsi terutama disumbangkan oleh kelompok **Makanan, Minuman & Tembakau** (bobot 33,68%) khususnya subkelompok *Makanan Pokok / Padi-padian*, *Rokok & Tembakau*, serta disparitas tarif utilitas lokal *Penyediaan Air Bersih*.

---

## Sumber Data & Referensi
- **Badan Pusat Statistik (BPS)**: Publikasi *Indeks Harga Konsumen 38 Provinsi di Indonesia 2025 (Tahun Dasar 2022 = 100)*.
- **Katalog BPS**: Hasil Survei Biaya Hidup (SBH) 2022 untuk Diagram Timbang Komoditas IHK.
- **Politeknik Statistika STIS**: Modul Praktikum Visualisasi Data (VISDAT) 2025/2026.
