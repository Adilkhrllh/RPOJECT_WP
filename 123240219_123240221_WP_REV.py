import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Page config & Style ───────────────────────────────────────────────────────
st.set_page_config(page_title="SPK Crypto – Metode WP", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] { background: #0f172a; }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    .stButton > button { background: #2563eb; color: white; border-radius: 8px; font-weight: 600; width: 100%; }
    .stButton > button:hover { background: #1d4ed8; }
    .metric-card { background: #1e293b; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.5rem; text-align: center; }
    .metric-card h4 { margin: 0 0 4px; font-size: 0.8rem; color: #94a3b8; }
    .metric-card p  { margin: 0; font-size: 1.4rem; font-weight: 700; color: #f1f5f9; }
</style>
""", unsafe_allow_html=True)

# ── Load dataset ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("CRYPTO_DATASET.csv")
    df = df[["Crypto", "Close", "Volume", "Market Cap", "Return", "Volatility"]].copy()
    df.columns = ["Crypto", "Close", "Volume", "Market_Cap", "Return", "Volatility"]
    return df

df = load_data()

# ── Sidebar Navigation ────────────────────────────────────────────────────────
st.sidebar.markdown("## Crypto\n**Metode: Weighted Product (WP)**\n---")
menu = st.sidebar.radio("Navigasi", ["🖿 Dataset", "⚙︎ Hitung SPK", "↗ Visualisasi", "☻ Profil Kelompok"])
st.sidebar.markdown("---")

# Global variables untuk kriteria
KRITERIA_INFO = pd.DataFrame({
    "Kriteria": ["Close", "Volume", "Market Cap", "Return", "Volatility"],
    "Jenis": ["Benefit ↑", "Benefit ↑", "Benefit ↑", "Benefit ↑", "Cost ↓"],
    "Keterangan": ["Harga penutupan rata-rata harian", "Volume perdagangan rata-rata harian", "Kapitalisasi pasar rata-rata", "Return/imbal hasil harian rata-rata", "Volatilitas (standar deviasi return)"]
})

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 1 – DATASET
# ═══════════════════════════════════════════════════════════════════════════════
if menu == "🖿 Dataset":
    st.title("🖿 Dataset Cryptocurrency")
    st.markdown("Dataset berisi **250 cryptocurrency** dengan 5 kriteria penilaian.")

    # Ringkasan statistik cepat
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="metric-card"><h4>Total Aset</h4><p>{len(df)} Crypto</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><h4>Harga Tertinggi</h4><p>${df["Close"].max():,.2f}</p></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><h4>Market Cap Terbesar</h4><p>${df["Market_Cap"].max()/1e12:.2f}T</p></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-card"><h4>Volatilitas Terendah</h4><p>{df["Volatility"].min():.4f}</p></div>', unsafe_allow_html=True)
    st.markdown("---")

    # Filter & Search
    col_cari, col_sort = st.columns([2, 1])
    search = col_cari.text_input("🔍 Cari nama crypto", placeholder="contoh: Bitcoin, Ethereum...")
    sort_col = col_sort.selectbox("Urutkan berdasarkan", ["Market_Cap", "Close", "Volume", "Return", "Volatility"])

    df_show = df[df["Crypto"].str.contains(search, case=False, na=False)] if search else df.copy()
    df_show = df_show.sort_values(sort_col, ascending=False).reset_index(drop=True)
    df_show.index += 1

    # Formatter tampilan tabel agar rapi
    df_display = df_show.copy()
    df_display["Close"] = df_display["Close"].apply(lambda x: f"${x:,.4f}")
    df_display["Volume"] = df_display["Volume"].apply(lambda x: f"${x/1e9:.2f}B")
    df_display["Market_Cap"] = df_display["Market_Cap"].apply(lambda x: f"${x/1e9:.2f}B")
    df_display["Return"] = df_display["Return"].apply(lambda x: f"{x:.4%}")
    df_display["Volatility"] = df_display["Volatility"].apply(lambda x: f"{x:.4f}")
    
    st.dataframe(df_display, use_container_width=True, height=400)
    st.markdown("---")
    st.subheader("Keterangan Kriteria")
    st.table(KRITERIA_INFO.set_index("Kriteria"))

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 2 – HITUNG SPK
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "⚙︎ Hitung SPK":
    st.title("⚙︎ Perhitungan SPK – Weighted Product (WP)")
    st.subheader("1. Atur Bobot Kriteria")

    col1, col2, col3 = st.columns(3)
    col4, col5, _ = st.columns(3)
    w_close = col1.slider("Close (Harga)", 1, 10, 5)
    w_volume = col2.slider("Volume", 1, 10, 4)
    w_marketcap = col3.slider("Market Cap", 1, 10, 6)
    w_return = col4.slider("Return", 1, 10, 7)
    w_volatility = col5.slider("Volatility", 1, 10, 5)

    bobot_asli = np.array([w_close, w_volume, w_marketcap, w_return, w_volatility], dtype=float)
    bobot_normalisasi = bobot_asli / bobot_asli.sum()

    st.markdown("---")
    top_n = st.number_input("Tampilkan Top N Crypto", min_value=5, max_value=250, value=20, step=5)
    st.markdown("---")

    if st.button("🚀 Hitung WP & Tampilkan Hasil"):
        with st.spinner("Menghitung..."):
            data = df[(df["Close"] > 0) & (df["Volume"] > 0) & (df["Market_Cap"] > 0)].copy()
            
            # Normalisasi linear khusus Return agar bernilai positif (menghindari hasil pangkat bilangan imajiner)
            data["Return_adj"] = ((data["Return"] - data["Return"].min()) / (data["Return"].max() - data["Return"].min())) + 1e-6
            data["Volatility_adj"] = data["Volatility"].copy()

            kolom = ["Close", "Volume", "Market_Cap", "Return_adj", "Volatility_adj"]
            tipe = ["benefit", "benefit", "benefit", "benefit", "cost"]

            # Perhitungan Vektor S
            S = np.ones(len(data))
            for i, (col, t, w) in enumerate(zip(kolom, tipe, bobot_normalisasi)):
                S *= data[col].values.astype(float) ** (w if t == "benefit" else -w)
            data["S"] = S

            # Perhitungan Vektor V
            data["V"] = data["S"] / data["S"].sum()
            data = data.sort_values("V", ascending=False).reset_index(drop=True)
            data.index += 1
            data["Peringkat"] = data.index

            # Simpan hasil ke session state untuk halaman visualisasi
            st.session_state["hasil"], st.session_state["top_n"] = data, top_n

        st.success("✅ Perhitungan selesai!")
        st.markdown("---")

        # ── EXPANDER: Langkah Perhitungan Terstruktur & Simple ──
        with st.expander("🔍 Lihat Langkah-Langkah Perhitungan Matematika WP"):
            st.markdown("#### **Langkah 1: Normalisasi Bobot ($W_j$)**")
            st.markdown("Memperbaiki bobot agar total $\sum W_j = 1")
            w_df = pd.DataFrame({
                "Kriteria": KRITERIA_INFO["Kriteria"],
                "Bobot Input": bobot_asli.astype(int),
                "Bobot Ternormalisasi (W)": [f"{w:.4f}" for w in bobot_normalisasi],
                "Sifat Pangkat": ["benefit", "benefit", "benefit", "benefit", "cost"]
            })
            st.table(w_df.set_index("Kriteria"))

            st.markdown("#### **Langkah 2: Menghitung Vektor $S_i$ (Sampel 5 Data Teratas)**")
            st.markdown("Perkalian matriks kriteria pangkat bobot:")
            st.dataframe(data[["Crypto", "Close", "Volume", "Market_Cap", "Return_adj", "Volatility_adj", "S"]].head(5).set_index("Crypto"), use_container_width=True)

            st.markdown("#### **Langkah 3: Menghitung Vektor $V_i$ (Nilai Preferensi Akhir)**")
            st.markdown("Pembagian komponen:")
            st.info(f"Total Nilai $\sum S$ seluruh alternatif = **{data['S'].sum():.6f}**")
            st.dataframe(data[["Peringkat", "Crypto", "S", "V"]].head(5).set_index("Peringkat"), use_container_width=True)

        st.markdown("---")
        st.subheader(f"🏆 Hasil Perangkingan – Top {top_n}")

        # Tampilan tabel utama peringkat
        hasil = data.head(top_n).copy()
        hasil_display = hasil[["Peringkat", "Crypto", "Close", "Volume", "Market_Cap", "Return", "Volatility", "V"]].copy()
        hasil_display["Close"] = hasil_display["Close"].apply(lambda x: f"${x:,.4f}")
        hasil_display["Volume"] = hasil_display["Volume"].apply(lambda x: f"${x/1e9:.2f}B")
        hasil_display["Market_Cap"] = hasil_display["Market_Cap"].apply(lambda x: f"${x/1e9:.2f}B")
        hasil_display["Return"] = hasil_display["Return"].apply(lambda x: f"{x:.4%}")
        hasil_display["Volatility"] = hasil_display["Volatility"].apply(lambda x: f"{x:.4f}")
        hasil_display["V"] = hasil_display["V"].apply(lambda x: f"{x:.6f}")
        hasil_display.columns = ["Peringkat", "Crypto", "Close", "Volume", "Market Cap", "Return", "Volatility", "Nilai WP (V)"]
        st.dataframe(hasil_display.set_index("Peringkat"), use_container_width=True, height=400)

        # UI Podium Top 3
        st.markdown("---")
        st.subheader("🥇 Top 3 Terbaik")
        medals, cols_pod = ["🥇", "🥈", "🥉"], st.columns(3)
        for i, (col, (_, row)) in enumerate(zip(cols_pod, data.head(3).iterrows())):
            col.markdown(f'<div class="metric-card"><h4>{medals[i]} Peringkat {i+1}</h4><p>{row["Crypto"]}</p><small style="color:#94a3b8">Nilai WP: {row["V"]:.6f}</small></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 3 – VISUALISASI
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "↗ Visualisasi":
    st.title("↗ Visualisasi Analitik")

    if "hasil" not in st.session_state:
        st.warning("Jalankan perhitungan SPK terlebih dahulu di halaman **⚙︎ Hitung SPK**.")
        st.stop()

    hasil = st.session_state["hasil"]
    top10 = hasil.head(10)
    COLORS = ["#2563eb", "#0891b2", "#059669", "#d97706", "#dc2626", "#7c3aed", "#db2777", "#ea580c", "#16a34a", "#0284c7"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})

    # Grafik 1: Horizontal Bar
    st.subheader("Grafik 1 – Nilai WP Top 10 Crypto")
    fig1, ax1 = plt.subplots(figsize=(12, 4))
    bars = ax1.barh(top10["Crypto"][::-1], top10["V"][::-1], color=COLORS[::-1], edgecolor="white", height=0.6)
    ax1.bar_label(bars, labels=[f"{v:.5f}" for v in top10["V"][::-1]], padding=4, fontsize=8)
    ax1.set_xlim(0, top10["V"].max() * 1.1)
    ax1.grid(axis="x", alpha=0.2, linestyle="--")
    st.pyplot(fig1)
    st.markdown("---")

    # Grafik 2: Scatter Risk-Return
    st.subheader("Grafik 2 – Risk-Return Analysis")
    vx_max, ry_min, ry_max = hasil["Volatility"].quantile(0.95), hasil["Return"].quantile(0.02), hasil["Return"].quantile(0.98)
    others_vis = hasil.iloc[10:][(hasil["Volatility"] <= vx_max) & (hasil["Return"] >= ry_min) & (hasil["Return"] <= ry_max)]

    fig2, ax2 = plt.subplots(figsize=(11, 5.5))
    ax2.axhspan(0, ry_max, xmin=0, xmax=0.5, alpha=0.05, color="green")
    ax2.axhline(0, color="gray", linewidth=1, linestyle="--", alpha=0.5)
    ax2.scatter(others_vis["Volatility"], others_vis["Return"], s=20, color="#94a3b8", alpha=0.4, label="Rank 11–250")
    
    for i, (_, row) in enumerate(top10.iterrows()):
        vx = min(row["Volatility"], vx_max * 0.98)
        ry = max(min(row["Return"], ry_max * 0.98), ry_min * 0.98)
        ax2.scatter(vx, ry, s=120, color=COLORS[i], edgecolors="white", zorder=5)
        ax2.annotate(f"#{int(row['Peringkat'])} {row['Crypto']}", (vx, ry), fontsize=7.5, fontweight="bold", xytext=(5, 5), textcoords="offset points", color=COLORS[i])

    ax2.set_xlim(0, vx_max)
    ax2.set_ylim(ry_min, ry_max)
    ax2.set_xlabel("Volatility (Risiko)")
    ax2.set_ylabel("Return Harian")
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(1.0, decimals=2))
    ax2.legend(loc="lower right")
    st.pyplot(fig2)
    st.markdown("---")

    # Grafik 3: Pie & Volume
    st.subheader("Grafik 3 – Distribusi Market Cap & Volume")
    fig3, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    axes[0].pie(list(top10["Market_Cap"]) + [hasil.iloc[10:]["Market_Cap"].sum()], labels=list(top10["Crypto"]) + ["Lainnya"], autopct="%1.1f%%", colors=COLORS + ["#cbd5e1"], startangle=140, textprops={'fontsize': 7})
    axes[0].set_title("Market Cap Share (%)", fontweight="bold")
    
    axes[1].bar(top10["Crypto"], top10["Volume"] / 1e9, color=COLORS)
    axes[1].tick_params(axis="x", rotation=40, labelsize=8)
    axes[1].set_ylabel("Volume (Miliar USD)")
    axes[1].grid(axis="y", alpha=0.2, linestyle="--")
    plt.tight_layout()
    st.pyplot(fig3)

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 4 – PROFIL KELOMPOK
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "☻ Profil Kelompok":
    st.title("☻ Profil Kelompok")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Informasi Proyek")
        st.table(pd.DataFrame({
            "Item": ["Tema", "Metode SPK", "Dataset", "Jumlah Data", "Sumber Data"],
            "Detail": ["Pemilihan Cryptocurrency Terbaik", "Weighted Product (WP)", "Historical Crypto Data", "250 Cryptocurrency", "CoinMarketCap"]
        }).set_index("Item"))

    with col_b:
        st.subheader("Kriteria")
        st.table(KRITERIA_INFO[["Kriteria", "Jenis"]].set_index("Kriteria"))

    st.markdown("---")
    st.subheader("Anggota Kelompok")
    members = [
        {"nama": "Rizqy Wildan Azka", "nim": "NIM 123240219"},
        {"nama": "Adiel Khairullah", "nim": "NIM 123240221"},
    ]
    cols_m = st.columns(len(members))
    for col, m in zip(cols_m, members):
        col.markdown(f'<div class="metric-card"><p style="font-size:1rem">{m["nama"]}</p><small style="color:#94a3b8">{m["nim"]}</small></div>', unsafe_allow_html=True)
