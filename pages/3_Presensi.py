import streamlit as st

from modules.metrics import *
from modules.charts import *
from modules.sidebar import sidebar_webinar

webinars, registrasi, presensi = sidebar_webinar()

st.set_page_config(
    page_title="Presensi",
    layout="wide"
)

st.title("📝 Dashboard Presensi")

# =====================================================
# KPI
# =====================================================

col1, col2, col3, col4 = st.columns(4)

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
st.subheader("📅 Aktivitas Pendaftaran")

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
st.subheader("👥 Demografi Peserta")

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
st.subheader("🗺️ Persebaran Peserta")

fig = map_chart(
    presensi,
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
# STATUS & KEPUASAN
# =====================================================
st.subheader("📚 Status Peserta dan Sumber Informasi")

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

st.subheader("💬 Feedback Peserta")

fig = top_words_chart(
    presensi,
    "Pesan atau saran untuk kegiatan selanjutnya"
)

st.plotly_chart(fig, use_container_width=True)
st.divider()