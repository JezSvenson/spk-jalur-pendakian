"""SPK Pemilihan Jalur Pendakian - Weighted Product. Jalankan: streamlit run app.py"""
import pandas as pd
import streamlit as st

from wp import weighted_product

st.set_page_config(page_title="SPK Jalur Pendakian", page_icon="⛰️", layout="wide")
st.title("⛰️ SPK Pemilihan Jalur Pendakian")
st.caption("Metode Weighted Product (WP). Data contoh fiktif, ganti dengan data asli.")

KRITERIA = ["C1 Waktu tempuh (jam)", "C2 Kecuraman (1-5)", "C3 Sumber air (titik)",
            "C4 Pemandangan (1-5)", "C5 Biaya (ribu Rp)"]
JENIS = ["cost", "cost", "benefit", "benefit", "cost"]
PROFIL = {
    "Umum": [5, 4, 3, 4, 2],
    "Pemula": [3, 5, 5, 2, 2],
    "Berpengalaman": [2, 1, 3, 5, 2],
    "Hemat": [3, 3, 3, 2, 5],
}

# --- Sidebar: profil pendaki ---
st.sidebar.header("Profil pendaki")
# ?profil=Pemula di URL memilih profil awal; nilai tak dikenal kembali ke "Umum"
awal = st.query_params.get("profil", "Umum")
profil = st.sidebar.selectbox("Pilih profil", list(PROFIL),
                              index=list(PROFIL).index(awal) if awal in PROFIL else 0)

st.sidebar.divider()
st.sidebar.subheader("Tentang aplikasi")
st.sidebar.markdown(
    "Dibuat untuk memenuhi **Tugas 8** mata kuliah **Kecerdasan Buatan (AI)**.\n\n"
    "Dibangun menggunakan **Python** (Streamlit) dengan algoritma **Weighted Product**.\n\n"
    "**Kelompok 6 AI:**\n"
    "- Fabricio B. I. Gerung\n"
    "- Jeshua L. S. Umpel\n"
    "- Gwenzy N. Rahim\n\n"
    "Teknik Informatika, Politeknik Negeri Manado, 2026"
)

st.subheader("1. Kriteria dan bobot")
kriteria_df = st.data_editor(
    pd.DataFrame({"Kriteria": KRITERIA, "Jenis": JENIS, "Bobot": PROFIL[profil]}),
    key=f"kriteria_{profil}",  # reset tabel saat profil diganti
    disabled=["Kriteria"],
    column_config={
        "Jenis": st.column_config.SelectboxColumn(options=["benefit", "cost"], required=True),
        "Bobot": st.column_config.NumberColumn(min_value=0, step=1, required=True),
    },
    hide_index=True,
    width="stretch",
)

# --- Data alternatif (tambah/hapus baris langsung di tabel) ---
st.subheader("2. Data jalur pendakian")
jalur_df = st.data_editor(
    pd.DataFrame(
        [["Jalur A1", 6, 3, 2, 5, 25], ["Jalur A2", 5, 4, 1, 4, 20],
         ["Jalur A3", 7, 2, 3, 4, 20], ["Jalur A4", 8, 3, 2, 5, 15]],
        columns=["Jalur"] + KRITERIA,
    ),
    num_rows="dynamic",
    hide_index=True,
    width="stretch",
)
jalur_df = jalur_df.dropna()
if len(jalur_df) < 2:
    st.warning("Isi minimal 2 jalur dengan data lengkap.")
    st.stop()

try:
    w, pangkat, S, V, ranking = weighted_product(
        jalur_df["Jalur"].tolist(),
        jalur_df[KRITERIA].astype(float).values.tolist(),
        kriteria_df["Bobot"].astype(float).tolist(),
        kriteria_df["Jenis"].tolist(),
    )
except ValueError as e:
    st.error(str(e))
    st.stop()

# --- Langkah perhitungan ---
st.subheader("3. Normalisasi bobot")
st.latex(r"w_j = \frac{W_j}{\sum W} \quad;\quad \text{cost} \Rightarrow -w_j")
st.dataframe(
    pd.DataFrame({"Kriteria": KRITERIA, "Jenis": kriteria_df["Jenis"],
                  "Bobot awal": kriteria_df["Bobot"], "w": w, "Pangkat": pangkat}).round(4),
    hide_index=True, width="stretch",
)

st.subheader("4. Vektor S dan Vektor V")
st.latex(r"S_i = \prod_j x_{ij}^{\,w_j} \qquad V_i = \frac{S_i}{\sum S}")
st.dataframe(
    pd.DataFrame({"Jalur": jalur_df["Jalur"], "S": S, "V": V}).round(4),
    hide_index=True, width="stretch",
)
st.write(f"ΣS = {sum(S):.4f}")

st.subheader("5. Ranking")
rank_df = pd.DataFrame(ranking, columns=["Jalur", "V"])
rank_df.index = range(1, len(rank_df) + 1)
st.dataframe(rank_df.round(4), width="stretch")
st.bar_chart(rank_df.set_index("Jalur"))
st.success(f"Rekomendasi untuk profil **{profil}**: **{ranking[0][0]}** (V = {ranking[0][1]:.4f})")
