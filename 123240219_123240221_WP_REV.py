import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SPK Crypto – Metode WP",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"] { background: #0f172a; }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    .stButton > button {
        background: #2563eb; color: white; border: none;
        border-radius: 8px; padding: 0.5rem 1.5rem;
        font-weight: 600; width: 100%;
    }
    .stButton > button:hover { background: #1d4ed8; }
    .metric-card {
        background: #1e293b; border-radius: 10px;
        padding: 1rem 1.2rem; margin-bottom: 0.5rem;
    }
    .metric-card h4 { margin: 0 0 4px; font-size: 0.8rem; color: #94a3b8; }
    .metric-card p  { margin: 0; font-size: 1.4rem; font-weight: 700; color: #f1f5f9; }
    h1, h2, h3 { color: #1e293b; }
    .rank-1  { background: #fef9c3; font-weight: 700; }
    .rank-2  { background: #f0fdf4; }
    .rank-3  { background: #eff6ff; }
    .info-box {
        background: #eff6ff; border-left: 4px solid #2563eb;
        padding: 0.75rem 1rem; border-radius: 6px;
        font-size: 0.9rem; color: #1e3a8a; margin-bottom: 1rem;
    }
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

# ── Sidebar navigation ────────────────────────────────────────────────────────
st.sidebar.markdown("## Crypto")
st.sidebar.markdown("**Metode: Weighted Product (WP)**")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigasi",
    ["🖿 Dataset", "⚙︎ Hitung SPK", "↗ Visualisasi", "☻ Profil Kelompok"],
)
st.sidebar.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 1 – DATASET
# ═══════════════════════════════════════════════════════════════════════════════
if menu == "🖿 Dataset":
    st.title("🖿 Dataset Cryptocurrency")
    st.markdown("Dataset berisi **250 cryptocurrency** dengan 5 kriteria penilaian.")

    # Ringkasan statistik
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown('<div class="metric-card"><h4>Total Aset</h4><p>250 Crypto</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card"><h4>Harga Tertinggi</h4><p>${df["Close"].max():,.2f}</p></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card"><h4>Market Cap Terbesar</h4><p>${df["Market_Cap"].max()/1e12:.2f}T</p></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-card"><h4>Volatilitas Terendah</h4><p>{df["Volatility"].min():.4f}</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Filter & search
    col_cariCrypto, col_pilihKriteria = st.columns([2, 1])
    with col_cariCrypto: search = st.text_input("🔍 Cari nama crypto", placeholder="contoh: Bitcoin, Ethereum...")
    with col_pilihKriteria: sort_col = st.selectbox("Urutkan berdasarkan", ["Market_Cap", "Close", "Volume", "Return", "Volatility"])

    df_show = df.copy()
    if search:
        df_show = df_show[df_show["Crypto"].str.contains(search, case=False, na=False)]
    df_show = df_show.sort_values(sort_col, ascending=False).reset_index(drop=True)
    df_show.index += 1

    # Format tampilan
    df_display = df_show.copy()
    df_display["Close"] = df_display["Close"].apply(lambda x: f"${x:,.4f}")
    df_display["Volume"] = df_display["Volume"].apply(lambda x: f"${x/1e9:.2f}B")
    df_display["Market_Cap"] = df_display["Market_Cap"].apply(lambda x: f"${x/1e9:.2f}B")
    df_display["Return"] = df_display["Return"].apply(lambda x: f"{x:.4%}")
    df_display["Volatility"] = df_display["Volatility"].apply(lambda x: f"{x:.4f}")
    df_display.columns = ["Crypto", "Close", "Volume", "Market Cap", "Return", "Volatility"]

    st.dataframe(df_display, use_container_width=True, height=460)

    st.markdown("---")
    st.subheader("Keterangan Kriteria")
    krit = pd.DataFrame({
        "Kriteria": ["Close", "Volume", "Market Cap", "Return", "Volatility"],
        "Keterangan": [
            "Harga penutupan rata-rata harian",
            "Volume perdagangan rata-rata harian",
            "Kapitalisasi pasar rata-rata",
            "Return/imbal hasil harian rata-rata",
            "Volatilitas (standar deviasi return)"
        ],
        "Jenis": ["Benefit ↑", "Benefit ↑", "Benefit ↑", "Benefit ↑", "Cost ↓"],
    })
    st.table(krit.set_index("Kriteria"))

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 2 – HITUNG SPK
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "⚙︎ Hitung SPK":
    st.title("⚙︎ Perhitungan SPK – Weighted Product (WP)")

    st.subheader("1. Atur Bobot Kriteria")

    col1, col2, col3 = st.columns(3)
    col4, col5, _ = st.columns(3)

    with col1: w_close = st.slider("Close (Harga)", 1, 10, 5, help="Semakin tinggi harga, semakin besar bobot")
    with col2: w_volume = st.slider("Volume", 1, 10, 4)
    with col3: w_marketcap = st.slider("Market Cap", 1, 10, 6)
    with col4: w_return = st.slider("Return", 1, 10, 7)
    with col5: w_volatility = st.slider("Volatility", 1, 10, 5, help="Semakin kecil volatility, maka semakin aman")

    bobot_asli = np.array([w_close, w_volume, w_marketcap, w_return, w_volatility], dtype=float)
    bobot_normalisasi = bobot_asli / bobot_asli.sum()

    st.markdown("---")
    st.subheader("2. Bobot Ternormalisasi")
    w_df = pd.DataFrame({
        "Kriteria": ["Close", "Volume", "Market Cap", "Return", "Volatility"],
        "Jenis": ["Benefit", "Benefit", "Benefit", "Benefit", "Cost"],
        "Bobot Input": bobot_asli.astype(int),
        "Bobot Normalisasi": [f"{w:.4f}" for w in bobot_normalisasi],
    })
    st.table(w_df.set_index("Kriteria"))
    st.info(f"Total bobot normal: **{sum(bobot_normalisasi):.4f}** (harus = 1.0)")

    st.markdown("---")
    st.subheader("3. Pilih Jumlah Hasil Perangkingan")
    top_n = st.number_input("Tampilkan Top N Crypto", min_value=5, max_value=250, value=20, step=5)

    st.markdown("---")
    if st.button("🚀 Hitung WP & Tampilkan Hasil"):
        with st.spinner("Menghitung..."):
            data = df.copy()

            # Hapus baris dengan nilai 0 atau negatif (tidak bisa dipangkatkan log)
            for col in ["Close", "Volume", "Market_Cap"]:
                data = data[data[col] > 0]
            # Return bisa negatif – geser agar semua positif
            data["Return_adj"] = data["Return"] - data["Return"].min() + 1e-9
            data["Volatility_adj"] = data["Volatility"].copy()

            kolom = ["Close", "Volume", "Market_Cap", "Return_adj", "Volatility_adj"]
            tipe = ["benefit", "benefit", "benefit", "benefit", "cost"]
            bobot = bobot_normalisasi.copy()

            # Hitung S (Weighted Product)
            S = np.ones(len(data))
            for i, (kolom, tipe, bobot) in enumerate(zip(kolom, tipe, bobot)):
                vals = data[kolom].values.astype(float)
                if tipe == "benefit":
                    S *= vals ** bobot
                else:  # cost
                    S *= vals ** (-bobot)

            data["S"] = S

            # Hitung V (normalisasi S)
            data["V"] = data["S"] / data["S"].sum()
            data = data.sort_values("V", ascending=False).reset_index(drop=True)
            data.index += 1
            data["Peringkat"] = data.index

            # Simpan ke session state
            st.session_state["hasil"] = data
            st.session_state["top_n"] = top_n

        st.success("✅ Perhitungan selesai!")
        st.markdown("---")
        st.subheader(f"🏆 Hasil Perangkingan – Top {top_n}")

        hasil = st.session_state["hasil"].head(top_n).copy()
        hasil_display = hasil[["Peringkat", "Crypto", "Close", "Volume", "Market_Cap", "Return", "Volatility", "V"]].copy()
        hasil_display["Close"] = hasil_display["Close"].apply(lambda x: f"${x:,.4f}")
        hasil_display["Volume"] = hasil_display["Volume"].apply(lambda x: f"${x/1e9:.2f}B")
        hasil_display["Market_Cap"] = hasil_display["Market_Cap"].apply(lambda x: f"${x/1e9:.2f}B")
        hasil_display["Return"] = hasil_display["Return"].apply(lambda x: f"{x:.4%}")
        hasil_display["Volatility"] = hasil_display["Volatility"].apply(lambda x: f"{x:.4f}")
        hasil_display["V"] = hasil_display["V"].apply(lambda x: f"{x:.6f}")
        hasil_display.columns = ["Peringkat", "Crypto", "Close", "Volume", "Market Cap", "Return", "Volatility", "Nilai WP (V)"]

        st.dataframe(hasil_display.set_index("Peringkat"), use_container_width=True, height=420)

        # Podium top 3
        st.markdown("---")
        st.subheader("🥇 Top 3 Terbaik")
        medals = ["🥇", "🥈", "🥉"]
        cols_pod = st.columns(3)
        for i, (col, (_, row)) in enumerate(zip(cols_pod, st.session_state["hasil"].head(3).iterrows())):
            with col:
                st.markdown(f"""
                <div class="metric-card" style="text-align:center">
                    <h4>{medals[i]} Peringkat {i+1}</h4>
                    <p>{row['Crypto']}</p>
                    <small style="color:#94a3b8">Nilai WP: {row['V']:.6f}</small>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 3 – VISUALISASI
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "↗ Visualisasi":
    st.title("↗ Visualisasi Analitik")

    if "hasil" not in st.session_state:
        st.warning("Jalankan perhitungan SPK terlebih dahulu di halaman ** ⚙︎ Hitung SPK**.")
        st.stop()

    hasil = st.session_state["hasil"]
    top_n = st.session_state.get("top_n", 20)
    top = hasil.head(top_n)

    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})
    COLORS = ["#2563eb", "#0891b2", "#059669", "#d97706", "#dc2626",
              "#7c3aed", "#db2777", "#ea580c", "#16a34a", "#0284c7"]

    # ── Grafik 1: Bar chart top 15 Nilai WP ─────────────────────────────────
    st.subheader("📊 Grafik 1 – Nilai WP Top 15 Crypto")
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    top15 = hasil.head(15)
    bars = ax1.barh(top15["Crypto"][::-1], top15["V"][::-1], color=COLORS[:15][::-1], edgecolor="white", height=0.65)
    ax1.set_xlabel("Nilai WP (V)", fontsize=11)
    ax1.set_title("Top 15 Cryptocurrency Terbaik Berdasarkan Nilai WP", fontsize=13, fontweight="bold", pad=12)
    ax1.bar_label(bars, labels=[f"{v:.5f}" for v in top15["V"][::-1]], padding=4, fontsize=8.5)
    ax1.set_xlim(0, top15["V"].max() * 1.15)
    ax1.grid(axis="x", alpha=0.3, linestyle="--")
    plt.tight_layout()
    st.pyplot(fig1)

    st.markdown("---")

    # ── Grafik 2: Scatter Return vs Volatility ───────────────────────────────
    st.subheader("📊 Grafik 2 – Risk-Return Analysis (Top 10 vs Lainnya)")
    st.caption("Sumbu dipotong pada persentil 95 agar titik tidak menumpuk akibat outlier. Ideal: Return tinggi (atas) & Volatilitas rendah (kiri).")

    # Clip outlier: batasi sumbu ke persentil 95 supaya grafik tidak gepeng
    vx_max = hasil["Volatility"].quantile(0.95)
    ry_min = hasil["Return"].quantile(0.02)
    ry_max = hasil["Return"].quantile(0.98)

    # Pisah data: top10 berwarna, sisanya abu
    top10_scatter = hasil.head(10)
    others        = hasil.iloc[10:].copy()
    # filter outlier untuk titik abu agar tidak melebihi batas sumbu
    others_vis = others[(others["Volatility"] <= vx_max) &
                        (others["Return"] >= ry_min) & (others["Return"] <= ry_max)]

    fig2, ax2 = plt.subplots(figsize=(11, 6))
    fig2.patch.set_facecolor("#f8fafc")
    ax2.set_facecolor("#f8fafc")

    # Kuadran latar belakang
    ax2.axhspan(0, ry_max, xmin=0, xmax=0.5, alpha=0.06, color="#16a34a")  # kiri atas = ideal
    ax2.axhspan(ry_min, 0, xmin=0, xmax=0.5, alpha=0.04, color="#dc2626")  # kiri bawah
    ax2.axhspan(0, ry_max, xmin=0.5, xmax=1, alpha=0.03, color="#d97706")  # kanan atas
    ax2.axhspan(ry_min, 0, xmin=0.5, xmax=1, alpha=0.06, color="#dc2626")  # kanan bawah = buruk

    # Garis tengah
    ax2.axhline(0, color="#475569", linewidth=1, linestyle="--", alpha=0.5)
    ax2.axvline(hasil["Volatility"].median(), color="#475569", linewidth=1,
                linestyle=":", alpha=0.5)

    # Titik lainnya (abu kecil)
    ax2.scatter(others_vis["Volatility"], others_vis["Return"],
                s=22, color="#94a3b8", alpha=0.45, zorder=2, label="Lainnya (rank 11–250)")

    # Warna berbeda untuk setiap top 10
    TOP10_COLORS = ["#ef4444","#f97316","#eab308","#22c55e","#06b6d4",
                    "#3b82f6","#8b5cf6","#ec4899","#14b8a6","#f59e0b"]
    for i, (_, row) in enumerate(top10_scatter.iterrows()):
        vx = min(row["Volatility"], vx_max * 0.98)   # jangan melebihi batas plot
        ry = max(min(row["Return"], ry_max * 0.98), ry_min * 0.98)
        ax2.scatter(vx, ry, s=160, color=TOP10_COLORS[i],
                    edgecolors="white", linewidths=1.2, zorder=5)
        ax2.annotate(
            f"#{int(row['Peringkat'])} {row['Crypto']}",
            (vx, ry),
            fontsize=8, fontweight="bold",
            xytext=(8, 6), textcoords="offset points",
            color=TOP10_COLORS[i],
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=TOP10_COLORS[i],
                      alpha=0.85, linewidth=0.8),
        )

    # Anotasi kuadran
    ax2.text(vx_max * 0.03, ry_max * 0.88, " Ideal\n(Return↑ Risk↓)",
             fontsize=8, color="#15803d", alpha=0.75, va="top")
    ax2.text(vx_max * 0.55, ry_max * 0.88, " High Risk\n High Return",
             fontsize=8, color="#b45309", alpha=0.75, va="top")
    ax2.text(vx_max * 0.03, ry_min * 0.85, " Rugi & Aman",
             fontsize=8, color="#dc2626", alpha=0.75, va="bottom")
    ax2.text(vx_max * 0.55, ry_min * 0.85, " Paling Buruk",
             fontsize=8, color="#dc2626", alpha=0.75, va="bottom")

    ax2.set_xlim(0, vx_max)
    ax2.set_ylim(ry_min, ry_max)
    ax2.set_xlabel("Volatility / Risiko (Std Dev Return)", fontsize=11)
    ax2.set_ylabel("Return Rata-rata Harian", fontsize=11)
    ax2.set_title("Risk-Return Analysis: Top 10 vs Semua Crypto", fontsize=13, fontweight="bold", pad=14)
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(1.0, decimals=2))
    ax2.legend(fontsize=9, loc="lower right")
    ax2.grid(alpha=0.2, linestyle="--", color="#cbd5e1")
    ax2.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig2)

    st.markdown("---")

    # ── Grafik 3: Distribusi Market Cap (pie) ───────────────────────────────
    st.subheader("📊 Grafik 3 – Distribusi Market Cap Top 10 vs Lainnya")
    fig3, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Pie – market cap share
    top10 = hasil.head(10)
    other_cap = hasil.iloc[10:]["Market_Cap"].sum()
    pie_vals = list(top10["Market_Cap"]) + [other_cap]
    pie_labels = list(top10["Crypto"]) + ["Lainnya (240)"]
    pie_colors = COLORS + ["#cbd5e1"]
    wedges, texts, autotexts = axes[0].pie(
        pie_vals, labels=None, autopct="%1.1f%%",
        colors=pie_colors, startangle=140, pctdistance=0.75,
        wedgeprops={"edgecolor": "white", "linewidth": 1.2}
    )
    for at in autotexts:
        at.set_fontsize(7.5)
    axes[0].legend(wedges, pie_labels, loc="lower left", fontsize=7, bbox_to_anchor=(-0.35, -0.1))
    axes[0].set_title("Market Cap Share (%)", fontsize=12, fontweight="bold")

    # Bar – volume top 10
    axes[1].bar(top10["Crypto"], top10["Volume"] / 1e9, color=COLORS, edgecolor="white")
    axes[1].set_xlabel("Crypto", fontsize=10)
    axes[1].set_ylabel("Volume (Miliar USD)", fontsize=10)
    axes[1].set_title("Volume Perdagangan Top 10", fontsize=12, fontweight="bold")
    axes[1].tick_params(axis="x", rotation=40, labelsize=8)
    axes[1].grid(axis="y", alpha=0.3, linestyle="--")
    plt.tight_layout()
    st.pyplot(fig3)

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 4 – PROFIL KELOMPOK
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "☻ Profil Kelompok":
    st.title("☻ Profil Kelompok")

    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.subheader("Informasi Proyek")
        info = pd.DataFrame({
            "Item": ["Tema", "Metode SPK", "Dataset", "Jumlah Data", "Jumlah Kriteria", "Sumber Data"],
            "Detail": [
                "Pemilihan Cryptocurrency Terbaik",
                "Weighted Product (WP)",
                "Historical Crypto Data",
                "250 Cryptocurrency",
                "5 Kriteria",
                "CoinMarketCap"
            ]
        })
        st.table(info.set_index("Item"))

    with col_b:
        st.subheader("Kriteria yang Digunakan")
        krit = pd.DataFrame({
            "No": [1, 2, 3, 4, 5],
            "Kriteria": ["Close", "Volume", "Market Cap", "Return", "Volatility"],
            "Jenis": ["Benefit ↑", "Benefit ↑", "Benefit ↑", "Benefit ↑", "Cost ↓"],
            "Keterangan": [
                "Harga penutupan rata-rata",
                "Volume perdagangan rata-rata",
                "Kapitalisasi pasar rata-rata",
                "Return harian rata-rata",
                "Standar deviasi return (risiko)"
            ]
        })
        st.table(krit.set_index("No"))

    st.markdown("---")
    st.subheader("Anggota Kelompok")

    # Isi dengan data kelompok Anda
    members = [
        {"nama": "Rizqy Wildan Azka", "nim": "NIM 123240219"},
        {"nama": "Adiel Khairullah", "nim": "NIM 123240221"},
    ]
    cols_m = st.columns(len(members))
    for col, m in zip(cols_m, members):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:center;min-height:90px">
                <p style="font-size:1rem">{m['nama']}</p>
                <small style="color:#94a3b8">{m['nim']}</small>
            </div>""", unsafe_allow_html=True)
