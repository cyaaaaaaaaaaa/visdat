import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import base64
import json

# ==============================================================================
# 0. PEMUATAN LOGO STIS
# ==============================================================================
logo_path = Path(__file__).parent / "logo stis.png"
if logo_path.exists():
    with open(logo_path, "rb") as _f:
        logo_stis_b64 = base64.b64encode(_f.read()).decode("utf-8")
else:
    logo_stis_b64 = ""

# ==============================================================================
# 1. KONFIGURASI HALAMAN & TEMA DESAIN (DEEP BURGUNDY & WARM CREAM)
# ==============================================================================
st.set_page_config(
    page_title="Indeks Harga Konsumen 38 Provinsi 2025",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Deep Burgundy Glassmorphic Editorial)
# Menggunakan kustomisasi CSS (unsafe_allow_html=True) sesuai instruksi revisi UI
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5, .brand-title {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: -0.02em;
}

/* 1. Menyembunyikan header default Streamlit */
header, [data-testid="stHeader"] {
    visibility: hidden !important;
    height: 0px !important;
}

/* Main Page Background */
.stApp {
    background: linear-gradient(135deg, #3B0A13 0%, #4A0D18 100%);
    color: #FDF5EC;
}

/* 1. Mengurangi padding atas bawaan Streamlit agar pas di bawah sticky header */
div.block-container, .main .block-container, [data-testid="stMainBlockContainer"] {
    max-width: 100% !important;
    padding-top: 5.2rem !important;
    padding-bottom: 3.5rem !important;
    padding-left: 2.2rem !important;
    padding-right: 2.2rem !important;
}

/* Memastikan kontrol tombol buka/tutup sidebar tetap terlihat di atas sticky header */
[data-testid="stSidebarCollapsedControl"] {
    visibility: visible !important;
    z-index: 1000001 !important;
    top: 10px !important;
}

/* ==============================================================================
   STICKY HEADER ATAS (LOGO STIS & DATA DIRI MAHASISWA - MENETAP SAAT SCROLL)
   ============================================================================== */
.sticky-stis-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 56px;
    background: rgba(35, 7, 13, 0.95);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(253, 245, 236, 0.18);
    box-shadow: 0 4px 22px rgba(0, 0, 0, 0.5);
    z-index: 999990;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 32px 0 54px;
    box-sizing: border-box;
    font-family: 'Inter', sans-serif;
}

.sticky-header-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.stis-logo-img {
    height: 38px;
    width: auto;
    object-fit: contain;
    filter: drop-shadow(0 2px 5px rgba(0, 0, 0, 0.5));
}

.stis-titles {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.stis-inst {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.82rem;
    font-weight: 800;
    color: #FDF5EC;
    letter-spacing: 0.8px;
    line-height: 1.15;
}

.stis-sub {
    font-size: 0.68rem;
    color: #E8908A;
    font-weight: 500;
    letter-spacing: 0.3px;
}

.sticky-header-right {
    display: flex;
    align-items: center;
}

.identity-badge {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(253, 245, 236, 0.08);
    border: 1px solid rgba(253, 245, 236, 0.22);
    border-radius: 24px;
    padding: 6px 16px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.badge-item {
    font-size: 0.82rem;
    color: #FDF5EC;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.badge-item strong {
    font-weight: 700;
    color: #FDF5EC;
}

.badge-item.name strong {
    color: #F5D6A8;
}

.badge-divider {
    color: #8C4E58;
    font-size: 0.75rem;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #2D070E;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4);
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #FDF5EC !important;
}

[data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
    color: #FDF5EC !important;
}

/* KPI Card (Warm Cream / Off-White #FDF5EC) */
.kpi-card {
    background-color: #FDF5EC;
    border-radius: 14px;
    padding: 20px 22px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(253, 245, 236, 0.2);
    margin-bottom: 22px;
    box-sizing: border-box;
}

.kpi-title {
    font-size: 0.74rem;
    font-weight: 700;
    color: #8C4E58;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
    font-family: 'Inter', sans-serif;
}

.kpi-value {
    font-size: 2.1rem;
    font-weight: 800;
    color: #2A0A10;
    line-height: 1.1;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.kpi-sub {
    font-size: 0.76rem;
    color: #8C4E58;
    margin-top: 5px;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
}

/* Styling Container Border Bawaan Streamlit menjadi Glassmorphic Card Penuh */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.045) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
    margin-bottom: 26px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.28) !important;
    width: 100% !important;
}

/* Full Width untuk Plotly Chart dan Dataframe */
[data-testid="stPlotlyChart"], [data-testid="stDataFrame"], .stPlotlyChart {
    width: 100% !important;
}

/* ==============================================================================
   TAB NAVIGASI FULL-WIDTH & RATA TENGAH (PROPORSIONAL 25% PER TAB)
   ============================================================================== */
/* Menargetkan container utama tab Streamlit */
div[data-testid="stTabs"] {
    width: 100% !important;
}

/* Container tablist membentang 100% dari kiri ke kanan */
div[data-testid="stTabs"] [role="tablist"],
div[data-baseweb="tab-list"],
[data-baseweb="tab-list"],
div[data-testid="stTabs"] > div:first-child {
    display: flex !important;
    width: 100% !important;
    max-width: 100% !important;
    justify-content: space-between !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.15) !important;
    gap: 0px !important;
    margin-bottom: 26px !important;
}

/* Memaksa setiap tombol tab untuk merentang dan membagi ruang secara rata (proporsional 25% per tab) */
div[data-testid="stTabs"] button[data-baseweb="tab"],
div[data-testid="stTabs"] div[data-baseweb="tab"],
div[data-testid="stTabs"] button[data-testid="stTab"],
div[data-testid="stTabs"] div[data-testid="stTab"],
div[data-testid="stTabs"] [data-testid="stTab"],
div[data-testid="stTabs"] [role="tab"],
div[data-baseweb="tab"],
button[data-baseweb="tab"],
[data-baseweb="tab"] {
    flex: 1 1 0% !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    text-align: center !important;
    padding-left: 0px !important;
    padding-right: 0px !important;
    padding-top: 14px !important;
    padding-bottom: 14px !important;
    background-color: transparent !important;
    border: none !important;
    color: #FDF5EC !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    opacity: 0.70;
    transition: all 0.2s ease-in-out;
    font-family: 'Inter', sans-serif !important;
}

/* Memastikan elemen teks di dalam tombol tab juga berada di tengah */
div[data-testid="stTabs"] button[data-baseweb="tab"] div,
div[data-testid="stTabs"] button[data-baseweb="tab"] p,
div[data-testid="stTabs"] button[data-baseweb="tab"] span,
div[data-testid="stTabs"] div[data-baseweb="tab"] div,
div[data-testid="stTabs"] div[data-baseweb="tab"] p,
div[data-testid="stTabs"] div[data-baseweb="tab"] span,
div[data-testid="stTabs"] [data-testid="stTab"] div,
div[data-testid="stTabs"] [data-testid="stTab"] p,
div[data-testid="stTabs"] [data-testid="stTab"] span,
div[data-testid="stTabs"] [role="tab"] div,
div[data-testid="stTabs"] [role="tab"] p,
div[data-testid="stTabs"] [role="tab"] span,
div[data-testid="stTabs"] [data-testid="stMarkdownContainer"],
div[data-baseweb="tab"] div,
div[data-baseweb="tab"] p,
div[data-baseweb="tab"] span,
button[data-baseweb="tab"] div,
button[data-baseweb="tab"] p,
button[data-baseweb="tab"] span {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    text-align: center !important;
    width: 100% !important;
    margin: 0 auto !important;
}

div[data-testid="stTabs"] button[data-baseweb="tab"]:hover,
div[data-testid="stTabs"] [data-testid="stTab"]:hover,
div[data-baseweb="tab"]:hover,
button[data-baseweb="tab"]:hover {
    opacity: 1 !important;
    color: #F5D6A8 !important;
    background-color: rgba(255, 255, 255, 0.04) !important;
}

div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"],
div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"],
div[data-testid="stTabs"] [data-testid="stTab"][data-selected="true"],
div[data-testid="stTabs"] [role="tab"][aria-selected="true"],
div[data-baseweb="tab"][aria-selected="true"],
button[data-baseweb="tab"][aria-selected="true"] {
    opacity: 1 !important;
    color: #FDF5EC !important;
    border-bottom: 3.5px solid #E8908A !important;
    background-color: rgba(255, 255, 255, 0.06) !important;
    border-radius: 8px 8px 0 0 !important;
}

div[data-baseweb="tab-highlight"] {
    background-color: #E8908A !important;
}

/* Styling Tombol Unduh Data (di bawah kiri visualisasi) */
.stDownloadButton {
    display: flex;
    justify-content: flex-start;
    margin-top: 6px;
    margin-bottom: 4px;
}

.stDownloadButton > button {
    background-color: rgba(253, 245, 236, 0.08) !important;
    color: #FDF5EC !important;
    border: 1px solid rgba(253, 245, 236, 0.28) !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 6px 14px !important;
    transition: all 0.2s ease-in-out !important;
    font-family: 'Inter', sans-serif !important;
}

.stDownloadButton > button:hover {
    background-color: #FDF5EC !important;
    color: #2A0A10 !important;
    border-color: #FDF5EC !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35) !important;
}

/* Form controls styling */
.stSelectbox label, .stSlider label, .stRadio label, .stMultiSelect label {
    color: #FDF5EC !important;
    font-weight: 600;
}

/* ==============================================================================
   RESPONSIVITAS UNTUK LAYAR HP (MOBILE-FRIENDLY DEVICES)
   ============================================================================== */
@media screen and (max-width: 768px) {
    /* Menyesuaikan padding utama agar tidak memakan ruang di layar kecil */
    div.block-container, .main .block-container, [data-testid="stMainBlockContainer"] {
        padding-top: 7rem !important; /* Memberi ruang lebih untuk header yang menumpuk di HP */
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Mengubah susunan Sticky Header menjadi atas-bawah (stacking) */
    .sticky-stis-header {
        flex-direction: column;
        height: auto;
        padding: 10px 15px 10px 45px; /* Sisakan ruang 45px di kiri untuk tombol sidebar */
        align-items: flex-start;
        gap: 8px;
    }

    /* Memperkecil teks di header agar tidak bertabrakan */
    .stis-inst { font-size: 0.75rem; }
    .stis-sub { font-size: 0.6rem; }
    
    .identity-badge {
        padding: 4px 10px;
        flex-wrap: wrap;
    }
    .badge-item { font-size: 0.7rem; }

    /* Memperkecil ukuran font pada KPI Card */
    .kpi-value { font-size: 1.6rem; }

    /* Memastikan Tab Navigasi bisa digeser ke kanan-kiri (scrollable) di HP */
    div[data-testid="stTabs"] [role="tablist"] {
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        justify-content: flex-start !important;
        padding-bottom: 5px;
    }
    
    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        flex: 0 0 auto !important;
        padding-left: 15px !important;
        padding-right: 15px !important;
    }
}
</style>""", unsafe_allow_html=True)

# Render Sticky STIS Header (Menetap di bagian atas saat di-scroll)
st.markdown(f"""
<div class="sticky-stis-header">
    <div class="sticky-header-left">
        <img src="data:image/png;base64,{logo_stis_b64}" class="stis-logo-img" alt="Logo Politeknik Statistika STIS" />
        <div class="stis-titles">
            <span class="stis-inst">POLITEKNIK STATISTIKA STIS</span>
            <span class="stis-sub">Visualisasi Data (VISDAT) · Proyek Akhir</span>
        </div>
    </div>
    <div class="sticky-header-right">
        <div class="identity-badge">
            <span class="badge-item name"><span class="badge-icon">👤</span> <strong>Syadza Khumairah Akmul</strong></span>
            <span class="badge-divider">•</span>
            <span class="badge-item nim"><span class="badge-icon">🆔</span> <strong>222313387</strong></span>
            <span class="badge-divider">•</span>
            <span class="badge-item kelas"><span class="badge-icon">🏛️</span> <strong>3SD1</strong></span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. DEFINISI PALET WARNA CHART PLOTLY & KOORDINAT SPASIAL
