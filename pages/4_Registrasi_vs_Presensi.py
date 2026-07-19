import streamlit as st

from modules.attendance import *
from modules.charts import *

st.set_page_config(
    page_title="Registrasi vs Presensi",
    layout="wide"
)

registrasi = st.session_state["registrasi"]
presensi = st.session_state["presensi"]

hadir, tidak_hadir, attendance = compare_data(
    registrasi,
    presensi
)
jumlah_registrasi, jumlah_presensi, attendance = summary(
    registrasi,
    presensi
)

st.title("🔄 Registrasi vs Presensi")

# ==================================================
# KPI
# ==================================================

jumlah_tidak_hadir = jumlah_registrasi - jumlah_presensi

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Registrasi",
    jumlah_registrasi
)

col2.metric(
    "Presensi",
    jumlah_presensi
)

col3.metric(
    "Tidak Hadir",
    jumlah_tidak_hadir
)

col4.metric(
    "Attendance",
    f"{attendance:.1f}%"
)

st.divider()

# ==================================================
# Funnel
# ==================================================

col1,col2 = st.columns(2)

with col1:

    st.plotly_chart(

        funnel_chart(

            jumlah_registrasi,
            jumlah_presensi

        ),

        use_container_width=True

    )

with col2:

    st.plotly_chart(

        gauge_chart(

            attendance

        ),

        use_container_width=True

    )

st.divider()

# ==================================================
# Attendance Rate
# ==================================================

col1, col2 = st.columns(2)

with col1:

    prov = attendance_by_province(
        registrasi,
        presensi
    )

    st.plotly_chart(

        attendance_chart(

            prov,

            y="Provinsi",

            x="Attendance Rate",

            title="Attendance Rate per Provinsi",

            palette="blue"

        ),

        use_container_width=True

    )

with col2:

    status = attendance_by_status(
        registrasi,
        presensi
    )

    st.plotly_chart(

        attendance_chart(

            status,

            y="Status Peserta",

            x="Attendance Rate",

            title="Attendance Rate per Status",

            palette="orange"

        ),

        use_container_width=True

    )

st.divider()

# ==================================================
# Peserta Tidak Hadir
# ==================================================

st.subheader("❌ Registrasi tetapi Tidak Hadir")

st.dataframe(
    tidak_hadir,
    use_container_width=True
)

csv = tidak_hadir.to_csv(index=False)

st.download_button(
    "⬇ Download CSV",
    csv,
    "tidak_hadir.csv",
    "text/csv"
)

st.divider()

# ==================================================
# Peserta Hadir
# ==================================================

st.subheader("✅ Peserta Hadir")

st.dataframe(
    hadir,
    use_container_width=True
)


