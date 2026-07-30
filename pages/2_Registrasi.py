import streamlit as st

st.set_page_config(
    page_title="Registrasi",
    layout="wide"
)

from modules.metrics import *
from modules.charts import *
from modules.sidebar import sidebar_webinar

webinars, registrasi, presensi = sidebar_webinar()

st.title("📝 Dashboard Registrasi")

if registrasi is None or registrasi.empty:
    st.warning("⚠️ Data registrasi untuk webinar ini tidak ditemukan.")
    st.stop()

# =====================================================
# KPI
# =====================================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Registrasi", total_peserta(registrasi))
col2.metric("Laki-laki", jumlah_laki(registrasi))
col3.metric("Perempuan", jumlah_perempuan(registrasi))
col4.metric("Rata-rata Usia", rata_usia(registrasi))


st.divider()

# =====================================================
# DATA
# =====================================================
with st.expander("📋 Lihat Data Registrasi"):
    st.dataframe(registrasi, use_container_width=True)

st.divider()

# =====================================================
# TIMESTAMP
# =====================================================
st.subheader("📅 Aktivitas Pendaftaran")

col1, col2 = st.columns(2)

with col1:
    fig = line_chart(registrasi, "Tanggal", "Registrasi per Hari", palette="purple")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = hour_chart(registrasi, "Jam", "Registrasi per Jam", palette="purple")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# DEMOGRAFI
# =====================================================
st.subheader("👥 Demografi Peserta")

col1, col2 = st.columns(2)

with col1:
    fig = histogram(registrasi, "Usia", "Distribusi Usia", palette="green", bin_size=5)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = pie_chart(registrasi, "Jenis Kelamin", "Jenis Kelamin", palette="cyan")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# PERSEBARAN
# =====================================================
st.subheader("🗺️ Persebaran Peserta")

fig = map_chart(registrasi, "Provinsi", "Sebaran Peserta Berdasarkan Provinsi")
if fig:
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# STATUS & SUMBER INFORMASI
# =====================================================
st.subheader("📚 Status Peserta dan Sumber Informasi")

col1, col2 = st.columns(2)

with col1:
    fig = bar_chart(registrasi, "Status Peserta", "Status Peserta", palette="orange")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if "Dari mana Anda mengetahui Informasi webinar ini?" in registrasi.columns:
        fig = bar_chart(
            registrasi,
            "Dari mana Anda mengetahui Informasi webinar ini?",
            "Sumber Informasi"
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# HARAPAN
# =====================================================
st.subheader("💭 Harapan Peserta")

fig = top_words_chart(
    registrasi,
    "Harapan setelah mengikuti webinar ini"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()