# ==============================================================================
CHART_COLORWAY = ['#E8908A', '#F5D6A8', '#A82C3E', '#7A2332', '#DDA07F', '#C97282']

# Skala warna kontinyu untuk Peta, Heatmap, Sunburst, Treemap (Kontras Tajam Mengikuti Sebaran IHK)
SEQUENTIAL_BURGUNDY_GOLD = [
    [0.0, "#FFF9F0"],   # Cream Terang Cerah (IHK Terendah ~105.0)
    [0.25, "#FAD586"],  # Warm Amber Gold (IHK Rendah ~106.2)
    [0.50, "#F39C6B"],  # Sunset Coral (IHK Median ~107.4)
    [0.75, "#D93856"],  # Vivid Ruby Crimson (IHK Tinggi ~108.5)
    [1.0, "#8B0A26"]    # Deep Rich Ruby Red (IHK Tertinggi ~110.6)
]

CLUSTER_COLOR_MAP = {
    'Klaster 1': '#E8908A',  # Muted Peach
    'Klaster 2': '#F5D6A8',  # Warm Gold
    'Klaster 3': '#A82C3E',  # Rich Crimson
    'Klaster 4': '#DDA07F',  # Coral
    'Klaster 5': '#C97282',  # Berry Pink
    'Klaster 6': '#7A2332'   # Wine
}

# Koordinat Sentroid 38 Provinsi Indonesia (Untuk Peta Choropleth & Peta Simbol Proporsional)
PROVINCE_COORDS = {
    'Aceh': {'lat': 4.6951, 'lon': 96.7494},
    'Sumatera Utara': {'lat': 2.1154, 'lon': 99.5451},
    'Sumatera Barat': {'lat': -0.7399, 'lon': 100.8000},
    'Riau': {'lat': 0.2933, 'lon': 101.7068},
    'Jambi': {'lat': -1.6101, 'lon': 103.6131},
    'Sumatera Selatan': {'lat': -3.3194, 'lon': 104.9144},
    'Bengkulu': {'lat': -3.5778, 'lon': 102.3464},
    'Lampung': {'lat': -4.5586, 'lon': 105.4068},
    'Kepulauan Bangka Belitung': {'lat': -2.7411, 'lon': 106.4406},
    'Kepulauan Riau': {'lat': 3.9456, 'lon': 108.1428},
    'Dki Jakarta': {'lat': -6.2088, 'lon': 106.8456},
    'Jawa Barat': {'lat': -6.9147, 'lon': 107.6098},
    'Jawa Tengah': {'lat': -7.1510, 'lon': 110.1403},
    'Di Yogyakarta': {'lat': -7.7956, 'lon': 110.3695},
    'Jawa Timur': {'lat': -7.5361, 'lon': 112.2384},
    'Banten': {'lat': -6.4058, 'lon': 106.0640},
    'Bali': {'lat': -8.4095, 'lon': 115.1889},
    'Nusa Tenggara Barat': {'lat': -8.6529, 'lon': 117.3616},
    'Nusa Tenggara Timur': {'lat': -8.6574, 'lon': 121.0794},
    'Kalimantan Barat': {'lat': -0.2787, 'lon': 111.4753},
    'Kalimantan Tengah': {'lat': -1.6815, 'lon': 113.3824},
    'Kalimantan Selatan': {'lat': -3.0926, 'lon': 115.2838},
    'Kalimantan Timur': {'lat': 0.5387, 'lon': 116.4194},
    'Kalimantan Utara': {'lat': 3.0731, 'lon': 116.0414},
    'Sulawesi Utara': {'lat': 0.6247, 'lon': 123.9750},
    'Sulawesi Tengah': {'lat': -1.4300, 'lon': 121.4456},
    'Sulawesi Selatan': {'lat': -3.6687, 'lon': 119.9740},
    'Sulawesi Tenggara': {'lat': -4.1449, 'lon': 122.1746},
    'Gorontalo': {'lat': 0.6999, 'lon': 122.4467},
    'Sulawesi Barat': {'lat': -2.8441, 'lon': 119.2321},
    'Maluku': {'lat': -3.2385, 'lon': 130.1453},
    'Maluku Utara': {'lat': 1.5709, 'lon': 127.8088},
    'Papua Barat': {'lat': -1.3361, 'lon': 133.1747},
    'Papua Barat Daya': {'lat': -0.8753, 'lon': 131.2558},
    'Papua': {'lat': -4.2699, 'lon': 138.0804},
    'Papua Selatan': {'lat': -7.5000, 'lon': 139.5000},
    'Papua Tengah': {'lat': -3.6000, 'lon': 136.5000},
    'Papua Pegunungan': {'lat': -4.1000, 'lon': 139.0000}
}

# Bobot Diagram Timbang BPS (Tahun Dasar 2022=100) untuk 38 Subkelompok Komoditas
# Digunakan sebagai variabel ukuran (values) pada visualisasi hirarki (Sunburst & Treemap)
BPS_SUB_WEIGHTS = {
    'Makanan': 25.20, 'Minuman yang Tidak Beralkohol': 3.80, 'Rokok dan Tembakau': 4.68,
    'Pakaian': 3.80, 'Alas Kaki': 1.60,
    'Sewa dan Kontrak Rumah': 5.50, 'Pemeliharaan, Perbaikan dan Keamanan': 2.80,
    'Penyediaan Air dan Layanan Perumahan Lainnya': 2.10, 'Listrik dan Bahan Bakar Rumah Tangga': 4.80,
    'Furnitur, Perlengkapan dan Karpet': 1.20, 'Tekstil Rumah Tangga': 0.60,
    'Peralatan Rumah Tangga': 0.90, 'Barang Pecah Belah dan Peralatan Makan Minum': 0.40,
    'Peralatan dan Perlengkapan Perumahan dan Kebun': 0.40, 'Barang dan Layanan untuk Pemeliharaan Rumah Tangga Rutin': 1.30,
    'Obat-obatan dan Produk Kesehatan': 1.10, 'Jasa Rawat Jalan': 0.80, 'Jasa Rawat Inap': 0.50, 'Jasa Kesehatan Lainnya': 0.40,
    'Pembelian Kendaraan': 3.80, 'Pengoperasian Peralatan Transportasi Pribadi': 4.60, 'Jasa Angkutan Penumpang': 3.00, 'Jasa Pengiriman Barang': 0.50,
    'Peralatan Informasi dan Komunikasi': 1.40, 'Layanan Informasi dan Komunikasi': 3.40, 'Jasa Keuangan': 0.80,
    'Barang Rekreasi Lainnya dan Olahraga': 0.50, 'Layanan Rekreasi dan Olahraga': 0.50, 'Layanan Kebudayaan': 0.40, 'Koran, Buku dan Perlengkapan Sekolah': 0.50,
    'Pendidikan Dasar dan Anak Usia Dini': 1.20, 'Pendidikan Menengah': 1.30, 'Pendidikan Tinggi': 1.30, 'Pendidikan Lainnya': 0.50,
    'Jasa Pelayanan Makanan dan Minuman': 8.80,
    'Perawatan Pribadi': 3.40, 'Perawatan Pribadi Lainnya': 1.42, 'Jasa Lainnya': 0.80
}


# ==============================================================================
# 3. HELPER FUNCTIONS UNTUK RENDERING UI MURNI (ANTI-BOCOR KODE)
# ==============================================================================
def render_kpi(col, label, value, subtext=""):
    """Merender kartu KPI warna krem menggunakan st.html murni (Khusus 4 KPI Utama)."""
    sub_tag = f'<div class="kpi-sub">{subtext}</div>' if subtext else ''
    col.html(f'''<div class="kpi-card">
        <div class="kpi-title">{label}</div>
        <div class="kpi-value">{value}</div>
        {sub_tag}
    </div>''')

def render_secondary_metric(col, label, value, subtext=""):
    """Merender kartu metrik sekunder ramping dan transparan untuk tab Network Analysis."""
    sub_tag = f'<div style="font-family: \'Inter\', sans-serif; font-size: 0.73rem; color: rgba(253, 245, 236, 0.7); margin-top: 3px; font-weight: 500;">{subtext}</div>' if subtext else ''
    col.markdown(f"""<div style="background-color: rgba(253, 245, 236, 0.05); border: 1px solid rgba(253, 245, 236, 0.2); border-radius: 8px; padding: 10px 15px; margin-bottom: 20px; box-sizing: border-box;">
<div style="font-family: 'Inter', sans-serif; font-size: 0.72rem; font-weight: 700; color: #E8908A; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 3px;">{label}</div>
<div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.55rem; font-weight: 800; color: #FDF5EC; line-height: 1.15;">{value}</div>
{sub_tag}
</div>""", unsafe_allow_html=True)

def render_section_header(title, subtitle=""):
    """Merender judul seksi visualisasi dengan tipografi editorial."""
    sub_tag = f'<div style="font-family: \'Inter\', sans-serif; font-size: 0.9rem; color: #E8908A; line-height: 1.5; margin-top: 4px;">{subtitle}</div>' if subtitle else ''
    st.html(f'''<div style="margin-top: 8px; margin-bottom: 16px;">
        <div style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 1.32rem; font-weight: 700; color: #FDF5EC; letter-spacing: -0.02em;">{title}</div>
        {sub_tag}
    </div>''')

def render_takeaway(title, text):
    """Merender kotak insight/kesimpulan ringkas untuk setiap sub-judul visualisasi."""
    st.html(f'''<div style="background: rgba(255, 255, 255, 0.035); border-left: 3.5px solid #F5D6A8; border-radius: 0 8px 8px 0; padding: 12px 18px; margin-top: 14px; margin-bottom: 6px;">
        <span style="font-family: \'Plus Jakarta Sans\', sans-serif; font-weight: 700; color: #F5D6A8; font-size: 0.94rem; margin-right: 6px;">📌 Insight Sub-Judul: {title} —</span>
        <span style="font-family: \'Inter\', sans-serif; font-size: 0.91rem; color: #FDF5EC; line-height: 1.6;">{text}</span>
    </div>''')

def render_source_caption():
    """Merender atribusi sumber data BPS resmi di bawah setiap visualisasi sesuai rubrik ujian."""
    st.caption("Sumber: Badan Pusat Statistik (BPS) - Indeks Harga Konsumen 2025")

def render_download_button(df, filename, label="📥 Unduh Data (CSV)", key=None):
    """Merender tombol unduh CSV di bawah kiri visualisasi dengan styling rapi."""
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    col_dl, col_space = st.columns([1.5, 3.5])
    with col_dl:
        st.download_button(
            label=label,
            data=csv_bytes,
            file_name=filename,
            mime="text/csv",
            key=key,
            use_container_width=True
        )

