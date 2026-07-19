import streamlit as st

from modules.metrics import *
from modules.charts import *

st.set_page_config(
    page_title="Presensi",
    layout="wide"
)

presensi = st.session_state["presensi"]

st.title("📝 Dashboard Presensi")

# =====================================================
# KPI
# =====================================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Presensi",
    total_peserta(presensi)
)

col2.metric(
    "Laki-laki",
    jumlah_laki(presensi)
)

col3.metric(
    "Perempuan",
    jumlah_perempuan(presensi)
)

col4.metric(
    "Rata-rata Usia",
    rata_usia(presensi)
)

col5.metric(
    "Provinsi",
    jumlah_provinsi(presensi)
)

st.divider()

# =====================================================
# DATAFRAME
# =====================================================

with st.expander("📋 Lihat Data Presensi", expanded=False):

    st.dataframe(
        presensi,
        use_container_width=True
    )

st.divider()

# =====================================================
# PRESENSI PER HARI
# =====================================================

col1, col2 = st.columns(2)

with col1:

    fig = line_chart(
        presensi,
        "Tanggal",
        "Presensi per Hari",
        palette="orange"
    )

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

with col2:

    fig = hour_chart(
        presensi,
        "Jam",
        "Presensi per Jam",
        palette="purple"
    )

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.divider()

# =====================================================
# USIA & JENIS KELAMIN
# =====================================================

col1, col2 = st.columns(2)

with col1:

    fig = histogram(
        presensi,
        "Usia",
        "Distribusi Usia",
        palette="green",
        bin_size=5
    )

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

with col2:

    fig = pie_chart(
        presensi,
        "Jenis Kelamin",
        "Jenis Kelamin",
        palette="cyan"
    )

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.divider()

# =====================================================
# PETA INDONESIA
# =====================================================

fig = map_chart(
    presensi,
    "Provinsi",
    "Sebaran Peserta"
)

if fig:
    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# STATUS & KEPUASAN
# =====================================================

col1, col2 = st.columns(2)

with col1:

    if "Status Saat Ini" in presensi.columns:

        fig = bar_chart(
            presensi,
            "Status Saat Ini",
            "Status Peserta",
            palette="orange"
        )

        if fig:
            st.plotly_chart(
                fig,
                use_container_width=True
            )

with col2:

    if "Seberapa puas Anda mengikuti webinar ini?" in presensi.columns:

        fig = bar_chart(
            presensi,
            "Seberapa puas Anda mengikuti webinar ini?",
            "Tingkat Kepuasan",
            palette="purple",
            sort=False
        )

        if fig:
            st.plotly_chart(
                fig,
                use_container_width=True
            )

st.divider()

# =====================================================
# FEEDBACK
# =====================================================

if "Pesan atau saran untuk kegiatan selanjutnya" in presensi.columns:

    st.subheader("💬 Feedback Peserta")

    st.info(
        "WordCloud dan analisis saran akan ditambahkan pada tahap berikutnya.")