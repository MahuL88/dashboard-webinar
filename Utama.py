import streamlit as st

st.set_page_config(
    page_title="Dashboard Webinar",
    page_icon="📊",
    layout="wide"
)

from modules.loader import load_all_webinars
from modules.preprocess import preprocess_registrasi, preprocess_presensi
from modules.cross import overall_summary, webinar_summary

# ==================================================
# LOAD DATA (Tanpa Sidebar Widget)
# ==================================================
if "webinars" not in st.session_state or not st.session_state["webinars"]:
    webinars = load_all_webinars()

    for nama in webinars:
        if webinars[nama].get("registrasi") is not None:
            webinars[nama]["registrasi"] = preprocess_registrasi(
                webinars[nama]["registrasi"]
            )

        if webinars[nama].get("presensi") is not None:
            webinars[nama]["presensi"] = preprocess_presensi(
                webinars[nama]["presensi"]
            )

    st.session_state["webinars"] = webinars

webinars = st.session_state.get("webinars", {})

st.title("📊 Dashboard Webinar")

# Jika data kosong, berikan peringatan dan hentikan eksekusi
if not webinars:
    st.warning("Data webinar belum tersedia.")
    st.stop()

# ==================================================
# KPI
# ==================================================
total_webinar, total_registrasi, total_presensi, attendance = overall_summary(webinars)

col1, col2, col3, col4 = st.columns(4)

col1.metric("📚 Total Webinar", total_webinar)
col2.metric("📝 Registrasi", f"{total_registrasi:,}")
col3.metric("✅ Presensi", f"{total_presensi:,}")
col4.metric("📈 Attendance", f"{attendance:.1f}%")

st.divider()

# ==================================================
# TABLE RINGKASAN
# ==================================================
summary = webinar_summary(webinars)

st.subheader("Ringkasan Seluruh Webinar")
st.dataframe(summary, use_container_width=True)