def render_conclusion_card(title, subtitle, items):
    """Merender kartu kesimpulan/takeaway secara utuh menggunakan st.html murni tanpa resiko bocor kode."""
    items_html = "".join([
        f'''<div style="background: rgba(255, 255, 255, 0.04); border-left: 4px solid #E8908A; border-radius: 0 10px 10px 0; padding: 16px 20px; margin-bottom: 14px;">
            <div style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 1.05rem; font-weight: 700; color: #F5D6A8; margin-bottom: 6px;">{item["title"]}</div>
            <div style="font-family: \'Inter\', sans-serif; font-size: 0.93rem; color: #FDF5EC; line-height: 1.65;">{item["desc"]}</div>
        </div>'''
        for item in items
    ])
    st.html(f'''<div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.12); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border-radius: 16px; padding: 26px 30px; margin-top: 24px; margin-bottom: 24px; box-shadow: 0 10px 32px rgba(0, 0, 0, 0.35); width: 100%; box-sizing: border-box;">
        <div style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 1.35rem; font-weight: 800; color: #FDF5EC; margin-bottom: 4px;">{title}</div>
        <div style="font-family: \'Inter\', sans-serif; font-size: 0.94rem; color: #E8908A; margin-bottom: 20px;">{subtitle}</div>
        {items_html}
    </div>''')


# ==============================================================================
# 4. LOAD & PREPARE REAL DATA (BPS 2025)
# ==============================================================================
@st.cache_data
def load_all_data():
    base_dir = Path(__file__).resolve().parent
    
    # Deteksi otomatis folder data: prioritas hasil_preprocessing_IHK atau data
    data_dir = base_dir / "hasil_preprocessing_IHK"
    if not data_dir.exists():
        data_dir = base_dir / "data"
    if not data_dir.exists():
        data_dir = base_dir
    
    df_hier = pd.read_csv(data_dir / "04_hierarchy_long.csv")
    df_sub = pd.read_csv(data_dir / "02_data_imputed.csv", index_col=0)
    
    # Deteksi nama file kamus variabel/hierarki
    kamus_path = data_dir / "07_kamus_variabel.csv"
    if not kamus_path.exists():
        kamus_path = data_dir / "00_kamus_hierarki.csv"
    df_kamus = pd.read_csv(kamus_path)
    
    # Poin Perbaikan 1: Tambahkan root node konstan 'Indonesia' dan bobot pengeluaran
    df_hier['Indonesia'] = 'Indonesia'
    df_hier['Bobot_Pengeluaran'] = df_hier['Subkelompok'].map(BPS_SUB_WEIGHTS).fillna(1.0)
    
    kel_pivot = df_hier.groupby(['Provinsi', 'Kelompok'])['IHK_RataRata_2025'].mean().unstack()
    sub_to_kel = dict(zip(df_kamus['Subkelompok'], df_kamus['Kelompok']))
    
    return df_hier, df_sub, kel_pivot, df_kamus, sub_to_kel

df_hier, df_sub, df_kelompok, df_kamus, sub_to_kel = load_all_data()
all_provinces = sorted(df_kelompok.index.tolist())
all_kelompok = sorted(df_kelompok.columns.tolist())

@st.cache_data
def load_geojson():
    base_dir = Path(__file__).resolve().parent
    geo_path = base_dir / "indonesia-38-provinces.geojson"
    if not geo_path.exists():
        geo_path = base_dir / "data" / "indonesia-38-provinces.geojson"
    if not geo_path.exists():
        geo_path = base_dir / "hasil_preprocessing_IHK" / "indonesia-38-provinces.geojson"
    with open(geo_path, "r", encoding="utf-8") as _f:
        return json.load(_f)

geojson_data = load_geojson()


# ==============================================================================
# 5. SIDEBAR: KONTROL DAN FILTER INTERAKTIF
# ==============================================================================
with st.sidebar:
    st.image("https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/chart-line.svg", width=34)
    st.markdown("## 🧭 Navigasi & Filter")
    st.caption("Pola IHK 38 Provinsi di Indonesia · BPS 2025")
    st.markdown("---")
    
    default_index = all_provinces.index("Sulawesi Selatan") if "Sulawesi Selatan" in all_provinces else 0
    selected_prov = st.selectbox(
        "🎯 Provinsi Sorotan (Fokus Brushing):",
        options=all_provinces,
        index=default_index,
        help="Provinsi ini akan otomatis di-highlight pada Peta, Ranking, PCA, Parallel Coordinates, Heatmap, Network, dan Hierarki!"
    )
    st.session_state['selected_province'] = selected_prov
    
    st.markdown("---")
    st.markdown("### ⚙️ Parameter Model")
    
    n_clusters = st.slider("Jumlah Klaster Pola (K-Means):", min_value=2, max_value=6, value=4, step=1)
    
    network_threshold = st.slider(
        "🔗 Ambang Batas Network (r):",
        min_value=0.50,
        max_value=0.95,
        value=0.80,
        step=0.02,
        help="Hanya hubungan antarprovinsi dengan koefisien korelasi ≥ r yang akan ditampilkan sebagai edge."
    )
    
    st.markdown("---")
    st.info("💡 **Petunjuk:** Setiap visualisasi ditampilkan dalam layout penuh (full-width) dari kiri ke kanan. Visualisasi interaktif mendukung hover, zoom, dan seleksi.")


# ==============================================================================
# 6. PERHITUNGAN STATISTIK & MACHINE LEARNING (OPTIMALISASI MULTIVARIAT 38 SUBKELOMPOK)
# ==============================================================================
# Sesuai rubrik evaluasi kriteria wajib multivariat (Poin Perbaikan 4):
# Penskalaan (StandardScaler), reduksi dimensi (PCA), dan iterasi K-Means
# dialihkan menggunakan dataset df_sub (38 variabel subkelompok) untuk presisi maksimal.
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_sub)

pca = PCA(n_components=2)
pca_coords = pca.fit_transform(X_scaled)
var_exp = pca.explained_variance_ratio_

kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)

df_pca = pd.DataFrame({
    'Provinsi': df_sub.index,
    'PC1': pca_coords[:, 0],
    'PC2': pca_coords[:, 1],
    'Cluster': [f"Klaster {c+1}" for c in cluster_labels]
}).set_index('Provinsi')

# Matriks korelasi antarprovinsi dihitung berbasis 38 variabel subkelompok
corr_matrix = df_sub.T.corr()

G = nx.Graph()
for p in all_provinces:
    G.add_node(p, cluster=df_pca.loc[p, 'Cluster'])

for i, p1 in enumerate(all_provinces):
    for j, p2 in enumerate(all_provinces):
        if j > i:
            r = corr_matrix.loc[p1, p2]
            if r >= network_threshold:
                G.add_edge(p1, p2, weight=r)

pos = nx.spring_layout(G, seed=42, k=0.38, iterations=60)
node_degrees = dict(G.degree())

prov_mean_series = df_kelompok.mean(axis=1).sort_values(ascending=False)
highest_prov = prov_mean_series.index[0]
highest_prov_val = prov_mean_series.iloc[0]
lowest_prov = prov_mean_series.index[-1]
lowest_prov_val = prov_mean_series.iloc[-1]
mean_ihk_nasional = prov_mean_series.mean()


# ==============================================================================
# 7. HEADER & TOP KPI CARDS (ROW 1 - WARM CREAM CARDS)
# ==============================================================================
st.markdown("""<div style="text-align: center; margin-bottom: 30px; margin-top: 5px;">
<h1 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2.75rem; font-weight: 800; color: #FDF5EC; letter-spacing: -0.025em; line-height: 1.22; margin: 0 0 10px 0;">
Pola Indeks Harga Konsumen (IHK) Antarprovinsi di Indonesia
</h1>
<p style="font-family: 'Inter', sans-serif; font-size: 1.1rem; color: #E8908A; font-weight: 500; margin: 0; letter-spacing: 0.3px;">
Dashboard Analisis Multivariat, Jaringan Kemiripan & Struktur Hierarki 38 Provinsi · Wilayah Analisis : Sulawesi Selatan
</p>
</div>""", unsafe_allow_html=True)

kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)
render_kpi(kpi_c1, "IHK INDONESIA (RATA-RATA)", f"{mean_ihk_nasional:.2f}".replace('.', ','), "Tahun Dasar 2022 = 100")
render_kpi(kpi_c2, "IHK TERTINGGI (PAPUA TENGAH)", f"{highest_prov_val:.2f}".replace('.', ','), "Disparitas Sektoral Tertinggi")
render_kpi(kpi_c3, "IHK TERENDAH (PAP. PEGUNUNGAN)", f"{lowest_prov_val:.2f}".replace('.', ','), "Indeks Rata-rata Terendah")
render_kpi(kpi_c4, "CAKUPAN DATA", "38 PROV", "11 Kelompok, 38 Sub")


# ==============================================================================
# 8. TOP NAVIGATION: TABS UTAMA (FULL WIDTH SECTIONS)
# ==============================================================================
tab_macro, tab_multi, tab_net, tab_hier = st.tabs([
    "Macro Overview",
    "Multivariate Analysis",
    "Network Analysis",
    "Hierarchical Drill-Down"
])


