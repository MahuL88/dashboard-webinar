import streamlit as st

from modules.metrics import *
from modules.charts import *

st.set_page_config(
    page_title="Registrasi",
    layout="wide"
)

registrasi = st.session_state["registrasi"]

st.title("📝 Dashboard Registrasi")

# =====================================================
# KPI
# =====================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Registrasi",
    total_peserta(registrasi)
)

col2.metric(
    "Rata-rata Usia",
    rata_usia(registrasi)
)

col3.metric(
    "Provinsi",
    jumlah_provinsi(registrasi)
)

col4.metric(
    "Status Peserta",
    jumlah_status(
        registrasi,
        "Status Peserta"
    )
)

st.divider()

# =====================================================
# DATA
# =====================================================

with st.expander("📋 Lihat Data Registrasi"):

    st.dataframe(
        registrasi,
        use_container_width=True
    )
    
# =====================================================
# TIMESTAMP
# =====================================================

st.subheader("📅 Aktivitas Pendaftaran")

col1, col2 = st.columns(2)

with col1:

    fig = line_chart(
        registrasi,
        "Tanggal",
        "Registrasi per Hari",
        palette="purple"
    )

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

with col2:

    fig = hour_chart(
        registrasi,
        "Jam",
        "Registrasi per Jam",
        palette="purple"
    )

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.divider()

# =====================================================
# DEMOGRAFI
# =====================================================

st.subheader("👥 Demografi Peserta")

col1, col2 = st.columns(2)

with col1:

    fig = histogram(
        registrasi,
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
        registrasi,
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
# PERSEBARAN
# =====================================================

st.subheader("🗺️ Persebaran Peserta")

fig = map_chart(
    registrasi,
    "Provinsi",
    "Sebaran Peserta Berdasarkan Provinsi"
)

if fig:
    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# STATUS & SUMBER INFORMASI
# =====================================================

st.subheader("📚 Status Peserta dan Sumber Informasi")

col1, col2 = st.columns(2)

with col1:

    fig = bar_chart(
        registrasi,
        "Status Peserta",
        "Status Peserta",
        palette="orange"
    )

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

with col2:

    if "Dari mana Anda mengetahui Informasi webinar ini?" in registrasi.columns:

        fig = bar_chart(
            registrasi,
            "Dari mana Anda mengetahui Informasi webinar ini?",
            "Sumber Informasi"
        )

        if fig:
            st.plotly_chart(
                fig,
                use_container_width=True
            )

st.divider()

# =====================================================
# HARAPAN
# =====================================================

st.subheader("☁️ Harapan Peserta")

if "Harapan setelah mengikuti webinar ini" in registrasi.columns:

    st.info("WordCloud akan ditampilkan pada tahap berikutnya.")

st.divider()