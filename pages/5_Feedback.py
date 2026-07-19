import streamlit as st

from modules.charts import *

st.set_page_config(
    page_title="Feedback Peserta",
    layout="wide"
)

presensi = st.session_state.get("presensi")

if presensi is None:
    st.warning("Data presensi belum tersedia.")
    st.stop()

# =====================================================
# NAMA KOLOM
# =====================================================

KOLOM_PUAS = "Seberapa puas Anda mengikuti webinar ini?"
KOLOM_SARAN = "Pesan atau saran untuk kegiatan selanjutnya"

if KOLOM_PUAS not in presensi.columns:
    st.error(f"Kolom '{KOLOM_PUAS}' tidak ditemukan.")
    st.stop()

st.title("💬 Feedback Webinar")

# =====================================================
# KPI
# =====================================================

jumlah_feedback = len(presensi)

rata = (
    presensi[KOLOM_PUAS]
    .value_counts(normalize=True)
    .mul(100)
    .round(1)
)

col1, col2 = st.columns(2)

col1.metric(
    "Jumlah Feedback",
    jumlah_feedback
)

if len(rata) > 0:
    col2.metric(
        "Mayoritas Jawaban",
        rata.index[0]
    )

st.divider()

# =====================================================
# DISTRIBUSI KEPUASAN
# =====================================================

fig = bar_chart(
    presensi,
    KOLOM_PUAS,
    "Distribusi Tingkat Kepuasan",
    palette="green",
    sort=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# DAFTAR SARAN
# =====================================================

st.subheader("📝 Pesan dan Saran")

if KOLOM_SARAN in presensi.columns:

    saran = (

        presensi[KOLOM_SARAN]

        .fillna("")

        .astype(str)

    )

    saran = saran[

        saran.str.strip() != ""

    ]

    if len(saran):

        for isi in saran:

            st.info(isi)

    else:

        st.success("Tidak ada pesan atau saran.")

else:

    st.warning("Kolom saran tidak ditemukan.")