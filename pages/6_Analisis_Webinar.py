import streamlit as st
import plotly.express as px

from modules.cross import *
from modules.charts import *

st.set_page_config(
    page_title="Tren Webinar",
    layout="wide"
)

st.title("📈 Tren Webinar")

from modules.loader import load_all_webinars
from modules.preprocess import (
    preprocess_registrasi,
    preprocess_presensi
)

webinars = load_all_webinars()

for nama, data in webinars.items():

    if data.get("registrasi") is not None:
        webinars[nama]["registrasi"] = preprocess_registrasi(
            data["registrasi"]
        )

    if data.get("presensi") is not None:
        webinars[nama]["presensi"] = preprocess_presensi(
            data["presensi"]
        )

summary = webinar_summary(webinars)

(
    total_webinar,
    total_registrasi,
    total_presensi,
    attendance
) = overall_summary(webinars)

# ======================================================
# KPI
# ======================================================

best = summary.sort_values(
    "Attendance Rate",
    ascending=False
).iloc[0]

c1,c2,c3,c4 = st.columns(4)

with c1:
    metric_card(
        "Total Webinar",
        total_webinar,
        "🎓",
        "#2563EB"
    )

with c2:
    metric_card(
        "Registrasi",
        total_registrasi,
        "👥",
        "#2563EB"
    )

with c3:
    metric_card(
        "Presensi",
        total_presensi,
        "✅",
        "#F97316"
    )

with c4:
    metric_card(
        "Best Webinar",
        best["Webinar"],
        "🏆",
        "#EAB308"
    )

st.divider()

# ======================================================
# TREN CHART
# ======================================================
st.plotly_chart(
    cross_line_chart(summary),
    use_container_width=True
)

st.divider()

# ======================================================
# RANKING 
# ======================================================

st.subheader("🏆 Top 3 Attendance Webinar")

ranking = (
    summary
    .sort_values("Attendance Rate", ascending=False)
    .head(3)
)

cols = st.columns(3)

medal = ["🥇", "🥈", "🥉"]

for col, (_, row), m in zip(cols, ranking.iterrows(), medal):

    with col:

        st.markdown(f"""
### {m} {row['Webinar']}

### **{row['Attendance Rate']:.1f}%**

👥 Registrasi : **{row['Registrasi']}**

✅ Presensi : **{row['Presensi']}**
""")
st.divider()

# ======================================================
# HEATMAP
# ======================================================

st.subheader("🧩 Heatmap Registrasi & Presensi")

heat = summary.set_index("Webinar")[
    ["Registrasi","Presensi"]
].T

fig = px.imshow(

    heat,

    text_auto=True,

    color_continuous_scale="Blues",

    aspect="auto"

)

fig.update_layout(

    height=350

)

st.plotly_chart(

    fig,

    use_container_width=True

)