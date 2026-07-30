import streamlit as st
from modules.loader import load_all_webinars
from modules.preprocess import preprocess_registrasi, preprocess_presensi


def sidebar_webinar():

    if "webinars" not in st.session_state or not st.session_state["webinars"]:
        webinars = load_all_webinars()
        
        if not webinars:
            st.sidebar.error("⚠️ Data webinar tidak ditemukan di folder `data/`")
            return {}, None, None

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

    webinars = st.session_state["webinars"]
    daftar_webinar = list(webinars.keys())

    if not daftar_webinar:
        return {}, None, None
    
    if "selected" not in st.session_state or st.session_state["selected"] not in daftar_webinar:
        st.session_state["selected"] = daftar_webinar[0]

    st.sidebar.selectbox(
        "📌 Pilih Webinar",
        options=daftar_webinar,
        key="selected"
    )

    selected = st.session_state["selected"]

    registrasi = webinars[selected].get("registrasi")
    presensi = webinars[selected].get("presensi")

    return webinars, registrasi, presensi