# ==============================================================================
# TAB 1: MACRO OVERVIEW (FULL-WIDTH DARI KIRI KE KANAN)
# ==============================================================================
with tab_macro:
    # 1. Peta Geografis Indonesia (Pilihan Choropleth / Simbol Proporsional)
    with st.container(border=True):
        render_section_header(
            "🗺️ Peta Geografis IHK Indonesia (OpenStreetMap Basemap)", 
            "Eksplorasi spasial sebaran Indeks Harga Konsumen (IHK) 38 provinsi di Indonesia. Gunakan selektor di bawah untuk beralih antara Peta Choropleth (poligon wilayah) dan Peta Simbol Proporsional (bubble map terkalibrasi)."
        )
        
        # Poin Perbaikan 2: Toggle Tampilan Alternatif Peta Geospasial
        map_type = st.radio(
            "Pilih Jenis Visualisasi Peta Geospasial:",
            options=["🗺️ Peta Choropleth (Area Poligon)", "📍 Peta Simbol Proporsional (Proportional Symbol Map)"],
            horizontal=True,
            help="Beralih antara peta tematik batas wilayah (Choropleth) dan peta sebaran lingkaran proporsional berdasarkan nilai IHK."
        )
        
        # Sinkronisasi nama provinsi dengan GeoJSON resmi 38 provinsi
        geo_name_map = {
            'Di Yogyakarta': 'Daerah Istimewa Yogyakarta',
            'Dki Jakarta': 'DKI Jakarta'
        }
        geo_df = pd.DataFrame([
            {
                'Provinsi': p,
                'IHK': prov_mean_series[p]
            }
            for p in all_provinces
        ])
        geo_df['PROVINSI_GEO'] = geo_df['Provinsi'].map(geo_name_map).fillna(geo_df['Provinsi'])
        
        min_ihk = geo_df['IHK'].min()
        max_ihk = geo_df['IHK'].max()
        
        # Data kustom untuk informasi interaktif saat kursor diarahkan ke wilayah peta
        custom_data_list = []
        for p, v in zip(geo_df['Provinsi'], geo_df['IHK']):
            diff = v - mean_ihk_nasional
            diff_str = f"+{diff:.2f}" if diff >= 0 else f"{diff:.2f}"
            if v >= 109.5:
                kat = "Tertinggi (Disparitas Ekstrem)"
            elif v >= 108.0:
                kat = "Tinggi (Di Atas Rata-rata)"
            elif v >= 106.5:
                kat = "Moderat (Sekitar Rata-rata Nasional)"
            else:
                kat = "Terendah (Di Bawah Rata-rata)"
            custom_data_list.append([p, kat, diff_str, f"{v:.2f}"])
        
        # Deteksi otomatis kelas Map untuk kompatibilitas versi Plotly (Plotly 7: Choroplethmap/Scattermap)
        if hasattr(go, 'Choroplethmap'):
            ChoroplethCls = go.Choroplethmap
            ScatterMapCls = go.Scattermap
            map_layout_cfg = dict(
                map_style="open-street-map",
                map_center=dict(lat=-2.2, lon=118.0),
                map_zoom=3.85
            )
        else:
            ChoroplethCls = getattr(go, 'Choroplethmapbox', go.Choropleth)
            ScatterMapCls = getattr(go, 'Scattermapbox', go.Scattergeo)
            map_layout_cfg = dict(
                mapbox_style="open-street-map",
                mapbox_center=dict(lat=-2.2, lon=118.0),
                mapbox_zoom=3.85
            )
        
        fig_map = go.Figure()
        
        if "Choropleth" in map_type:
            # OPSI A: PETA CHOROPLETH (AREA POLIGON)
            fig_map.add_trace(ChoroplethCls(
                geojson=geojson_data,
                locations=geo_df['PROVINSI_GEO'],
                featureidkey='properties.PROVINSI',
                z=geo_df['IHK'],
                colorscale=SEQUENTIAL_BURGUNDY_GOLD,
                zmin=min_ihk,
                zmax=max_ihk,
                marker_opacity=0.72,
                marker_line_color="rgba(253, 245, 236, 0.95)",
                marker_line_width=1.5,
                colorbar=dict(
                    title=dict(
                        text="<b>IHK 2025</b><br><span style='font-size:10px;color:#E8908A;'>Dasar 2022=100</span>",
                        font=dict(color="#FDF5EC", family="Inter", size=12)
                    ),
                    tickvals=[105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 110.6],
                    ticktext=["105.0 (Min)", "106.0", "107.0", "108.0", "109.0", "110.0", "110.6 (Maks)"],
                    tickfont=dict(color="#FDF5EC", family="Inter", size=11),
                    thickness=18,
                    len=0.82,
                    outlinecolor="rgba(253, 245, 236, 0.45)",
                    outlinewidth=1.2,
                    bgcolor="rgba(35, 7, 13, 0.85)"
                ),
                customdata=custom_data_list,
                hovertemplate=(
                    '<span style="font-size:14px; font-weight:800; color:#FDF5EC;">%{customdata[0]}</span><br>' +
                    '<span style="color:rgba(253,245,236,0.4);">' + '―'*26 + '</span><br>' +
                    '📊 Rata-rata IHK: <b>%{customdata[3]}</b><br>' +
                    '🏷️ Klasifikasi: <b>%{customdata[1]}</b><br>' +
                    f'⚖️ Selisih vs Nasional: <b>%{{customdata[2]}}</b> (Nasional: {mean_ihk_nasional:.2f})' +
                    '<extra></extra>'
                )
            ))
            
            # Indikator Sorotan (Marker Bintang) pada Provinsi Terpilih
            if selected_prov in PROVINCE_COORDS:
                sel_coord = PROVINCE_COORDS[selected_prov]
                sel_val = prov_mean_series[selected_prov]
                diff_sel = sel_val - mean_ihk_nasional
                diff_str = f"+{diff_sel:.2f}" if diff_sel >= 0 else f"{diff_sel:.2f}"
                
                fig_map.add_trace(ScatterMapCls(
                    lat=[sel_coord['lat']],
                    lon=[sel_coord['lon']],
                    mode='markers+text',
                    text=[f"<b>⭐ {selected_prov}</b>"],
                    textposition="top center",
                    textfont=dict(family="Plus Jakarta Sans", size=13, color="#FFF9F0"),
                    marker=dict(size=16, color="#FFF9F0"),
                    hoverinfo='text',
                    hovertext=[f"<b>⭐ {selected_prov} (Provinsi Sorotan)</b><br>Rata-rata IHK 2025: <b>{sel_val:.2f}</b><br>Selisih thd Nasional: <b>{diff_str}</b>"],
                    showlegend=False
                ))
        else:
            # OPSI B: PETA SIMBOL PROPORSIONAL (PROPORTIONAL SYMBOL MAP)
            # Poin Perbaikan 2: Menggunakan koordinat PROVINCE_COORDS, marker size & color proporsional thd IHK
            prop_lats = [PROVINCE_COORDS[p]['lat'] for p in geo_df['Provinsi']]
            prop_lons = [PROVINCE_COORDS[p]['lon'] for p in geo_df['Provinsi']]
            
            # Ukuran marker lingkaran diskalakan secara proporsional antara 12px s.d. 36px
            prop_sizes = [12.0 + 24.0 * ((v - min_ihk) / (max_ihk - min_ihk)) for v in geo_df['IHK']]
            
            fig_map.add_trace(ScatterMapCls(
                lat=prop_lats,
                lon=prop_lons,
                mode='markers',
                marker=dict(
                    size=prop_sizes,
                    color=geo_df['IHK'],
                    colorscale=SEQUENTIAL_BURGUNDY_GOLD,
                    cmin=min_ihk,
                    cmax=max_ihk,
                    opacity=0.88,
                    showscale=True,
                    line=dict(color="#FDF5EC", width=1.6),
                    colorbar=dict(
                        title=dict(
                            text="<b>IHK 2025</b><br><span style='font-size:10px;color:#E8908A;'>Ukuran & Warna</span>",
                            font=dict(color="#FDF5EC", family="Inter", size=12)
                        ),
                        tickvals=[105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 110.6],
                        ticktext=["105.0 (Min)", "106.0", "107.0", "108.0", "109.0", "110.0", "110.6 (Maks)"],
                        tickfont=dict(color="#FDF5EC", family="Inter", size=11),
                        thickness=18,
                        len=0.82,
                        outlinecolor="rgba(253, 245, 236, 0.45)",
                        outlinewidth=1.2,
                        bgcolor="rgba(35, 7, 13, 0.85)"
                    )
                ),
                customdata=custom_data_list,
                hovertemplate=(
                    '<span style="font-size:14px; font-weight:800; color:#FDF5EC;">%{customdata[0]}</span><br>' +
                    '<span style="color:rgba(253,245,236,0.4);">' + '―'*26 + '</span><br>' +
                    '📊 Rata-rata IHK: <b>%{customdata[3]}</b><br>' +
                    '🏷️ Klasifikasi: <b>%{customdata[1]}</b><br>' +
                    f'⚖️ Selisih vs Nasional: <b>%{{customdata[2]}}</b> (Nasional: {mean_ihk_nasional:.2f})<br>' +
                    '⭕ Ukuran Simbol: <b>Proporsional terhadap IHK</b>' +
                    '<extra></extra>'
                ),
                showlegend=False
            ))
            
            # Highlight khusus provinsi terpilih pada Simbol Proporsional
            if selected_prov in PROVINCE_COORDS:
                sel_coord = PROVINCE_COORDS[selected_prov]
                sel_val = prov_mean_series[selected_prov]
                sel_size = 12.0 + 24.0 * ((sel_val - min_ihk) / (max_ihk - min_ihk))
                diff_sel = sel_val - mean_ihk_nasional
                diff_str = f"+{diff_sel:.2f}" if diff_sel >= 0 else f"{diff_sel:.2f}"
                
                fig_map.add_trace(ScatterMapCls(
                    lat=[sel_coord['lat']],
                    lon=[sel_coord['lon']],
                    mode='markers+text',
                    text=[f"<b>⭐ {selected_prov}</b>"],
                    textposition="top center",
                    textfont=dict(family="Plus Jakarta Sans", size=13, color="#F5D6A8"),
                    marker=dict(
                        size=sel_size + 14,
                        color="rgba(245, 214, 168, 0.25)",
                        line=dict(color="#F5D6A8", width=3.0)
                    ),
                    hoverinfo='text',
                    hovertext=[f"<b>⭐ {selected_prov} (Provinsi Sorotan)</b><br>Rata-rata IHK 2025: <b>{sel_val:.2f}</b><br>Selisih thd Nasional: <b>{diff_str}</b>"],
                    showlegend=False
                ))
            
        fig_map.update_layout(
            **map_layout_cfg,
            height=580,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FDF5EC", family="Inter"),
            margin=dict(l=0, r=0, t=10, b=10)
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Poin Perbaikan 5: Atribusi Sumber Data BPS & Tombol Unduh Data Peta
        render_source_caption()
        df_dl_peta = geo_df[['Provinsi', 'IHK']].copy()
        df_dl_peta['Klasifikasi'] = [kat for _, kat, _, _ in custom_data_list]
        df_dl_peta['Selisih_vs_Nasional'] = [diff for _, _, diff, _ in custom_data_list]
        render_download_button(df_dl_peta, "data_peta_geospasial_ihk_2025.csv", "📥 Unduh Data Peta (CSV)", "dl_peta")
        
        render_takeaway(
            "Interpretasi Peta Spasial", 
            "Distribusi IHK menunjukkan adanya variasi tingkat harga antarprovinsi di Indonesia. Perbedaan tersebut menggambarkan kondisi harga yang relatif beragam antarwilayah, di mana Indonesia Timur mencatat disparitas indeks terlebar."
        )

    # 2. Clustered Heatmap (Full Width)
    with st.container(border=True):
        render_section_header("🧬 Clustered Heatmap (38 Provinsi vs 11 Kelompok Pengeluaran)", "Memetakan secara komprehensif spektrum harga konsumen pada seluruh kelompok kebutuhan hidup di 38 provinsi.")
        
        sort_option = st.selectbox(
            "Urutkan Baris Provinsi Berdasarkan:",
            options=["Rata-rata IHK (Tinggi ke Rendah)", "Rata-rata IHK (Rendah ke Tinggi)", "Berdasarkan Klaster Pola", "Abjad (A - Z)"]
        )
        selected_kel_heatmap = st.multiselect(
            "Filter Kelompok Pengeluaran:",
            options=all_kelompok,
            default=all_kelompok
        )

        df_heat = df_kelompok[selected_kel_heatmap].copy()
        if sort_option == "Rata-rata IHK (Tinggi ke Rendah)":
            df_heat['mean'] = df_heat.mean(axis=1)
            df_heat = df_heat.sort_values(by='mean', ascending=True).drop(columns=['mean'])
        elif sort_option == "Rata-rata IHK (Rendah ke Tinggi)":
            df_heat['mean'] = df_heat.mean(axis=1)
            df_heat = df_heat.sort_values(by='mean', ascending=False).drop(columns=['mean'])
        elif sort_option == "Berdasarkan Klaster Pola":
            df_heat['cluster'] = df_pca.loc[df_heat.index, 'Cluster']
            df_heat = df_heat.sort_values(by='cluster', ascending=True).drop(columns=['cluster'])
        else:
            df_heat = df_heat.sort_index(ascending=False)

        custom_y_labels = [f"👉 <b>{p}</b> (Fokus)" if p == selected_prov else p for p in df_heat.index]
        fig_heat = px.imshow(
            df_heat,
            labels=dict(x="Kelompok Pengeluaran", y="Provinsi", color="IHK"),
            y=custom_y_labels,
            color_continuous_scale=SEQUENTIAL_BURGUNDY_GOLD,
            aspect="auto"
        )
        fig_heat.update_layout(
            height=820,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FDF5EC", family="Inter", size=10),
            xaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickangle=-30),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            coloraxis_colorbar=dict(
                title=dict(text="IHK", font=dict(color="#FDF5EC")),
                tickfont=dict(color="#FDF5EC"),
                thickness=14,
                len=0.75
            ),
            margin=dict(l=10, r=10, t=10, b=40)
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
        # Poin Perbaikan 5: Atribusi Sumber Data BPS & Tombol Unduh Data Heatmap
        render_source_caption()
        df_dl_heat = df_heat.copy().reset_index().rename(columns={'index': 'Provinsi'})
        render_download_button(df_dl_heat, "data_clustered_heatmap_ihk_2025.csv", "📥 Unduh Data Heatmap (CSV)", "dl_heat")
        
        render_takeaway("Clustered Heatmap", "Kelompok Makanan, Minuman & Tembakau serta Perawatan Pribadi menunjukkan kontras warna crimson paling pekat di sebagian besar provinsi, membuktikan kedua sektor ini menjadi penyumbang utama tekanan kenaikan harga nasional.")

    # 3. Horizontal Ranking Bar Chart (Full Width)
    with st.container(border=True):
        render_section_header("📊 Peringkat IHK Rata-Rata Seluruh Provinsi", "Peringkat lengkap 38 provinsi diurutkan dari IHK terendah ke tertinggi. Batang peach terang menandai provinsi sorotan. Garis putus-putus emas menunjukkan benchmark rata-rata nasional.")
        
        df_rank = pd.DataFrame({'Provinsi': prov_mean_series.index, 'IHK': prov_mean_series.values}).sort_values(by='IHK', ascending=True)
        bar_colors = ["#E8908A" if p == selected_prov else "rgba(232, 144, 138, 0.45)" for p in df_rank['Provinsi']]
        
        fig_bar = go.Figure(go.Bar(
            x=df_rank['IHK'],
            y=df_rank['Provinsi'],
            orientation='h',
            marker=dict(color=bar_colors, line=dict(color="#FDF5EC", width=0.8)),
            hoverinfo='text',
            hovertext=[f"<b>{p}</b>: {v:.2f}" for p, v in zip(df_rank['Provinsi'], df_rank['IHK'])]
        ))
        fig_bar.add_vline(x=mean_ihk_nasional, line_dash="dash", line_color="#F5D6A8", annotation_text=f"Nasional ({mean_ihk_nasional:.2f})", annotation_font_color="#F5D6A8", annotation_position="top right")
        fig_bar.update_layout(
            height=720,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FDF5EC", family="Inter", size=10),
            xaxis=dict(title="Nilai Rata-rata IHK 2025", gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            margin=dict(l=10, r=20, t=20, b=40)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Poin Perbaikan 5: Atribusi Sumber Data BPS & Tombol Unduh Data Peringkat
        render_source_caption()
        df_dl_rank = df_rank.copy().reset_index(drop=True)
        df_dl_rank['Peringkat'] = range(1, len(df_dl_rank) + 1)
        render_download_button(df_dl_rank, "data_peringkat_ihk_2025.csv", "📥 Unduh Data Peringkat (CSV)", "dl_rank")
        
        render_takeaway("Peringkat Agregat", f"Papua Tengah memuncaki indeks tertinggi ({highest_prov_val:.2f}) sementara Papua Pegunungan menempati peringkat terendah ({lowest_prov_val:.2f}). Provinsi fokus {selected_prov} berada di angka {prov_mean_series[selected_prov]:.2f}.")

    # 4. Dot Plot Sebaran IHK (Full Width)
    with st.container(border=True):
        render_section_header("🎯 Sebaran Distribusi IHK 38 Provinsi (Dot Plot)", "Dispersi nilai 38 provinsi membentang melintasi garis patokan nasional untuk mengamati ketimpangan dan kepadatan sebaran.")
        
        fig_dot = go.Figure()
        fig_dot.add_trace(go.Scatter(
            x=prov_mean_series.values,
            y=np.random.normal(1, 0.035, size=len(prov_mean_series)),
            mode='markers',
            marker=dict(size=12, color="rgba(245, 214, 168, 0.7)", line=dict(color="#FDF5EC", width=1)),
            name="38 Provinsi",
            hoverinfo='text',
            hovertext=[f"<b>{p}</b>: {v:.2f}" for p, v in zip(prov_mean_series.index, prov_mean_series.values)]
        ))
        
        sel_val = prov_mean_series[selected_prov]
        fig_dot.add_trace(go.Scatter(
            x=[sel_val],
            y=[1.0],
            mode='markers+text',
            text=[f"⭐ {selected_prov} ({sel_val:.2f})"],
            textposition="top center",
            textfont=dict(family="Plus Jakarta Sans", size=12, color="#FDF5EC"),
            marker=dict(size=20, color="#E8908A", symbol="star", line=dict(color="#FDF5EC", width=2)),
            name=f"Fokus: {selected_prov}",
            hoverinfo='skip'
        ))
        fig_dot.add_vline(x=mean_ihk_nasional, line_width=2, line_dash="dot", line_color="#FDF5EC", annotation_text=f"Benchmark Nasional ({mean_ihk_nasional:.2f})", annotation_position="bottom right", annotation_font_color="#FDF5EC")
        fig_dot.update_layout(
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FDF5EC", family="Inter"),
            xaxis=dict(title="Nilai Rata-rata IHK", gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[0.85, 1.2]),
            showlegend=False,
            margin=dict(l=10, r=10, t=30, b=40)
        )
        st.plotly_chart(fig_dot, use_container_width=True)
        
        # Poin Perbaikan 5: Atribusi Sumber Data BPS & Tombol Unduh Data Dot Plot
        render_source_caption()
        df_dl_dot = pd.DataFrame({
            'Provinsi': prov_mean_series.index,
            'IHK_RataRata_2025': prov_mean_series.values,
            'Deviasi_vs_Nasional': prov_mean_series.values - mean_ihk_nasional
        })
        render_download_button(df_dl_dot, "data_sebaran_dotplot_ihk_2025.csv", "📥 Unduh Data Sebaran (CSV)", "dl_dot")
        
        render_takeaway("Sebaran Dispersi", "Kepadatan provinsi paling tinggi terkumpul pada rentang IHK 106,5 hingga 108,0. Titik-titik di luar rentang tersebut mencerminkan anomali regional yang membutuhkan intervensi stabilisasi pasokan pangan.")

    # 5. Kesimpulan Khusus Sub-Tema: Macro Overview (Full Width Card)
    render_conclusion_card(
        "💡 Kesimpulan: Macro Overview & Disparitas Spasial",
        "Sintesis komprehensif dinamika agregat tingkat harga 38 provinsi di Indonesia (Tahun Dasar 2022 = 100)",
        [
            {
                "title": "Disparitas Tajam di Kawasan Indonesia Timur",
                "desc": "Rata-rata IHK nasional berada di level <b>107,41</b>. Rentang disparitas terbesar justru terkonsentrasi di pulau Papua: <b>Papua Tengah</b> mencatat rata-rata tertinggi se-Indonesia (<b>110,64</b>) akibat beban logistik komoditas, sedangkan <b>Papua Pegunungan</b> mencatat rata-rata terendah (<b>104,99</b>)."
            },
            {
                "title": "Stabilitas Klaster Jawa-Sumatera Melawan Heterogenitas Kepulauan",
                "desc": "Provinsi-provinsi di pulau Jawa dan Sumatera memperlihatkan sebaran nilai yang sangat rapat di sekitar garis patokan nasional, mencerminkan integrasi pasar dan transmisi distribusi pasokan pangan yang relatif seragam dibandingkan provinsi kepulauan seperti Maluku Utara dan Papua."
            }
        ]
    )


# ==============================================================================
# TAB 2: MULTIVARIATE ANALYSIS (FULL-WIDTH DARI KIRI KE KANAN)
# ==============================================================================
with tab_multi:
    # 1. PCA Biplot (Optimalisasi 38 Subkelompok Komoditas)
    with st.container(border=True):
        render_section_header(
            "🧬 PCA Biplot (Peta Reduksi 38 Dimensi Subkelompok Komoditas)", 
            f"Model dilatih pada 38 subkelompok komoditas · Sumbu X: PC1 ({var_exp[0]*100:.1f}% variansi) · Sumbu Y: PC2 ({var_exp[1]*100:.1f}% variansi). Titik bintang peach menandai provinsi fokus. Vektor panah menunjukkan arah pengaruh subkelompok pengeluaran."
        )
        
        # Poin Perbaikan 4: Pengaturan Loadings 38 Subkelompok Komoditas
        loading_view_mode = st.radio(
            "Pilihan Vektor Loadings Subkelompok:",
            options=["🌟 10 Subkelompok Paling Berpengaruh (Top Loadings)", "📑 Seluruh 38 Subkelompok", "🚫 Sembunyikan Vektor"],
            horizontal=True
        )
        
        fig_pca = go.Figure()
        
        for cl in sorted(df_pca['Cluster'].unique()):
            sub_df = df_pca[df_pca['Cluster'] == cl]
            sub_normal = sub_df[sub_df.index != selected_prov]
            color_point = CLUSTER_COLOR_MAP.get(cl, '#E8908A')
            
            fig_pca.add_trace(go.Scatter(
                x=sub_normal['PC1'],
                y=sub_normal['PC2'],
                mode='markers+text',
                name=cl,
                text=sub_normal.index,
                textposition="top center",
                textfont=dict(size=10, color="rgba(253, 245, 236, 0.8)", family="Inter"),
                marker=dict(size=10, color=color_point, opacity=0.85, line=dict(color="#3B0A13", width=1.2)),
                hoverinfo='text',
                hovertext=[f"<b>{p}</b><br>{cl}<br>PC1: {x:.2f}, PC2: {y:.2f}" for p, x, y in zip(sub_normal.index, sub_normal['PC1'], sub_normal['PC2'])]
            ))
            
        sel_pc1 = df_pca.loc[selected_prov, 'PC1']
        sel_pc2 = df_pca.loc[selected_prov, 'PC2']
        fig_pca.add_trace(go.Scatter(
            x=[sel_pc1],
            y=[sel_pc2],
            mode='markers+text',
            name=f"Fokus: {selected_prov}",
            text=[f"⭐ <b>{selected_prov}</b>"],
            textposition="bottom center",
            textfont=dict(size=13, color="#FDF5EC", family="Plus Jakarta Sans"),
            marker=dict(size=24, color="#E8908A", symbol="star", line=dict(color="#FDF5EC", width=2.5)),
            hoverinfo='text',
            hovertext=f"<b>⭐ {selected_prov}</b><br>PC1: {sel_pc1:.2f}, PC2: {sel_pc2:.2f}"
        ))
        
        if "Sembunyikan" not in loading_view_mode:
            scale_arrow = 4.2
            all_sub_features = list(df_sub.columns)
            loading_magnitudes = [np.sqrt(pca.components_[0, i]**2 + pca.components_[1, i]**2) for i in range(len(all_sub_features))]
            
            if "10 Subkelompok" in loading_view_mode:
                top_indices = np.argsort(loading_magnitudes)[-10:]
            else:
                top_indices = range(len(all_sub_features))
                
            for i in top_indices:
                sub_name = all_sub_features[i]
                l_x = pca.components_[0, i] * scale_arrow
                l_y = pca.components_[1, i] * scale_arrow
                fig_pca.add_annotation(
                    ax=0, ay=0, x=l_x, y=l_y, xref="x", yref="y", axref="x", ayref="y",
                    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5,
                    arrowcolor="#F5D6A8", opacity=0.8
                )
                fig_pca.add_trace(go.Scatter(
                    x=[l_x * 1.12], y=[l_y * 1.12], mode="text", text=[sub_name[:16]],
                    textfont=dict(size=9, color="#F5D6A8", family="Inter"),
                    showlegend=False, hoverinfo="text",
                    hovertext=f"<b>Vektor: {sub_name}</b><br>PC1: {pca.components_[0, i]:.3f}<br>PC2: {pca.components_[1, i]:.3f}"
                ))
                
        fig_pca.update_layout(
            xaxis=dict(title=f"PC1 ({var_exp[0]*100:.1f}% Variansi)", zeroline=True, zerolinecolor="rgba(255,255,255,0.2)", gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(title=f"PC2 ({var_exp[1]*100:.1f}% Variansi)", zeroline=True, zerolinecolor="rgba(255,255,255,0.2)", gridcolor="rgba(255,255,255,0.1)"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FDF5EC", family="Inter"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            height=630,
            margin=dict(l=10, r=10, t=10, b=40)
        )
        st.plotly_chart(fig_pca, use_container_width=True)
        
        # Poin Perbaikan 5: Atribusi Sumber Data BPS & Tombol Unduh Data Skor PCA
        render_source_caption()
        df_dl_pca = df_pca.copy().reset_index().rename(columns={'index': 'Provinsi'})
        render_download_button(df_dl_pca, "data_pca_biplot_2025.csv", "📥 Unduh Data Skor PCA (CSV)", "dl_pca")
        
        render_takeaway("PCA Biplot 38 Variabel", f"Reduksi dimensi pada 38 subkelompok komoditas menghasilkan total variansi kumulatif {(var_exp[0]+var_exp[1])*100:.1f}%. PC1 mencerminkan polarisasi konsumsi modernitas rumah tangga & perawatan pribadi, sementara PC2 memisahkan sektor pakaian & tekstil dari komoditas pangan pokok.")
        
        with st.expander("📊 Lihat Detail Bobot Loadings Lengkap (38 Subkelompok Komoditas)"):
            pca_loadings_df = pd.DataFrame({
                'Subkelompok Komoditas': df_sub.columns,
                'Kelompok Induk': [sub_to_kel.get(s, '-') for s in df_sub.columns],
                'Loading PC1': pca.components_[0],
                'Loading PC2': pca.components_[1],
                'Magnitudo Kontribusi': [np.sqrt(pca.components_[0, i]**2 + pca.components_[1, i]**2) for i in range(len(df_sub.columns))]
            }).sort_values(by='Magnitudo Kontribusi', ascending=False)
            try:
                st.dataframe(pca_loadings_df.style.background_gradient(cmap='PuRd', subset=['Loading PC1', 'Loading PC2', 'Magnitudo Kontribusi']), use_container_width=True, hide_index=True)
            except Exception:
                st.dataframe(pca_loadings_df, use_container_width=True, hide_index=True)
            render_source_caption()

    # 2. Parallel Coordinates (Full Width)
    with st.container(border=True):
        render_section_header("📈 Parallel Coordinates (Profil Pola Komparatif 11 Kelompok Pengeluaran)", "Setiap garis mewakili satu provinsi melintasi 11 kelompok pengeluaran makro. Garis putus-putus putih: rata-rata nasional. Garis tebal peach: provinsi fokus. Garis lain redup transparan.")
        
        compare_prov = st.selectbox(
            "Bandingkan dengan Provinsi Lain:",
            options=["(Tidak Ada)"] + [p for p in all_provinces if p != selected_prov],
            index=0
        )
        
        fig_par = go.Figure()
        short_kel = [k.replace("Perlengkapan, Peralatan dan Pemeliharaan Rutin Rumah Tangga", "Perlengkapan RT")
                      .replace("Perumahan, Air, Listrik dan Bahan Bakar Rumah", "Perumahan & Energi")
                      .replace("Informasi, Komunikasi dan Jasa Keuangan", "Info & Komunikasi")
                      .replace("Penyediaan Makanan dan Minuman / Restoran", "Restoran / F&B")
                      .replace("Perawatan Pribadi dan Jasa Lainnya", "Perawatan Pribadi")
                      .replace("Rekreasi, Olahraga dan Budaya", "Rekreasi & Budaya")
                      .replace("Makanan, Minuman dan Tembakau", "Makanan & Tembakau")
                      .replace("Pendidikan Dasar dan Anak Usia Dini", "Pendidikan") for k in all_kelompok]
        
        for p in all_provinces:
            if p != selected_prov and p != compare_prov:
                fig_par.add_trace(go.Scatter(
                    x=short_kel, y=df_kelompok.loc[p], mode='lines',
                    line=dict(color="rgba(255, 255, 255, 0.16)", width=1),
                    name="Provinsi Lain", showlegend=False, hoverinfo='text', hovertext=f"<b>{p}</b>"
                ))
                
        fig_par.add_trace(go.Scatter(
            x=short_kel, y=df_kelompok.mean(), mode='lines+markers',
            line=dict(color="#FDF5EC", width=2.5, dash="dot"),
            marker=dict(size=6, color="#FDF5EC"),
            name="🇮🇩 Rata-Rata Nasional",
            hoverinfo='text', hovertext=[f"<b>Rata-rata Nasional</b><br>{k}: {v:.2f}" for k, v in zip(short_kel, df_kelompok.mean())]
        ))
        
        if compare_prov != "(Tidak Ada)":
            fig_par.add_trace(go.Scatter(
                x=short_kel, y=df_kelompok.loc[compare_prov], mode='lines+markers',
                line=dict(color="#F5D6A8", width=3.5),
                marker=dict(size=7, color="#F5D6A8"),
                name=f"📍 {compare_prov}",
                hoverinfo='text', hovertext=[f"<b>{compare_prov}</b><br>{k}: {v:.2f}" for k, v in zip(short_kel, df_kelompok.loc[compare_prov])]
            ))
            
        fig_par.add_trace(go.Scatter(
            x=short_kel, y=df_kelompok.loc[selected_prov], mode='lines+markers',
            line=dict(color="#E8908A", width=4.5),
            marker=dict(size=9, color="#E8908A", line=dict(color="#FDF5EC", width=1.8)),
            name=f"⭐ {selected_prov} (Fokus)",
            hoverinfo='text', hovertext=[f"<b>⭐ {selected_prov}</b><br>{k}: {v:.2f}" for k, v in zip(short_kel, df_kelompok.loc[selected_prov])]
        ))
        
        fig_par.update_layout(
            xaxis=dict(tickangle=-25, gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(title="Nilai IHK", gridcolor="rgba(255,255,255,0.1)"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FDF5EC", family="Inter"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5),
            height=580,
            margin=dict(l=10, r=10, t=10, b=80)
        )
        st.plotly_chart(fig_par, use_container_width=True)
        
        # Poin Perbaikan 5: Atribusi Sumber Data BPS & Tombol Unduh Data Parallel Coordinates
        render_source_caption()
        df_dl_par = df_kelompok.copy().reset_index().rename(columns={'index': 'Provinsi'})
        render_download_button(df_dl_par, "data_parallel_coordinates_2025.csv", "📥 Unduh Data Kelompok Pengeluaran (CSV)", "dl_par")
        
        render_takeaway("Parallel Coordinates", f"Pola garis provinsi {selected_prov} memperlihatkan fluktuasi spesifik antar-11 kelompok pengeluaran. Kelompok dengan jarak terjauh dari benchmark nasional merupakan determinan inflasi lokal utama.")

    # 3. Kesimpulan Khusus Sub-Tema: Multivariate Analysis (Full Width Card)
    render_conclusion_card(
        "💡 Kesimpulan: Multivariate Analysis & Reduksi Dimensi",
        "Interpretasi reduksi dimensi subkelompok komoditas melalui PCA dan klasterisasi K-Means",
        [
            {
                "title": "Presisi Analisis Multivariat Berbasis 38 Subkelompok",
                "desc": f"Pengalihan reduksi dimensi ke 38 variabel subkelompok mengungkap pembagian variansi yang mendalam: <b>PC1 ({var_exp[0]*100:.1f}%)</b> dipimpin oleh komoditas tahan lama dan perawatan (<i>Furnitur & Perlengkapan +0,327</i>, <i>Perawatan Pribadi +0,316</i>, <i>Layanan Olahraga +0,315</i>), sementara <b>PC2 ({var_exp[1]*100:.1f}%)</b> menangkap variansi kebutuhan sandang (<i>Pakaian +0,323</i>, <i>Alas Kaki +0,246</i>) melawan bahan pokok."
            },
            {
                "title": "Segmentasi Karakteristik Antarwilayah",
                "desc": "Provinsi urban seperti DKI Jakarta, Bali, dan Kepulauan Riau menempati kuadran kanan atas (tinggi pada gaya hidup dan komunikasi), sedangkan provinsi kepulauan dan pedalaman terdistribusi di kuadran berlawanan karena tertekan tingginya indeks biaya logistik pangan dan kesehatan."
            }
        ]
    )


# ==============================================================================
# TAB 3: NETWORK ANALYSIS (FULL-WIDTH DARI KIRI KE KANAN)
# ==============================================================================
with tab_net:
    # 1. Ringkasan Metrik Network (Full Width Grid - Desain Metrik Sekunder Ramping)
    net_m1, net_m2, net_m3, net_m4 = st.columns(4)
    total_edges = G.number_of_edges()
    avg_degree = sum(node_degrees.values()) / len(G.nodes)
    connected_components_count = nx.number_connected_components(G)
    sel_neighbors = list(G.neighbors(selected_prov))
    
    render_secondary_metric(net_m1, "TOTAL EDGE AKTIF", f"{total_edges}", f"Korelasi ≥ {network_threshold:.2f}")
    render_secondary_metric(net_m2, "RATA-RATA DERAJAT", f"{avg_degree:.1f}", "Koneksi serupa per provinsi")
    render_secondary_metric(net_m3, "JUMLAH KOMPONEN", f"{connected_components_count}", "Kluster/pulau terpisah")
    render_secondary_metric(net_m4, f"KONEKSI {selected_prov[:14]}", f"{len(sel_neighbors)}", f"{len(sel_neighbors) - int(avg_degree):+d} vs Rata-rata")

    # 2. Force-Directed Graph (Full Width)
    with st.container(border=True):
        render_section_header("🕸️ Force-Directed Graph (Jaringan Kemiripan Antarprovinsi)", f"Visualisasi graf fisika pegas (spring layout). Ukuran node proporsional terhadap koneksi (derajat). Garis peach tebal menunjukkan relasi langsung provinsi fokus ({selected_prov}).")
        
        edge_x, edge_y = [], []
        sel_edge_x, sel_edge_y = [], []
        
        for u, v, data in G.edges(data=True):
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            if u == selected_prov or v == selected_prov:
                sel_edge_x.extend([x0, x1, None])
                sel_edge_y.extend([y0, y1, None])
            else:
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
                
        fig_net = go.Figure()
        fig_net.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color="rgba(255, 255, 255, 0.15)"),
            hoverinfo='none', mode='lines'
        ))
        fig_net.add_trace(go.Scatter(
            x=sel_edge_x, y=sel_edge_y,
            line=dict(width=3.2, color="#E8908A"),
            hoverinfo='none', mode='lines'
        ))
        
        node_x, node_y, node_text, node_color, node_size = [], [], [], [], []
        for node in G.nodes():
            x, y = pos[node]
            deg = node_degrees[node]
            cl = df_pca.loc[node, 'Cluster']
            node_x.append(x)
            node_y.append(y)
            node_size.append(max(11, deg * 1.6 + 8))
            node_color.append(CLUSTER_COLOR_MAP.get(cl, '#E8908A'))
            neighbors = [f"{nb} (r={corr_matrix.loc[node, nb]:.2f})" for nb in G.neighbors(node)]
            top_nb = "<br> • ".join(neighbors[:5])
            nb_str = f"<br><b>Tetangga Serupa (r ≥ {network_threshold:.2f}):</b><br> • " + top_nb if neighbors else "<br><i>(Terisolasi pada threshold ini)</i>"
            node_text.append(f"<b>{node}</b><br>{cl}<br>Derajat: {deg}{nb_str}")
            
        fig_net.add_trace(go.Scatter(
            x=node_x, y=node_y, mode='markers+text',
            text=list(G.nodes()), textposition="top center",
            textfont=dict(size=9, color="#FDF5EC", family="Inter"),
            hoverinfo='text', hovertext=node_text,
            marker=dict(color=node_color, size=node_size, line=dict(color="#3B0A13", width=1.5))
        ))
        
        if selected_prov in pos:
            sx, sy = pos[selected_prov]
            fig_net.add_trace(go.Scatter(
                x=[sx], y=[sy], mode='markers+text',
                text=[f"⭐ <b>{selected_prov}</b>"], textposition="bottom center",
                textfont=dict(size=13, color="#FDF5EC", family="Plus Jakarta Sans"),
                marker=dict(size=26, color="#E8908A", symbol="star", line=dict(color="#FDF5EC", width=2.5)),
                hoverinfo='skip'
            ))
            
        fig_net.update_layout(
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FDF5EC", family="Inter"),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=680,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_net, use_container_width=True)
        
        # Poin Perbaikan 5: Atribusi Sumber Data BPS & Tombol Unduh Data Jaringan Graf
        render_source_caption()
        edge_records = []
        for u, v in G.edges():
            edge_records.append({
                'Provinsi_1': u,
                'Provinsi_2': v,
                'Koefisien_Korelasi': round(corr_matrix.loc[u, v], 4),
                'Klaster_Provinsi_1': df_pca.loc[u, 'Cluster'],
                'Klaster_Provinsi_2': df_pca.loc[v, 'Cluster']
            })
        df_dl_edges = pd.DataFrame(edge_records) if edge_records else pd.DataFrame(columns=['Provinsi_1', 'Provinsi_2', 'Koefisien_Korelasi', 'Klaster_Provinsi_1', 'Klaster_Provinsi_2'])
        render_download_button(df_dl_edges, f"data_network_edges_r{int(network_threshold*100)}_2025.csv", "📥 Unduh Data Relasi Jaringan (CSV)", "dl_net")
        
        render_takeaway("Topologi Network", f"Pada ambang r = {network_threshold:.2f}, provinsi fokus {selected_prov} memiliki {len(sel_neighbors)} tetangga korelasi langsung. Struktur jaringan memperlihatkan inti terpadu berderajat tinggi dan pulau terisolasi berderajat 0.")

    # 3. Poin Perbaikan 3: Chart Adjacency Matrix (PERSIS DI BAWAH GRAF FORCE-DIRECTED)
    with st.container(border=True):
        render_section_header(
            "⏹️ Matriks Adjacency (Koneksi Korelasi Antarprovinsi)", 
            f"Tampilan alternatif data berjaring memvisualisasikan matriks korelasi penuh (corr_matrix) antarprovinsi berbasis 38 subkelompok. Menunjukkan struktur blok homogenitas intra-klaster dan asimetri antar-wilayah."
        )
        
        c_adj1, c_adj2 = st.columns([1.5, 1.5])
        with c_adj1:
            matrix_sort_order = st.radio(
                "Urutan Baris & Kolom Matriks:",
                options=["Urut Berdasarkan Klaster Pola", "Urut Abjad (A - Z)", "Urut Rata-rata IHK"],
                horizontal=True
            )
        with c_adj2:
            matrix_filter_mode = st.radio(
                "Filter Ambang Batas Korelasi:",
                options=[f"Terapkan Ambang Batas (r ≥ {network_threshold:.2f})", "Tampilkan Seluruh Nilai Korelasi (Penuh)"],
                horizontal=True
            )
        
        # Pengurutan matriks
        if "Klaster" in matrix_sort_order:
            ordered_provs = df_pca.sort_values(by='Cluster').index.tolist()
        elif "Rata-rata" in matrix_sort_order:
            ordered_provs = prov_mean_series.index.tolist()
        else:
            ordered_provs = sorted(all_provinces)
            
        display_corr = corr_matrix.loc[ordered_provs, ordered_provs].copy()
        
        if "Terapkan Ambang Batas" in matrix_filter_mode:
            display_corr_masked = display_corr.copy()
            display_corr_masked[display_corr_masked < network_threshold] = np.nan
            c_min_val = network_threshold
        else:
            display_corr_masked = display_corr.copy()
            c_min_val = float(np.nanmin(display_corr.values))
            
        fig_adj = px.imshow(
            display_corr_masked,
            labels=dict(x="Provinsi", y="Provinsi", color="Korelasi (r)"),
            color_continuous_scale=SEQUENTIAL_BURGUNDY_GOLD,
            range_color=[c_min_val, 1.0],
            aspect="auto"
        )
        fig_adj.update_layout(
            height=780,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FDF5EC", family="Inter", size=10),
            xaxis=dict(tickangle=-35, gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            coloraxis_colorbar=dict(
                title=dict(text="<b>Korelasi (r)</b>", font=dict(color="#FDF5EC", size=11)),
                tickfont=dict(color="#FDF5EC"),
                thickness=16,
                len=0.75
            ),
            margin=dict(l=10, r=10, t=10, b=50)
        )
        st.plotly_chart(fig_adj, use_container_width=True)
        
        # Poin Perbaikan 5: Atribusi Sumber Data BPS & Tombol Unduh Data Matriks Adjacency
        render_source_caption()
        df_dl_adj = display_corr.copy().reset_index().rename(columns={'index': 'Provinsi'})
        render_download_button(df_dl_adj, "data_matriks_adjacency_korelasi_2025.csv", "📥 Unduh Data Matriks Adjacency (CSV)", "dl_adj")
        
        render_takeaway("Matriks Adjacency", "Blok-blok diagonal yang menyala terang membuktikan tingginya homogenitas pola harga di dalam klaster yang sama, sedangkan area gelap menegaskan asimetri hubungan antar-klaster.")

    # 4. Profil Kemiripan & Tabel Tetangga (Full Width Layout, Tidak Terbelah Sempit)
    with st.container(border=True):
        render_section_header(f"👥 Profil Kemiripan Spesifik: {selected_prov}", "Koefisien korelasi kemiripan pola pengeluaran terhadap provinsi fokus. Menampilkan provinsi paling serupa dan paling berbeda secara penuh dari kiri ke kanan.")
        
        sim_series = corr_matrix[selected_prov].drop(selected_prov).sort_values(ascending=False)
        
        view_sim_choice = st.radio(
            "Pilih Tampilan Tabel Profil:",
            options=["🟢 8 Provinsi Paling Mirip (Korelasi Tertinggi)", "🔴 4 Provinsi Paling Berbeda (Korelasi Terendah)", "📑 Tampilkan Keduanya Berurutan"],
            horizontal=True
        )
        
        if "Paling Mirip" in view_sim_choice or "Keduanya" in view_sim_choice:
            st.write(f"**🟢 8 Provinsi Paling Mirip dengan {selected_prov} (Pola Pergerakan Paling Serupa):**")
            top_similar_df = pd.DataFrame({'Provinsi': sim_series.index[:8], 'Koefisien Korelasi (r)': sim_series.values[:8]})
            try:
                st.dataframe(top_similar_df.style.format({'Koefisien Korelasi (r)': '{:.3f}'}).background_gradient(cmap='PuRd', subset=['Koefisien Korelasi (r)']), use_container_width=True, hide_index=True)
            except Exception:
                st.dataframe(top_similar_df, use_container_width=True, hide_index=True)
                
        if "Paling Berbeda" in view_sim_choice or "Keduanya" in view_sim_choice:
            st.write(f"**🔴 4 Provinsi Paling Berbeda dengan {selected_prov} (Pola Pergerakan Paling Asimetris):**")
            least_similar_df = pd.DataFrame({'Provinsi': sim_series.index[-4:], 'Koefisien Korelasi (r)': sim_series.values[-4:]})
            try:
                st.dataframe(least_similar_df.style.format({'Koefisien Korelasi (r)': '{:.3f}'}).background_gradient(cmap='OrRd', subset=['Koefisien Korelasi (r)']), use_container_width=True, hide_index=True)
            except Exception:
                st.dataframe(least_similar_df, use_container_width=True, hide_index=True)
                
        # Poin Perbaikan 5: Atribusi Sumber Data BPS & Tombol Unduh Data Profil Kemiripan
        render_source_caption()
        df_dl_sim = pd.DataFrame({
            'Provinsi_Fokus': selected_prov,
            'Provinsi_Mitra': sim_series.index,
            'Koefisien_Korelasi_r': sim_series.values.round(4)
        })
        render_download_button(df_dl_sim, f"data_profil_kemiripan_{selected_prov.lower().replace(' ', '_')}.csv", "📥 Unduh Data Profil Kemiripan (CSV)", "dl_sim")
        
        render_takeaway("Profil Kemiripan Pasangan", f"Mitra paling serupa dengan {selected_prov} adalah {sim_series.index[0]} (r = {sim_series.values[0]:.3f}), sedangkan provinsi dengan disparitas perilaku harga tertinggi adalah {sim_series.index[-1]} (r = {sim_series.values[-1]:.3f}).")

    # 5. Kesimpulan Khusus Sub-Tema: Network Analysis (Full Width Card)
    render_conclusion_card(
        "💡 Kesimpulan: Network Analysis & Struktur Asimetri",
        "Rangkuman relasi kemiripan dan konektivitas harga antarprovinsi melalui graf network dan matriks adjacency",
        [
            {
                "title": "Blok Raksasa Terpadu: Klaster 23 Provinsi Barat-Tengah",
                "desc": "Pada ambang batas korelasi standar <b>r ≥ 0,80</b>, sebanyak 23 provinsi membentuk satu komponen jaringan raksasa (*giant component*). Kemiripan tertinggi terjadi antara <b>DI Yogyakarta dan Sulawesi Selatan (r = 0,988)</b>, disusul <b>NTB & Sumatera Selatan (r = 0,985)</b> serta <b>Jawa Barat & Jawa Timur (r = 0,985)</b>, membuktikan bahwa kesamaan pola didorong oleh struktur konsumsi perkotaan dan pasokan, bukan batas geografis semata."
            },
            {
                "title": "Isolasi Struktural Kawasan Indonesia Timur",
                "desc": "Provinsi di kawasan Papua (<b>Papua Pegunungan, Papua Tengah, Papua</b>) dan <b>Maluku Utara</b> terisolasi dari komponen raksasa (misalnya korelasi Maluku Utara ↔ Sulawesi Tenggara hanya <i>r = 0,418</i>; DKI Jakarta ↔ Papua Pegunungan hanya <i>r = 0,452</i>). Hal ini mengonfirmasi adanya keterputusan logistik dan perbedaan perilaku harga yang sangat asimetris."
            }
        ]
    )


# ==============================================================================
# TAB 4: HIERARCHICAL DRILL-DOWN (FULL-WIDTH DARI KIRI KE KANAN)
# ==============================================================================
with tab_hier:
    # Breadcrumb Navigation (Full Width)
    st.html(f'''<div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); backdrop-filter: blur(8px); border-radius: 12px; padding: 14px 22px; font-size: 0.94rem; font-weight: 600; color: #FDF5EC; margin-bottom: 22px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
        <span>🏠 Indonesia (Root Node)</span>
        <span style="opacity: 0.5;">➔</span>
        <span style="color: #F5D6A8;">📍 {selected_prov}</span>
        <span style="opacity: 0.5;">➔</span>
        <span style="color: #E8908A;">🏷️ 11 Kelompok Pengeluaran</span>
        <span style="opacity: 0.5;">➔</span>
        <span style="color: #FDF5EC;">📦 38 Subkelompok Komoditas</span>
    </div>''')
    
    hier_scope = st.radio(
        "Pilih Lingkup Analisis Hierarki:",
        options=[f"Fokus Provinsi: {selected_prov}", "Agregat Seluruh Indonesia (38 Provinsi)"],
        horizontal=True
    )
    
    # Poin Perbaikan 1: Struktur Hierarki 3 Level (Indonesia -> Kelompok -> Subkelompok)
    # Parameter ukuran (values) menggunakan 'Bobot_Pengeluaran' (Diagram Timbang %)
    # Parameter warna (color) menggunakan 'IHK_RataRata_2025' (dua variabel numerik berbeda)
    if hier_scope.startswith("Fokus Provinsi"):
        df_hier_filt = df_hier[df_hier['Provinsi'] == selected_prov].copy()
    else:
        df_hier_filt = df_hier.groupby(['Indonesia', 'Kelompok', 'Subkelompok'], as_index=False).agg({
            'IHK_RataRata_2025': 'mean',
            'Bobot_Pengeluaran': 'first'
        })
        
    h_path = ['Indonesia', 'Kelompok', 'Subkelompok']

    # 1. Sunburst Chart (Full Width)
    with st.container(border=True):
        render_section_header(
            "☀️ Sunburst Chart (Struktur Konsentris 3 Level Hierarki IHK)", 
            "Diagram konsentris 3 level (Indonesia ➔ Kelompok ➔ Subkelompok). Ukuran sektor (values) merepresentasikan Bobot Diagram Timbang Pengeluaran (%), sedangkan warna sektor (color) merepresentasikan Nilai Rata-rata IHK 2025. Klik cincin untuk zoom-in ke rincian komoditas."
        )
        
        fig_sun = px.sunburst(
            df_hier_filt,
            path=h_path,
            values='Bobot_Pengeluaran',
            color='IHK_RataRata_2025',
            color_continuous_scale=SEQUENTIAL_BURGUNDY_GOLD,
            hover_data={'Bobot_Pengeluaran': ':.2f', 'IHK_RataRata_2025': ':.2f'}
        )
        fig_sun.update_traces(
            insidetextorientation='horizontal',
            hovertemplate=(
                '<b>%{label}</b><br>' +
                '🏷️ Hierarki Induk: <b>%{parent}</b><br>' +
                '📦 Bobot Diagram Timbang: <b>%{value:.2f}%</b><br>' +
                '📈 Rata-rata IHK 2025: <b>%{color:.2f}</b><br>' +
                '<extra></extra>'
            )
        )
        fig_sun.update_layout(
            height=700,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FDF5EC", family="Inter"),
            coloraxis_colorbar=dict(
                title=dict(text="<b>IHK 2025</b>", font=dict(color="#FDF5EC", size=12)),
                tickfont=dict(color="#FDF5EC"),
                thickness=16,
                len=0.75
            ),
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_sun, use_container_width=True)
        
        # Poin Perbaikan 5: Atribusi Sumber Data BPS & Tombol Unduh Data Sunburst
        render_source_caption()
        render_download_button(df_hier_filt, "data_hierarki_sunburst_3level_2025.csv", "📥 Unduh Data Sunburst (CSV)", "dl_sun")
        
        render_takeaway("Sunburst Konsentris 3 Level", "Struktur konsentris memperlihatkan bahwa bobot agregat terbesar (~33,7%) dan variasi warna terdalam terkonsentrasi pada cincin Makanan, Minuman & Tembakau, membuktikan pengaruh dominan sektor ini terhadap kerentanan daya beli masyarakat.")

    # 2. Treemap Chart (Full Width)
    with st.container(border=True):
        render_section_header(
            "🗺️ Treemap Chart (Komposisi Proporsi Spasial 3 Level Hierarki IHK)", 
            "Hierarki persegi proporsional 3 level (Indonesia ➔ Kelompok ➔ Subkelompok). Luas kotak (values) mencerminkan Bobot Diagram Timbang (%), sedangkan rona warna (color) mencerminkan Nilai IHK 2025. Klik kotak untuk zoom-in ke rincian komoditas."
        )
        
        fig_tree = px.treemap(
            df_hier_filt,
            path=h_path,
            values='Bobot_Pengeluaran',
            color='IHK_RataRata_2025',
            color_continuous_scale=SEQUENTIAL_BURGUNDY_GOLD,
            hover_data={'Bobot_Pengeluaran': ':.2f', 'IHK_RataRata_2025': ':.2f'}
        )
        fig_tree.update_traces(
            hovertemplate=(
                '<b>%{label}</b><br>' +
                '🏷️ Hierarki Induk: <b>%{parent}</b><br>' +
                '📦 Bobot Diagram Timbang: <b>%{value:.2f}%</b><br>' +
                '📈 Rata-rata IHK 2025: <b>%{color:.2f}</b><br>' +
                '<extra></extra>'
            )
        )
        fig_tree.update_layout(
            height=670,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FDF5EC", family="Inter"),
            coloraxis_colorbar=dict(
                title=dict(text="<b>IHK 2025</b>", font=dict(color="#FDF5EC", size=12)),
                tickfont=dict(color="#FDF5EC"),
                thickness=16,
                len=0.75
            ),
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_tree, use_container_width=True)
        
        # Poin Perbaikan 5: Atribusi Sumber Data BPS & Tombol Unduh Data Treemap
        render_source_caption()
        render_download_button(df_hier_filt, "data_hierarki_treemap_3level_2025.csv", "📥 Unduh Data Treemap (CSV)", "dl_tree")
        
        render_takeaway("Treemap Proporsi Spasial 3 Level", "Luas area kotak menunjukkan proporsi bobot konsumsi rumah tangga. Komoditas esensial seperti Makanan Pokok (25,2%) dan Energi Rumah Tangga menduduki proporsi ruang terluas dengan rona warna pekat di seluruh provinsi.")

    # 3. Kesimpulan Khusus Sub-Tema: Hierarchical Drill-Down (Full Width Card)
    render_conclusion_card(
        "💡 Kesimpulan: Hierarchical Drill-Down & Disparitas Subkelompok",
        "Penelusuran akar pembentukan indeks dari level makro ke subkelompok komoditas mikro pada 3 level hierarki",
        [
            {
                "title": "Akar Lonjakan Makro Bersumber dari Komoditas Esensial Tertentu",
                "desc": "Eksplorasi Sunburst dan Treemap menunjukkan bahwa lonjakan indeks pada kelompok pengeluaran besar selalu dipicu oleh subkelompok tertentu: <b>Makanan Pokok / Padi-padian</b> dan <b>Rokok & Tembakau</b> (IHK menembus level 125-140 di sejumlah provinsi luar Jawa)."
            },
            {
                "title": "Disparitas Tarif Layanan Lokal dan Utilitas Publik",
                "desc": "Pada kelompok Perumahan dan Energi, disparitas indeks antardaerah paling lebar tercatat pada subkelompok <b>Penyediaan Air dan Layanan Rumah Tangga Terkait</b>, yang secara langsung merefleksikan variasi regulasi tarif PDAM lokal dan struktur geografis pasokan air bersih antarprovinsi."
            }
        ]
    )


# ==============================================================================
# 9. SECTION INSIGHT & KESIMPULAN UTAMA DASHBOARD (FULL-WIDTH, PURE HTML)
# ==============================================================================
render_conclusion_card(
    "💡 Kesimpulan Utama & Sintesis Eksekutif:",
    "Menjawab Pertanyaan Riset Utama: Apakah pola perubahan harga konsumen di Indonesia memiliki karakteristik yang sama di setiap provinsi?",
    [
        {
            "title": "TEMUAN 01 — Pola Harga Antarprovinsi TIDAK SERAGAM (Hasil Reduksi PCA 38 Subkelompok)",
            "desc": f"Pola pergerakan harga konsumen di Indonesia memiliki karakteristik yang <b>berbeda secara signifikan antarprovinsi</b>. Reduksi dimensi pada 38 subkelompok komoditas menunjukkan <b>PC1 ({var_exp[0]*100:.1f}% variansi)</b> paling kuat digerakkan oleh tingkat modernitas dan perlengkapan rumah tangga (<i>Furnitur & Perlengkapan +0,327</i> dan <i>Perawatan Pribadi +0,316</i>), sedangkan <b>PC2 ({var_exp[1]*100:.1f}% variansi)</b> menangkap variansi kebutuhan sandang (<i>Pakaian +0,323</i>, <i>Alas Kaki +0,246</i>) melawan komoditas esensial pangan."
        },
        {
            "title": "TEMUAN 02 — Kedekatan Pola Antarwilayah: Fenomena Yogyakarta & Sulawesi Selatan",
            "desc": "Kemiripan pola harga tidak mutlak dibatasi oleh kedekatan daratan geografis. Pasangan provinsi dengan pola paling identik di Indonesia adalah <b>DI Yogyakarta dan Sulawesi Selatan (r = 0,988)</b>, disusul <b>NTB & Sumatera Selatan (r = 0,985)</b> serta <b>Jawa Barat & Jawa Timur (r = 0,985)</b>. Sebanyak <b>23 dari 38 provinsi</b> mengelompok padat dalam klaster inti barat/tengah yang memiliki respon transmisi harga serupa."
        },
        {
            "title": "TEMUAN 03 — Topologi Network Mengungkap Isolasi dan Asimetri Indonesia Timur",
            "desc": "Pada ambang batas korelasi standar <b>r ≥ 0,80</b>, terbentuk satu <i>giant component</i> terpadu Jawa-Sumatera-Kalimantan. Sebaliknya, provinsi di kawasan Papua (<b>Papua Pegunungan, Papua Tengah, Papua</b>) dan <b>Maluku Utara</b> terisolasi dengan korelasi terendah di Indonesia (misalnya Maluku Utara ↔ Sulawesi Tenggara hanya <i>r = 0,418</i>; DKI Jakarta ↔ Papua Pegunungan hanya <i>r = 0,452</i>), membuktikan asimetri biaya pasok logistik lokal."
        },
        {
            "title": "TEMUAN 04 — Penelusuran Hierarkis: Disparitas Makro Berakar dari Subkelompok Spesifik",
            "desc": "Penelusuran konsentris Sunburst dan proporsi spasial Treemap 3 level membuktikan bahwa ketimpangan agregat provinsi selalu berakar dari lonjakan tajam pada komoditas spesifik, terutama <b>Makanan Pokok</b>, <b>Rokok/Tembakau</b>, dan <b>Penyediaan Air Bersih</b>, bukan karena kenaikan seragam di seluruh barang konsumsi."
        }
    ]
)

# Footer
st.html('''<div style="text-align: center; color: rgba(253, 245, 236, 0.45); font-size: 0.85rem; padding: 26px 0 10px 0; font-family: \'Inter\', sans-serif;">
    <b>Dashboard Analisis Indeks Harga Konsumen 38 Provinsi di Indonesia</b><br>
    Dikembangkan untuk Ujian Akhir Semester (UAS) Visualisasi Data • Politeknik Statistika STIS • Sumber Data: Badan Pusat Statistik (BPS) 2025
</div>''')
