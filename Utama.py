import streamlit as st

from modules.loader import load_all_webinars
from modules.preprocess import (
    preprocess_registrasi,
    preprocess_presensi
)
from modules.metrics import *

st.set_page_config(
    page_title="Dashboard Webinar",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Webinar")

# ===========================
# LOAD DATA
# ===========================

webinars = load_all_webinars()

if not webinars:
    st.error("Tidak ada file Excel ditemukan.")
    st.stop()

# ===========================
# SIDEBAR
# ===========================

selected = st.sidebar.selectbox(
    "Pilih Webinar",
    list(webinars.keys())
)

registrasi = webinars[selected].get("registrasi")
presensi = webinars[selected].get("presensi")

if registrasi is not None:
    registrasi = preprocess_registrasi(registrasi)

if presensi is not None:
    presensi = preprocess_presensi(presensi)

# Simpan agar bisa dipakai pages
st.session_state["selected"] = selected
st.session_state["webinars"] = webinars
st.session_state["registrasi"] = registrasi
st.session_state["presensi"] = presensi

# ===========================
# KPI
# ===========================

jumlah_registrasi = len(registrasi)
jumlah_presensi = len(presensi)

attendance_rate = (
    jumlah_presensi / jumlah_registrasi * 100
    if jumlah_registrasi > 0
    else 0
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Registrasi", jumlah_registrasi)
col2.metric("Presensi", jumlah_presensi)
col3.metric("Attendance Rate", f"{attendance_rate:.1f}%")
col4.metric("Laki-laki", jumlah_laki(registrasi))
col5.metric("Perempuan", jumlah_perempuan(registrasi))

st.divider()

with st.expander("📋 Lihat Data Registrasi"):
    st.dataframe(
        registrasi,
        use_container_width=True
    )

with st.expander("✅ Lihat Data Presensi"):
    st.dataframe(
        presensi,
        use_container_width=True
    )
