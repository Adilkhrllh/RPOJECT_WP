# ============================================================
# SPK INVESTASI - METODE WEIGHTED PRODUCT (WP)
# Dibuat dengan Python + Streamlit
# ============================================================
# CARA PAKAI:
#   1. Install library: pip install streamlit pandas numpy matplotlib seaborn
#   2. Jalankan: streamlit run app.py
#   3. Upload file CSV kamu di sidebar
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# KONFIGURASI HALAMAN STREAMLIT
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InvestSmart SPK - Weighted Product",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# TAMPILAN (CSS) - Bagian ini mengatur warna dan style tampilan web
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 50%, #0a1628 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1b35 0%, #111d30 100%);
        border-right: 1px solid #1e3a5f;
    }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #0d1f3c, #112240);
        border: 1px solid #1e4080;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 20px rgba(0,150,255,0.08);
    }
    [data-testid="stMetricLabel"] { color: #7aa8d2 !important; font-size: 0.78rem !important; }
    [data-testid="stMetricValue"] { color: #e8f4fd !important; font-size: 1.6rem !important; font-weight: 700 !important; }

    h1, h2, h3 { color: #e8f4fd !important; }
    p, li, label { color: #b0c9e8 !important; }

    [data-testid="stDataFrame"] {
        border: 1px solid #1e3a5f;
        border-radius: 10px;
        overflow: hidden;
    }
    .stButton > button {
        background: linear-gradient(135deg, #0066cc, #0044aa);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,102,204,0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #0080ff, #0055cc);
        box-shadow: 0 6px 25px rgba(0,128,255,0.5);
        transform: translateY(-2px);
    }
    .banner {
        background: linear-gradient(135deg, #051530 0%, #0a2040 50%, #0c2850 100%);
        border: 1px solid #1e4080;
        border-radius: 16px;
        padding: 32px 40px;
        margin-bottom: 24px;
        box-shadow: 0 8px 40px rgba(0,100,255,0.12);
        position: relative;
        overflow: hidden;
    }
    .banner-title { font-size: 2rem; font-weight: 700; color: #ffffff; margin-bottom: 6px; }
    .banner-sub   { font-size: 1rem; color: #7aa8d2; font-weight: 400; }
    .badge {
        display: inline-block;
        background: linear-gradient(135deg, #0055aa, #003d80);
        color: #7ec8ff;
        border: 1px solid #0066cc;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.78rem; font-weight: 600;
        margin-right: 8px; margin-top: 12px;
    }
    .section-title {
        font-size: 1.2rem; font-weight: 700; color: #e8f4fd;
        border-left: 4px solid #0066cc;
        padding-left: 14px;
        margin: 28px 0 16px 0;
    }
    .info-box {
        background: linear-gradient(135deg, #051530, #0a2040);
        border: 1px solid #1e3a6e;
        border-left: 4px solid #0066cc;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 16px;
    }
    .formula-box {
        background: #060f22;
        border: 1px solid #1a3a6e;
        border-radius: 10px;
        padding: 16px 20px;
        font-family: 'JetBrains Mono', monospace;
        color: #7ec8ff;
        font-size: 0.88rem;
        margin: 12px 0;
    }
    .profile-card {
        background: linear-gradient(135deg, #0d1f3c, #112240);
        border: 1px solid #1e4080;
        border-radius: 14px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s;
        box-shadow: 0 4px 20px rgba(0,100,255,0.08);
    }
    .profile-card:hover {
        border-color: #0066cc;
        box-shadow: 0 8px 30px rgba(0,100,255,0.2);
        transform: translateY(-4px);
    }
    .profile-avatar {
        width: 80px; height: 80px;
        background: linear-gradient(135deg, #0055aa, #0066cc);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 2rem;
        margin: 0 auto 12px auto;
        border: 3px solid #1a5fa8;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    hr { border-color: #1e3a5f !important; }
    [data-testid="stExpander"] {
        background: #0d1f3c;
        border: 1px solid #1e3a6e;
        border-radius: 10px;
    }
    /* Style khusus untuk kotak upload file */
    [data-testid="stFileUploader"] {
        background: #0d1f3c;
        border: 2px dashed #0066cc;
        border-radius: 10px;
        padding: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# KONFIGURASI KOLOM KRITERIA
# Ini adalah nama-nama kolom yang HARUS ADA di file CSV kamu!
# ─────────────────────────────────────────────────────────────────────────────
KRITERIA_COLS  = ["Return_Tahunan", "Volatilitas", "Likuiditas", "Regulasi", "Kemudahan_Modal"]
KRITERIA_LABEL = ["Return Tahunan", "Volatilitas", "Likuiditas", "Regulasi", "Kemudahan Modal"]

# "benefit" = makin besar makin baik (contoh: return tinggi = bagus)
# "cost"    = makin kecil makin baik (contoh: volatilitas rendah = bagus)
KRITERIA_TIPE  = ["benefit", "cost", "benefit", "benefit", "benefit"]

KRITERIA_DESC  = [
    "Keuntungan tahunan aset (%)",
    "Tingkat risiko/fluktuasi harga (%)",
    "Kemudahan aset untuk dicairkan (1–5)",
    "Kepatuhan regulasi & legalitas (1–5)",
    "Kemudahan berinvestasi / modal awal (1–5)",
]

# Warna untuk setiap jenis aset di grafik
COLORS_MAP = {
    "Saham":      "#0066cc",
    "Crypto":     "#f7931a",
    "Emas":       "#ffd700",
    "Reksa Dana": "#00c896"
}

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR (Panel kiri)
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Judul sidebar
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 8px 0;'>
        <div style='font-size:2.4rem;'>📊</div>
        <div style='font-size:1.1rem; font-weight:700; color:#e8f4fd; margin-top:4px;'>InvestSmart SPK</div>
        <div style='font-size:0.75rem; color:#7aa8d2;'>Weighted Product Method</div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    # ── FITUR UPLOAD CSV ──
    # Ini bagian yang DIPERBAIKI dari versi sebelumnya!
    # Sekarang user bisa upload file CSV sendiri, tidak perlu hardcode nama file
    st.markdown("### 📁 Upload Data CSV")
    st.markdown("""
    <div class='info-box' style='font-size:0.8rem;'>
    <strong style='color:#7ec8ff;'>Format CSV yang dibutuhkan:</strong><br>
    Kolom wajib: <code>Nama</code>, <code>Jenis</code>,<br>
    <code>Return_Tahunan</code>, <code>Volatilitas</code>,<br>
    <code>Likuiditas</code>, <code>Regulasi</code>,<br>
    <code>Kemudahan_Modal</code>
    </div>
    """, unsafe_allow_html=True)

    # Widget upload file - hanya menerima file .csv
    uploaded_file = st.file_uploader(
        "Pilih file CSV kamu",
        type=["csv"],                           # hanya terima file .csv
        help="Upload file CSV data investasi"
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # Menu navigasi halaman
    nav = st.radio(
        "Navigasi",
        ["🏠 Beranda", "📂 Dataset", "⚙️ Hitung SPK", "📊 Visualisasi", "👥 Profil Kelompok"],
        label_visibility="collapsed"
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.75rem; color:#4a6e8e; text-align:center; padding:8px;'>
        Sistem Pendukung Keputusan<br>Analisis Investasi Digital<br>
        <span style='color:#0066cc;'>Metode: Weighted Product (WP)</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA — Fungsi untuk membaca file CSV yang diupload
# ─────────────────────────────────────────────────────────────────────────────
def load_data_from_upload(file):
    """
    Fungsi ini membaca file CSV yang diupload oleh user.
    Mengembalikan DataFrame jika berhasil, None jika gagal.
    """
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"❌ Gagal membaca file: {e}")
        return None

def validasi_kolom(df):
    """
    Fungsi ini mengecek apakah file CSV memiliki kolom yang dibutuhkan.
    Mengembalikan True jika valid, False jika ada kolom yang kurang.
    """
    kolom_wajib = ["Nama", "Jenis"] + KRITERIA_COLS
    kolom_kurang = [k for k in kolom_wajib if k not in df.columns]

    if kolom_kurang:
        st.error(f"❌ Kolom berikut tidak ditemukan di CSV: **{', '.join(kolom_kurang)}**")
        st.info("💡 Pastikan nama kolom CSV persis sama (huruf besar/kecil diperhatikan)!")
        return False
    return True

# ── Cek apakah user sudah upload file ──
if uploaded_file is not None:
    # Ada file yang diupload → baca filenya
    df_raw = load_data_from_upload(uploaded_file)

    if df_raw is not None:
        # Cek apakah kolomnya valid
        if not validasi_kolom(df_raw):
            st.stop()  # Hentikan program jika kolom tidak valid
        else:
            st.sidebar.success(f"✅ File berhasil dimuat! ({len(df_raw)} baris)")
    else:
        st.stop()
else:
    # Belum ada file yang diupload → tampilkan pesan panduan
    st.markdown("""
    <div class='banner'>
        <div class='banner-title'>📊 InvestSmart — SPK Weighted Product</div>
        <div class='banner-sub'>Sistem Pendukung Keputusan Analisis Investasi Digital</div>
    </div>
    """, unsafe_allow_html=True)

    st.info("👈 **Silakan upload file CSV kamu terlebih dahulu di sidebar kiri!**")

    # Tampilkan panduan format CSV
    st.markdown("<div class='section-title'>📋 Panduan Format File CSV</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
    <p>File CSV kamu harus memiliki <strong style='color:#7ec8ff;'>kolom-kolom berikut</strong> (nama harus sama persis):</p>
    </div>
    """, unsafe_allow_html=True)

    # Tabel contoh format CSV
    contoh_df = pd.DataFrame({
        "No":               [1, 2, 3],
        "Nama":             ["Bitcoin", "BBCA", "Emas 24K"],
        "Jenis":            ["Crypto", "Saham", "Emas"],
        "Return_Tahunan":   [85.5, 12.3, 8.7],
        "Volatilitas":      [70.2, 15.4, 5.1],
        "Likuiditas":       [5, 4, 3],
        "Regulasi":         [2, 5, 5],
        "Kemudahan_Modal":  [4, 4, 3],
    })
    st.dataframe(contoh_df, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class='info-box'>
    <p><strong style='color:#7ec8ff;'>Keterangan kolom:</strong></p>
    <ul>
        <li><code>Nama</code> → Nama aset investasi (teks bebas)</li>
        <li><code>Jenis</code> → Kategori: Saham / Crypto / Emas / Reksa Dana</li>
        <li><code>Return_Tahunan</code> → Keuntungan tahunan dalam % (angka)</li>
        <li><code>Volatilitas</code> → Tingkat risiko dalam % (angka)</li>
        <li><code>Likuiditas</code> → Skor 1–5 (angka bulat)</li>
        <li><code>Regulasi</code> → Skor 1–5 (angka bulat)</li>
        <li><code>Kemudahan_Modal</code> → Skor 1–5 (angka bulat)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # Tombol download contoh CSV
    contoh_csv = contoh_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Contoh File CSV",
        data=contoh_csv,
        file_name="contoh_investasi.csv",
        mime="text/csv",
    )
    st.stop()  # Hentikan program, tunggu user upload file

# ── Dari sini ke bawah, df_raw sudah pasti ada dan valid ──

# Ambil daftar jenis aset yang ada di CSV
JENIS_LIST  = sorted(df_raw["Jenis"].unique().tolist())
COLORS_LIST = [COLORS_MAP.get(j, "#888888") for j in JENIS_LIST]

# ─────────────────────────────────────────────────────────────────────────────
# HALAMAN BERANDA
# ─────────────────────────────────────────────────────────────────────────────
if nav == "🏠 Beranda":
    st.markdown("""
    <div class='banner'>
        <div class='banner-title'>📊 InvestSmart — Sistem Pendukung Keputusan</div>
        <div class='banner-sub'>Analisis & Rekomendasi Aset Investasi Digital Menggunakan Metode Weighted Product</div>
        <div>
            <span class='badge'>🔷 Saham</span>
            <span class='badge'>₿ Crypto</span>
            <span class='badge'>🥇 Emas</span>
            <span class='badge'>📁 Reksa Dana</span>
            <span class='badge'>⚡ WP Method</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Statistik ringkas data yang diupload
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("📋 Total Data",   f"{len(df_raw):,} baris",        f"{len(df_raw)} records")
    with col2: st.metric("💼 Total Aset",   f"{df_raw['Nama'].nunique()}",    "alternatif")
    with col3: st.metric("🎯 Kriteria SPK", f"{len(KRITERIA_COLS)} kriteria", "WP Method")
    with col4: st.metric("🏷️ Jenis Aset",  f"{df_raw['Jenis'].nunique()} jenis", "kategori")

    st.markdown("---")
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown("<div class='section-title'>📌 Tentang Aplikasi</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='info-box'>
        <p>Aplikasi ini adalah <strong style='color:#7ec8ff;'>Sistem Pendukung Keputusan (SPK)</strong>
        yang membantu investor memilih aset investasi digital terbaik.</p>
        <p>Menggunakan <strong style='color:#7ec8ff;'>Metode Weighted Product (WP)</strong>:
        setiap aset dihitung skor-nya berdasarkan bobot kriteria yang bisa kamu atur sendiri,
        lalu diurutkan dari yang terbaik.</p>
        </div>
        """, unsafe_allow_html=True)

        # Penjelasan rumus WP
        st.markdown("<div class='section-title'>🔢 Formula Weighted Product</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='formula-box'>
# LANGKAH 1 — Normalisasi Bobot
  W_j  =  w_j / Σ(w_j)      ← total bobot dijadikan 1

# LANGKAH 2 — Hitung Vektor S (skor tiap alternatif)
  S_i  =  Π ( x_ij ^ +W_j ) ← kriteria Benefit (makin besar makin baik)
  S_i  =  Π ( x_ij ^ -W_j ) ← kriteria Cost    (makin kecil makin baik)

# LANGKAH 3 — Hitung Nilai Preferensi V (peringkat akhir)
  V_i  =  S_i / Σ(S_i)      ← dibagi total semua skor

# LANGKAH 4 — Ranking
  V_i terbesar → Peringkat 1 (TERBAIK)
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        # Diagram pie distribusi jenis aset
        st.markdown("<div class='section-title'>📊 Distribusi Jenis Aset</div>", unsafe_allow_html=True)
        dist = df_raw["Jenis"].value_counts()
        fig, ax = plt.subplots(figsize=(5, 4.5), facecolor="none")
        colors = [COLORS_MAP.get(j, "#888") for j in dist.index]
        wedges, texts, autotexts = ax.pie(
            dist.values, labels=dist.index, colors=colors,
            autopct='%1.1f%%', startangle=90, pctdistance=0.75,
            wedgeprops=dict(width=0.6, edgecolor='#0a0f1e', linewidth=2),
            textprops=dict(color='#b0c9e8', fontsize=10)
        )
        for at in autotexts:
            at.set_color('white'); at.set_fontsize(9); at.set_fontweight('bold')
        ax.set_facecolor("none"); fig.patch.set_alpha(0)
        ax.set_title("Komposisi Jenis Aset", color="#e8f4fd", fontsize=11, fontweight='bold', pad=14)
        st.pyplot(fig)

        # Tabel kriteria WP
        st.markdown("<div class='section-title'>📋 Kriteria WP</div>", unsafe_allow_html=True)
        kriteria_df = pd.DataFrame({
            "Kriteria": KRITERIA_LABEL,
            "Tipe":     ["✅ Benefit" if t == "benefit" else "❌ Cost" for t in KRITERIA_TIPE],
        })
        st.dataframe(kriteria_df, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# HALAMAN DATASET
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "📂 Dataset":
    st.markdown("""
    <div class='banner'>
        <div class='banner-title'>📂 Dataset Investasi Digital</div>
        <div class='banner-sub'>Lihat dan filter data yang sudah kamu upload</div>
    </div>
    """, unsafe_allow_html=True)

    # Filter dan pencarian data
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_jenis = st.multiselect(
            "🔷 Filter Jenis Aset",
            options=JENIS_LIST,
            default=JENIS_LIST
        )
    with col2:
        search_aset = st.text_input("🔍 Cari Nama Aset", placeholder="Contoh: Bitcoin, BBCA...")
    with col3:
        sort_col = st.selectbox("📊 Urutkan Berdasarkan",
            options=["No"] + KRITERIA_COLS,
            format_func=lambda x: {"No": "No (Default)"}.get(x, x)
        )

    # Terapkan filter ke dataframe
    df_show = df_raw[df_raw["Jenis"].isin(filter_jenis)].copy()
    if search_aset:
        df_show = df_show[df_show["Nama"].str.contains(search_aset, case=False, na=False)]
    if sort_col != "No":
        asc = (sort_col == "Volatilitas")  # Volatilitas: cost → urutkan ascending (kecil lebih baik)
        df_show = df_show.sort_values(sort_col, ascending=asc)

    st.markdown(
        f"<div class='section-title'>📊 Tabel Dataset "
        f"<span style='color:#7aa8d2; font-size:0.85rem; font-weight:400;'>"
        f"({len(df_show)} baris)</span></div>",
        unsafe_allow_html=True
    )

    # Tampilkan tabel dengan warna gradient
    st.dataframe(
        df_show.style
            .format({"Return_Tahunan": "{:.2f}%", "Volatilitas": "{:.2f}%"})
            .background_gradient(subset=["Return_Tahunan"], cmap="Blues")
            .background_gradient(subset=["Volatilitas"],    cmap="Reds_r")
            .background_gradient(subset=["Likuiditas", "Regulasi", "Kemudahan_Modal"], cmap="Greens"),
        use_container_width=True, height=500,
    )

    st.markdown("---")

    # Statistik deskriptif
    with st.expander("📊 Statistik Deskriptif Dataset"):
        st.dataframe(df_raw[KRITERIA_COLS].describe().round(3), use_container_width=True)

    # Penjelasan kolom
    with st.expander("📋 Penjelasan Kolom Dataset"):
        desc_df = pd.DataFrame({
            "Kolom":      ["No", "Nama", "Jenis"] + KRITERIA_LABEL,
            "Tipe":       ["ID", "Teks", "Kategori"] + ["✅ Benefit" if t == "benefit" else "❌ Cost" for t in KRITERIA_TIPE],
            "Keterangan": [
                "Nomor urut aset",
                "Nama lengkap aset investasi",
                "Kategori: Saham / Crypto / Emas / Reksa Dana",
            ] + KRITERIA_DESC,
        })
        st.dataframe(desc_df, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# HALAMAN HITUNG SPK
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "⚙️ Hitung SPK":
    st.markdown("""
    <div class='banner'>
        <div class='banner-title'>⚙️ Perhitungan SPK — Weighted Product</div>
        <div class='banner-sub'>Atur bobot kriteria, lalu klik tombol untuk menghitung peringkat</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Input Bobot ──
    st.markdown("<div class='section-title'>🎚️ Input Bobot Kriteria (Geser Slider)</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
    <p>Geser slider untuk mengatur kepentingan setiap kriteria.
    Bobot akan <strong style='color:#7ec8ff;'>dinormalisasi otomatis</strong> (total = 1.00).</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        # Slider bobot untuk setiap kriteria (nilai 1–10)
        w_return = st.slider("📈 Return Tahunan     ✅ Benefit", 1, 10, 5, help="Semakin tinggi return, semakin baik")
        w_vol    = st.slider("⚠️ Volatilitas         ❌ Cost",    1, 10, 4, help="Semakin rendah volatilitas, semakin aman")
        w_liq    = st.slider("💧 Likuiditas          ✅ Benefit", 1, 10, 3, help="Semakin mudah dicairkan, semakin baik")
        w_reg    = st.slider("🏛️ Regulasi            ✅ Benefit", 1, 10, 3, help="Semakin patuh regulasi, semakin aman")
        w_modal  = st.slider("💰 Kemudahan Modal     ✅ Benefit", 1, 10, 3, help="Semakin mudah modalnya, semakin baik")

    # Normalisasi bobot: bagi tiap bobot dengan total semua bobot
    bobot_asli = [w_return, w_vol, w_liq, w_reg, w_modal]
    total_w    = sum(bobot_asli)
    W_norm     = [round(b / total_w, 6) for b in bobot_asli]

    with col2:
        # Tampilkan tabel bobot yang sudah dinormalisasi
        st.markdown("<div class='section-title'>📋 Bobot Ternormalisasi</div>", unsafe_allow_html=True)
        w_df = pd.DataFrame({
            "Kriteria":    KRITERIA_LABEL,
            "Tipe":        ["✅ Benefit" if t == "benefit" else "❌ Cost" for t in KRITERIA_TIPE],
            "Bobot Asli":  bobot_asli,
            "W Normal":    W_norm,
            "Eksponen WP": [round(w if t == "benefit" else -w, 6) for w, t in zip(W_norm, KRITERIA_TIPE)],
        })
        st.dataframe(w_df, use_container_width=True, hide_index=True)
        st.markdown(f"""
        <div class='info-box'>
        <p>Total bobot asli: <strong style='color:#7ec8ff;'>{total_w}</strong></p>
        <p>Total bobot normal: <strong style='color:#00c896;'>1.000000</strong></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Pengaturan Tambahan ──
    st.markdown("<div class='section-title'>⚙️ Pengaturan Tambahan</div>", unsafe_allow_html=True)
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        jenis_filter = st.multiselect(
            "🔷 Jenis Aset yang Dianalisis",
            options=JENIS_LIST, default=JENIS_LIST,
        )
    with col_f2:
        top_n = st.selectbox("🏆 Tampilkan Top-N Peringkat",
                             options=[5, 10, 15, 20, 30, 50, "Semua"], index=2)
    with col_f3:
        show_steps = st.selectbox("📄 Detail Langkah Perhitungan",
                                  options=["Ya, tampilkan detail", "Tidak, hasil saja"])

    st.markdown("---")

    # ── Tombol Hitung ──
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        hitung = st.button("🚀 MULAI HITUNG SPK — WEIGHTED PRODUCT", use_container_width=True)

    if hitung:
        # Filter data berdasarkan jenis aset yang dipilih
        df_wp = df_raw[df_raw["Jenis"].isin(jenis_filter)].copy().reset_index(drop=True)

        if len(df_wp) == 0:
            st.error("❌ Tidak ada aset terpilih! Pilih minimal 1 jenis aset.")
            st.stop()

        with st.spinner("⏳ Menghitung Weighted Product..."):
            import time; time.sleep(0.5)

        # ── LANGKAH 1: Ambil Matriks Keputusan ──
        # X adalah tabel nilai kriteria untuk semua aset (baris=aset, kolom=kriteria)
        X = df_wp[KRITERIA_COLS].values.astype(float)

        # Pastikan semua nilai positif (WP tidak bisa dengan angka 0 atau negatif)
        for j in range(X.shape[1]):
            if X[:, j].min() <= 0:
                X[:, j] = X[:, j] - X[:, j].min() + 0.001  # geser ke positif

        if show_steps == "Ya, tampilkan detail":
            st.markdown("<div class='section-title'>📋 Langkah 1 — Matriks Keputusan (X)</div>", unsafe_allow_html=True)
            mx = pd.DataFrame(X, columns=KRITERIA_LABEL, index=df_wp["Nama"])
            st.dataframe(mx.round(4).head(10), use_container_width=True)
            st.caption("*Ditampilkan 10 baris pertama saja.*")

        # ── LANGKAH 2: Bobot ──
        W = np.array(W_norm)

        if show_steps == "Ya, tampilkan detail":
            st.markdown("<div class='section-title'>📋 Langkah 2 — Bobot Ternormalisasi (W)</div>", unsafe_allow_html=True)
            st.dataframe(w_df, use_container_width=True, hide_index=True)

        # ── LANGKAH 3: Hitung Vektor S ──
        # S_i = hasil perkalian semua (nilai^bobot) untuk setiap aset
        S = np.ones(len(df_wp))   # mulai dari 1 (identitas perkalian)
        for j, (w, t) in enumerate(zip(W, KRITERIA_TIPE)):
            if t == "benefit":
                S *= X[:, j] ** w    # benefit → eksponen positif
            else:
                S *= X[:, j] ** (-w) # cost    → eksponen negatif

        if show_steps == "Ya, tampilkan detail":
            st.markdown("<div class='section-title'>📋 Langkah 3 — Vektor S</div>", unsafe_allow_html=True)
            s_df = pd.DataFrame({"Nama Aset": df_wp["Nama"], "Jenis": df_wp["Jenis"], "Nilai S_i": S})
            st.dataframe(s_df.style.format({"Nilai S_i": "{:.8f}"}),
                         use_container_width=True, hide_index=True, height=300)

        # ── LANGKAH 4: Hitung Vektor V ──
        # V_i = S_i dibagi jumlah semua S → nilai preferensi akhir (0 < V < 1)
        V = S / S.sum()

        if show_steps == "Ya, tampilkan detail":
            st.markdown("<div class='section-title'>📋 Langkah 4 — Vektor V (Nilai Preferensi)</div>", unsafe_allow_html=True)
            v_df_show = pd.DataFrame({
                "Nama Aset": df_wp["Nama"],
                "Jenis":     df_wp["Jenis"],
                "Nilai S_i": S,
                "Nilai V_i": V,
                "V_i (%)":   V * 100,
            })
            st.dataframe(
                v_df_show.style.format({
                    "Nilai S_i": "{:.8f}",
                    "Nilai V_i": "{:.8f}",
                    "V_i (%)":  "{:.5f}%",
                }),
                use_container_width=True, hide_index=True, height=300,
            )

        # ── LANGKAH 5: Ranking ──
        df_result = df_wp.copy()
        df_result["Skor_S"]   = S
        df_result["Skor_V"]   = V
        df_result["Peringkat"] = df_result["Skor_V"].rank(ascending=False).astype(int)
        df_result = df_result.sort_values("Peringkat").reset_index(drop=True)

        # Simpan hasil ke session_state agar bisa dipakai di halaman Visualisasi
        st.session_state["df_result"] = df_result

        # ── Tampilkan Hasil ──
        st.markdown("---")
        st.success("✅ Perhitungan Weighted Product berhasil!")

        n_show = len(df_result) if top_n == "Semua" else int(top_n)
        st.markdown(f"<div class='section-title'>🏆 Tabel Hasil Perangkingan — Top {n_show}</div>",
                    unsafe_allow_html=True)

        df_top = df_result.head(n_show).copy()

        # Fungsi untuk menampilkan emoji medali di kolom peringkat
        def render_rank(r):
            if r == 1:   return "🥇 #1"
            elif r == 2: return "🥈 #2"
            elif r == 3: return "🥉 #3"
            return f"   #{r}"

        df_display = pd.DataFrame({
            "Peringkat":       df_top["Peringkat"].apply(render_rank),
            "Nama Aset":       df_top["Nama"],
            "Jenis":           df_top["Jenis"],
            "Return (%)":      df_top["Return_Tahunan"].round(2),
            "Volatilitas (%)": df_top["Volatilitas"].round(2),
            "Likuiditas":      df_top["Likuiditas"],
            "Regulasi":        df_top["Regulasi"],
            "Kemudahan Modal": df_top["Kemudahan_Modal"],
            "Skor V_i":        df_top["Skor_V"].round(8),
        })

        st.dataframe(
            df_display.style
                .background_gradient(subset=["Skor V_i"],       cmap="Blues")
                .background_gradient(subset=["Return (%)"],      cmap="Greens")
                .background_gradient(subset=["Volatilitas (%)"], cmap="Reds_r"),
            use_container_width=True, hide_index=True,
            height=min(80 + n_show * 38, 600),
        )

        # ── Podium Top 3 ──
        st.markdown("<div class='section-title'>🎖️ Podium Rekomendasi Terbaik</div>", unsafe_allow_html=True)
        p_cols  = st.columns(3)
        emojis  = ["🥇", "🥈", "🥉"]
        borders = ["#ffd700", "#c0c0c0", "#cd7f32"]
        labels  = ["TERBAIK", "2ND BEST", "3RD BEST"]

        for i, (col_pod, (_, row)) in enumerate(zip(p_cols, df_result.head(3).iterrows())):
            with col_pod:
                jenis_color = COLORS_MAP.get(row["Jenis"], "#888")
                st.markdown(f"""
                <div class='profile-card' style='border-color:{borders[i]}; border-width:2px;'>
                    <div style='font-size:2.8rem;'>{emojis[i]}</div>
                    <div style='font-size:0.7rem; color:{borders[i]}; font-weight:700; letter-spacing:2px; margin-top:4px;'>{labels[i]}</div>
                    <div style='font-size:1.05rem; font-weight:700; color:#e8f4fd; margin-top:10px;'>{row['Nama']}</div>
                    <div style='font-size:0.78rem; color:{jenis_color}; margin-top:4px; font-weight:600;'>{row['Jenis']}</div>
                    <hr style='border-color:#1e3a6e; margin:12px 0;'>
                    <div style='font-size:0.82rem; color:#00c896; font-weight:700;'>Skor V = {row['Skor_V']:.8f}</div>
                    <div style='font-size:0.78rem; color:#b0c9e8; margin-top:6px;'>
                        Return: {row['Return_Tahunan']:.2f}% &nbsp;|&nbsp; Volatilitas: {row['Volatilitas']:.2f}%</div>
                    <div style='font-size:0.78rem; color:#b0c9e8; margin-top:2px;'>
                        Likuiditas: {row['Likuiditas']} &nbsp;|&nbsp;
                        Regulasi: {row['Regulasi']} &nbsp;|&nbsp;
                        Modal: {row['Kemudahan_Modal']}</div>
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HALAMAN VISUALISASI
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "📊 Visualisasi":
    st.markdown("""
    <div class='banner'>
        <div class='banner-title'>📊 Visualisasi Data Analitik</div>
        <div class='banner-sub'>Grafik eksplorasi dataset investasi menggunakan Matplotlib & Seaborn</div>
    </div>
    """, unsafe_allow_html=True)

    # Warna latar grafik (dark theme)
    DARK_BG  = "#060f22"
    DARK_AX  = "#0d1f3c"
    TEXT_CLR = "#b0c9e8"
    TITLE_CLR= "#e8f4fd"

    # Fungsi helper untuk memberi style gelap pada grafik matplotlib
    def style_ax(ax, title="", xlabel="", ylabel=""):
        ax.set_facecolor(DARK_AX)
        for spine in ["top", "right"]:   ax.spines[spine].set_visible(False)
        for spine in ["bottom", "left"]: ax.spines[spine].set_color('#1e3a6e')
        ax.tick_params(colors=TEXT_CLR, labelsize=8)
        ax.xaxis.label.set_color(TEXT_CLR)
        ax.yaxis.label.set_color(TEXT_CLR)
        if title:  ax.set_title(title,   color=TITLE_CLR, fontsize=11, fontweight='bold', pad=10)
        if xlabel: ax.set_xlabel(xlabel, fontsize=9)
        if ylabel: ax.set_ylabel(ylabel, fontsize=9)
        ax.grid(color='#1a3a6e', alpha=0.4, linewidth=0.6)

    # ── Grafik 1: Scatter Return vs Volatilitas ──
    st.markdown("<div class='section-title'>📈 Grafik 1: Return vs Volatilitas</div>", unsafe_allow_html=True)
    fig1, ax1 = plt.subplots(figsize=(11, 5.5), facecolor=DARK_BG)
    for jenis in JENIS_LIST:
        sub   = df_raw[df_raw["Jenis"] == jenis]
        color = COLORS_MAP.get(jenis, "#888")
        ax1.scatter(sub["Volatilitas"], sub["Return_Tahunan"],
                    c=color, label=jenis, s=70, alpha=0.80,
                    edgecolors='white', linewidth=0.4)
        for _, row in sub.iterrows():
            ax1.annotate(row["Nama"], (row["Volatilitas"], row["Return_Tahunan"]),
                         fontsize=4.5, color=TEXT_CLR, alpha=0.65,
                         xytext=(3, 3), textcoords='offset points')
    ax1.axhline(0, color='#ff4444', linestyle='--', alpha=0.5, linewidth=0.8, label='Return = 0%')
    style_ax(ax1, "Return Tahunan vs Volatilitas per Aset", "Volatilitas (%)", "Return Tahunan (%)")
    ax1.legend(loc='upper right', facecolor='#0d1f3c', edgecolor='#1e3a6e', labelcolor=TEXT_CLR, fontsize=8)
    fig1.tight_layout()
    st.pyplot(fig1)
    st.caption("📌 Aset **ideal** berada di **kiri atas**: Return tinggi & Volatilitas rendah.")

    st.markdown("---")

    # ── Grafik 2 & 3 ──
    col_g2, col_g3 = st.columns(2)

    with col_g2:
        st.markdown("<div class='section-title'>📦 Grafik 2: Distribusi Return per Jenis</div>", unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(6, 4.5), facecolor=DARK_BG)
        data_box  = [df_raw[df_raw["Jenis"] == j]["Return_Tahunan"].values for j in JENIS_LIST]
        bplot = ax2.boxplot(data_box, labels=JENIS_LIST, patch_artist=True,
                            medianprops=dict(color='white', linewidth=2),
                            whiskerprops=dict(color=TEXT_CLR),
                            capprops=dict(color=TEXT_CLR),
                            flierprops=dict(marker='o', color='#ff6666', alpha=0.5, markersize=4))
        for patch, jenis in zip(bplot['boxes'], JENIS_LIST):
            patch.set_facecolor(COLORS_MAP.get(jenis, "#888"))
            patch.set_alpha(0.75)
        style_ax(ax2, "Distribusi Return Tahunan", "Jenis Aset", "Return (%)")
        ax2.tick_params(axis='x', rotation=15)
        fig2.tight_layout()
        st.pyplot(fig2)

    with col_g3:
        st.markdown("<div class='section-title'>📊 Grafik 3: Rata-rata Skor Kriteria per Jenis</div>", unsafe_allow_html=True)
        fig3, ax3 = plt.subplots(figsize=(6, 4.5), facecolor=DARK_BG)
        kriteria_bar = ["Likuiditas", "Regulasi", "Kemudahan_Modal"]
        label_bar    = ["Likuiditas", "Regulasi", "Kemudahan Modal"]
        x     = np.arange(len(kriteria_bar))
        width = 0.2
        for idx, jenis in enumerate(JENIS_LIST):
            means = [df_raw[df_raw["Jenis"] == jenis][k].mean() for k in kriteria_bar]
            ax3.bar(x + idx * width, means, width, label=jenis,
                    color=COLORS_MAP.get(jenis, "#888"), alpha=0.85)
        ax3.set_xticks(x + width * 1.5)
        ax3.set_xticklabels(label_bar, fontsize=8)
        ax3.set_ylim(0, 6)
        style_ax(ax3, "Rata-rata Skor Kriteria (1–5)", "Kriteria", "Nilai Rata-rata")
        ax3.legend(loc='upper right', facecolor='#0d1f3c', edgecolor='#1e3a6e',
                   labelcolor=TEXT_CLR, fontsize=7)
        fig3.tight_layout()
        st.pyplot(fig3)

    st.markdown("---")

    # ── Grafik 4: Heatmap Korelasi ──
    st.markdown("<div class='section-title'>🔥 Grafik 4: Heatmap Korelasi Antar Kriteria</div>", unsafe_allow_html=True)
    fig4, ax4 = plt.subplots(figsize=(8, 4.5), facecolor=DARK_BG)
    corr_m = df_raw[KRITERIA_COLS].corr()
    corr_m.index   = KRITERIA_LABEL
    corr_m.columns = KRITERIA_LABEL
    mask = np.triu(np.ones_like(corr_m, dtype=bool))
    sns.heatmap(corr_m, mask=mask, annot=True, fmt=".2f", cmap="Blues", ax=ax4,
                linewidths=0.5, linecolor="#0a0f1e",
                annot_kws={"size": 10, "color": "white", "weight": "bold"},
                cbar_kws={"shrink": 0.7})
    ax4.set_facecolor(DARK_AX)
    ax4.tick_params(colors=TEXT_CLR, labelsize=8)
    ax4.set_title("Korelasi Antar Kriteria Investasi", color=TITLE_CLR, fontsize=11, fontweight='bold', pad=10)
    fig4.tight_layout()
    st.pyplot(fig4)

    st.markdown("---")

    # ── Grafik 5: Violin Plot Volatilitas ──
    st.markdown("<div class='section-title'>🎻 Grafik 5: Distribusi Volatilitas per Jenis (Violin)</div>", unsafe_allow_html=True)
    fig5, ax5 = plt.subplots(figsize=(10, 4.5), facecolor=DARK_BG)
    parts = ax5.violinplot(
        [df_raw[df_raw["Jenis"] == j]["Volatilitas"].values for j in JENIS_LIST],
        positions=range(len(JENIS_LIST)), showmedians=True
    )
    for i, (pc, jenis) in enumerate(zip(parts['bodies'], JENIS_LIST)):
        pc.set_facecolor(COLORS_MAP.get(jenis, "#888"))
        pc.set_alpha(0.7)
    parts['cmedians'].set_color('white')
    parts['cbars'].set_color(TEXT_CLR)
    parts['cmins'].set_color(TEXT_CLR)
    parts['cmaxes'].set_color(TEXT_CLR)
    ax5.set_xticks(range(len(JENIS_LIST)))
    ax5.set_xticklabels(JENIS_LIST, color=TEXT_CLR, fontsize=9)
    style_ax(ax5, "Distribusi Volatilitas per Jenis Aset", "Jenis Aset", "Volatilitas (%)")
    patches = [mpatches.Patch(color=COLORS_MAP.get(j, "#888"), label=j) for j in JENIS_LIST]
    ax5.legend(handles=patches, loc='upper right', facecolor='#0d1f3c',
               edgecolor='#1e3a6e', labelcolor=TEXT_CLR, fontsize=8)
    fig5.tight_layout()
    st.pyplot(fig5)

    # ── Grafik 6: Hasil SPK (hanya tampil setelah hitung) ──
    if "df_result" in st.session_state:
        st.markdown("---")
        st.markdown("<div class='section-title'>🏆 Grafik 6: Hasil Perangkingan SPK — Top 20</div>", unsafe_allow_html=True)
        df_res   = st.session_state["df_result"].head(20)
        bar_cols = [COLORS_MAP.get(j, "#888") for j in df_res["Jenis"]]

        fig6, ax6 = plt.subplots(figsize=(11, 7), facecolor=DARK_BG)
        bars = ax6.barh(range(len(df_res)), df_res["Skor_V"].values,
                        color=bar_cols, edgecolor='none', height=0.65)
        ax6.set_yticks(range(len(df_res)))
        ax6.set_yticklabels([f"#{i+1}  {n}" for i, n in enumerate(df_res["Nama"])],
                            fontsize=8, color=TEXT_CLR)
        for bar, val in zip(bars, df_res["Skor_V"].values):
            ax6.text(val + df_res["Skor_V"].max() * 0.005,
                     bar.get_y() + bar.get_height() / 2,
                     f"{val:.6f}", va='center', ha='left', color=TEXT_CLR, fontsize=7)
        style_ax(ax6, "Peringkat Aset Investasi — Skor WP (V_i)", "Skor V_i", "")
        ax6.invert_yaxis()
        patches = [mpatches.Patch(color=c, label=j) for j, c in COLORS_MAP.items() if j in JENIS_LIST]
        ax6.legend(handles=patches, loc='lower right', facecolor='#0d1f3c',
                   edgecolor='#1e3a6e', labelcolor=TEXT_CLR, fontsize=8)
        fig6.tight_layout()
        st.pyplot(fig6)
    else:
        st.info("💡 Jalankan perhitungan di halaman **⚙️ Hitung SPK** dulu untuk melihat grafik ranking.")

# ─────────────────────────────────────────────────────────────────────────────
# HALAMAN PROFIL KELOMPOK
# ─────────────────────────────────────────────────────────────────────────────
elif nav == "👥 Profil Kelompok":
    st.markdown("""
    <div class='banner'>
        <div class='banner-title'>👥 Profil Kelompok</div>
        <div class='banner-sub'>Anggota tim pengembang — SPK Analisis Investasi Digital</div>
    </div>
    """, unsafe_allow_html=True)

    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.markdown("""
        <div class='info-box'>
            <p><strong style='color:#7ec8ff;'>Judul Proyek:</strong><br>
            Aplikasi Analisis dan Rekomendasi Aset Investasi Digital<br>Menggunakan Metode Weighted Product</p>
            <p><strong style='color:#7ec8ff;'>Metode SPK:</strong> Weighted Product (WP)</p>
            <p><strong style='color:#7ec8ff;'>Tema:</strong> Finansial & Investasi</p>
        </div>
        """, unsafe_allow_html=True)
    with col_i2:
        st.markdown("""
        <div class='info-box'>
            <p><strong style='color:#7ec8ff;'>Mata Kuliah:</strong> Sistem Cerdas dan Pendukung Keputusan</p>
            <p><strong style='color:#7ec8ff;'>Semester:</strong> 4</p>
            <p><strong style='color:#7ec8ff;'>Framework:</strong> Python + Streamlit</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='section-title'>🧑‍💻 Anggota Kelompok</div>", unsafe_allow_html=True)

    # =====================================================================
    # GANTI DATA INI DENGAN NAMA & NIM ANGGOTA KELOMPOK LO!
    # =====================================================================
    anggota = [
        {"nama": "Nama Anggota 1", "nim": "NIM000001", "peran": "Project Leader",         "emoji": "👨‍💼"},
        {"nama": "Nama Anggota 2", "nim": "NIM000002", "peran": "Backend / WP Developer",  "emoji": "👨‍💻"},
        {"nama": "Nama Anggota 3", "nim": "NIM000003", "peran": "Data Analyst",            "emoji": "📊"},
        {"nama": "Nama Anggota 4", "nim": "NIM000004", "peran": "UI/UX Streamlit",         "emoji": "🎨"},
        {"nama": "Nama Anggota 5", "nim": "NIM000005", "peran": "Dokumentasi & Laporan",   "emoji": "📝"},
    ]
    # =====================================================================

    cols = st.columns(len(anggota))
    for col, a in zip(cols, anggota):
        with col:
            st.markdown(f"""
            <div class='profile-card'>
                <div class='profile-avatar'>{a['emoji']}</div>
                <div style='font-size:0.92rem; font-weight:700; color:#e8f4fd;'>{a['nama']}</div>
                <div style='font-size:0.76rem; color:#7aa8d2; margin-top:4px;'>{a['nim']}</div>
                <hr style='border-color:#1e3a6e; margin:10px 0;'>
                <div style='font-size:0.74rem; color:#0099ff; font-weight:600;'>{a['peran']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='section-title'>🛠️ Teknologi yang Digunakan</div>", unsafe_allow_html=True)
    techs = [
        ("🐍", "Python 3",   "Bahasa pemrograman utama"),
        ("🌊", "Streamlit",  "Framework GUI web interaktif"),
        ("🐼", "Pandas",     "Manipulasi & analisis data"),
        ("🔢", "NumPy",      "Komputasi numerik metode WP"),
        ("📊", "Matplotlib", "Visualisasi grafik & chart"),
        ("🎨", "Seaborn",    "Heatmap & statistical plots"),
    ]
    tech_cols = st.columns(len(techs))
    for col, (icon, name, desc) in zip(tech_cols, techs):
        with col:
            st.markdown(f"""
            <div class='profile-card'>
                <div style='font-size:1.8rem;'>{icon}</div>
                <div style='font-size:0.85rem; font-weight:700; color:#e8f4fd; margin-top:8px;'>{name}</div>
                <div style='font-size:0.7rem; color:#7aa8d2; margin-top:4px;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; color:#4a6e8e; font-size:0.82rem; padding:20px;'>
        © 2025 InvestSmart SPK &nbsp;—&nbsp;
        Tugas Akhir Sistem Cerdas dan Pendukung Keputusan<br>
        <span style='color:#0066cc;'>Metode Weighted Product • Python • Streamlit</span>
    </div>
    """, unsafe_allow_html=True)