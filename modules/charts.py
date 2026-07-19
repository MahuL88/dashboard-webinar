import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import plotly.graph_objects as go
from pathlib import Path

# ==========================================================
# PALETTE
# ==========================================================

PALETTES = {

    "green": ("#CDECCF", "#2E7D32"),

    "purple": ("#E9D5FF", "#7C3AED"),

    "orange": ("#FFE4C7", "#EA580C"),

    "cyan": ("#CFFAFE", "#0891B2"),

    "pink": ("#FBCFE8", "#BE185D"),

    "blue": ("#DBEAFE", "#2563EB")

}

TEMPLATE = "plotly_white"


# ==========================================================
# LAYOUT
# ==========================================================

def style(fig):

    fig.update_layout(

        template="plotly_white",

        height=430,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        title=dict(
            x=0.02,
            font=dict(
                size=22,
                family="Segoe UI",
                color="#334155"
            )
        ),

        paper_bgcolor="white",

        plot_bgcolor="white",

        font=dict(
            family="Segoe UI",
            color="#475569"
        ),

        legend_title="",

        hoverlabel=dict(
            bgcolor="white",
            font_size=13
        )
    )

    fig.update_xaxes(

        showgrid=False,

        zeroline=False,

        linecolor="#CBD5E1"
    )

    fig.update_yaxes(

        gridcolor="#E2E8F0",

        zeroline=False,

        linecolor="#CBD5E1"
    )

    return fig


# ==========================================================
# BAR CHART
# ==========================================================

def bar_chart(
        df,
        column,
        title,
        palette="blue",
        top_n=None,
        sort=True
):

    if column not in df.columns:
        return None

    data = (

        df[column]

        .fillna("Tidak diketahui")

        .astype(str)

        .value_counts()

        .reset_index()

    )

    data.columns = [column, "Jumlah"]

    if top_n:
        data = data.head(top_n)

    if sort:
        data = data.sort_values(
            "Jumlah",
            ascending=True
        )

    light, dark = PALETTES[palette]

    colors = [light] * len(data)

    idx = data["Jumlah"].idxmax()

    colors[data.index.get_loc(idx)] = dark

    fig = px.bar(

        data,

        x="Jumlah",

        y=column,

        orientation="h",

        text="Jumlah",

        title=title

    )

    fig.update_traces(

        marker_color=colors,

        textposition="outside",

        marker_line_width=0,

        hovertemplate="<b>%{y}</b><br>Jumlah : %{x}<extra></extra>"

    )

    fig.update_layout(

        xaxis_title="",

        yaxis_title=""

    )

    return style(fig)


# ==========================================================
# HISTOGRAM
# ==========================================================

def histogram(
        df,
        column,
        title,
        palette="green",
        bin_size=5
):

    if column not in df.columns:
        return None

    light, dark = PALETTES[palette]

    usia = pd.to_numeric(df[column], errors="coerce").dropna()

    start = (usia.min() // bin_size) * bin_size
    end = ((usia.max() // bin_size) + 1) * bin_size

    bins = list(range(int(start), int(end + bin_size), bin_size))

    labels = [
        f"{bins[i]}-{bins[i+1]-1}"
        for i in range(len(bins)-1)
    ]

    kategori = pd.cut(
        usia,
        bins=bins,
        labels=labels,
        right=False
    )

    data = kategori.value_counts().sort_index().reset_index()

    data.columns = ["Rentang", "Jumlah"]

    colors = [light] * len(data)

    colors[data["Jumlah"].idxmax()] = dark

    fig = px.bar(

        data,

        x="Rentang",

        y="Jumlah",

        text="Jumlah",

        title=title

    )

    fig.update_traces(

        marker_color=colors,
        marker_line_width=0,

        hovertemplate="Usia %{x}<br>%{y} peserta<extra></extra>"

    )

    return style(fig)


# ==========================================================
# AREA CHART
# ==========================================================

def line_chart(
        df,
        column,
        title,
        palette="orange"
):

    if column not in df.columns:
        return None

    data = (
        df[column]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    data.columns = [column, "Jumlah"]

    fig = go.Figure()

    # area
    fig.add_trace(

        go.Scatter(

            x=data[column],
            y=data["Jumlah"],

            mode="lines",

            line=dict(
                color="rgba(0,0,0,0)"
            ),

            fill="tozeroy",

            fillcolor="rgba(249,115,22,0.18)",

            hoverinfo="skip",

            showlegend=False

        )

    )

    # garis utama
    fig.add_trace(

        go.Scatter(

            x=data[column],
            y=data["Jumlah"],

            mode="lines+markers+text",

            text=data["Jumlah"],

            textposition="top center",

            line=dict(

                color="#F97316",
                width=4

            ),

            marker=dict(

                size=8,
                color="#EA580C"

            ),

            showlegend=False

        )

    )

    fig.update_layout(

        title=title,

        xaxis_title="",

        yaxis_title="Jumlah"

    )

    return style(fig)


# ==========================================================
# BAR KHUSUS JAM
# ==========================================================

def hour_chart(
        df,
        column,
        title,
        palette="purple"
):

    if column not in df.columns:
        return None

    hours = pd.DataFrame({

        "Jam": range(24)

    })

    data = (

        df[column]

        .value_counts()

        .rename_axis("Jam")

        .reset_index(name="Jumlah")

    )

    data["Jam"] = pd.to_numeric(data["Jam"])

    data = hours.merge(

        data,

        on="Jam",

        how="left"

    )

    data["Jumlah"] = data["Jumlah"].fillna(0)

    light, dark = PALETTES[palette]

    colors = [light] * len(data)

    colors[data["Jumlah"].idxmax()] = dark

    fig = px.bar(

        data,

        x="Jam",

        y="Jumlah",

        text="Jumlah",

        title=title

    )

    fig.update_traces(

        marker_color=colors

    )

    fig.update_xaxes(

    tickmode="linear",

    tickvals=list(range(24)),

    ticktext=[

        f"{i:02d}"

        for i in range(24)

    ]
)

    return style(fig)


# ==========================================================
# MAP
# ==========================================================

def map_chart(
    df,
    column="Provinsi",
    title="Sebaran Peserta"
):
    if column not in df.columns:
        return None
    
    all_provinces = pd.DataFrame({
    "Provinsi": [
        "ACEH",
        "SUMATERA UTARA",
        "SUMATERA BARAT",
        "RIAU",
        "KEPULAUAN RIAU",
        "JAMBI",
        "SUMATERA SELATAN",
        "KEPULAUAN BANGKA BELITUNG",
        "BENGKULU",
        "LAMPUNG",
        "DKI JAKARTA",
        "JAWA BARAT",
        "JAWA TENGAH",
        "DI YOGYAKARTA",
        "JAWA TIMUR",
        "BANTEN",
        "BALI",
        "NUSA TENGGARA BARAT",
        "NUSA TENGGARA TIMUR",
        "KALIMANTAN BARAT",
        "KALIMANTAN TENGAH",
        "KALIMANTAN SELATAN",
        "KALIMANTAN TIMUR",
        "KALIMANTAN UTARA",
        "SULAWESI UTARA",
        "GORONTALO",
        "SULAWESI TENGAH",
        "SULAWESI BARAT",
        "SULAWESI SELATAN",
        "SULAWESI TENGGARA",
        "MALUKU",
        "MALUKU UTARA",
        "PAPUA",
        "PAPUA BARAT",
        "PAPUA SELATAN",
        "PAPUA TENGAH",
        "PAPUA PEGUNUNGAN",
        "PAPUA BARAT DAYA"
    ]
})

    # -----------------------------
    # Load GeoJSON
    # -----------------------------
    with open(
        "assets/batas_provinsi.geojson",
        encoding="utf-8"
    ) as f:
        geojson = json.load(f)

    jumlah = (
    df[column]
    .astype(str)
    .str.upper()
    .str.strip()
    .value_counts()
    .rename_axis("Provinsi")
    .reset_index(name="Jumlah")
)

    jumlah = (
        df[column]
        .astype(str)
        .str.upper()
        .str.strip()
        .value_counts()
        .rename_axis("Provinsi")
        .reset_index(name="Jumlah")
    )

    data = all_provinces.merge(
        jumlah,
        on="Provinsi",
        how="left"
    )

    data["Jumlah"] = data["Jumlah"].fillna(0)

    data.columns = ["Provinsi", "Jumlah"]

    data["Persentase"] = (
        data["Jumlah"] /
        data["Jumlah"].sum() * 100
    ).round(2)

    fig = px.choropleth(
        data_frame=data,

        geojson=geojson,

        locations="Provinsi",

        featureidkey="properties.Provinsi",

        color="Jumlah",

        hover_name="Provinsi",

        hover_data={
            "Jumlah": True,
            "Persentase": True
        },

        projection="mercator",

        color_continuous_scale=[

        (0.0,"#F8FAFC"),

        (0.2,"#ECFEFF"),

        (0.4,"#CFFAFE"),

        (0.6,"#67E8F9"),

        (0.8,"#06B6D4"),

        (1.0,"#155E75")
],
    )

    fig.update_geos(

    showcountries=False,

    showcoastlines=False,

    showland=True,

    landcolor="#F8FAFC",

    showocean=True,

    oceancolor="#E0F2FE",

    showlakes=True,

    lakecolor="#E0F2FE",

    fitbounds=False,

    center={
        "lat": -2.5,
        "lon":118
    },

    projection_scale=5.3
)

    fig.update_layout(

        title=title,

        margin=dict(
            l=0,
            r=0,
            t=50,
            b=0
        ),

        coloraxis_colorbar=dict(
            title="Peserta"
        )

    )

    return fig


# =====================================================
# PIE
# =====================================================

def pie_chart(
        df,
        column,
        title,
        palette="cyan"
):

    if column not in df.columns:
        return None

    data = (
        df[column]
        .fillna("Tidak diketahui")
        .astype(str)
        .value_counts()
        .reset_index()
    )

    data.columns = [column, "Jumlah"]

    light, dark = PALETTES[palette]

    fig = px.pie(

        data,

        names=column,

        values="Jumlah",

        title=title,

        color_discrete_sequence=[
            dark,
            light,
            "#FDE68A",
            "#FBCFE8",
            "#DDD6FE",
            "#E5E7EB"
        ]

    )

    fig.update_traces(

    textinfo="percent+label",

    pull=[0.05] + [0]*(len(data)-1),

    marker=dict(

        line=dict(

            color="white",

            width=3

        )
    )
)

    return style(fig)


def funnel_chart(registrasi,presensi):

    fig = go.Figure(

        go.Funnel(

            y=[

                "Registrasi",

                "Presensi"

            ],

            x=[

                registrasi,

                presensi

            ],

            marker=dict(

                color=[

                    "#93C5FD",

                    "#2563EB"

                ]

            )

        )

    )

    fig.update_layout(

        height=350,

        margin=dict(

            l=20,
            r=20,
            t=50,
            b=20

        )

    )

    return fig

def gauge_chart(rate):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=rate,

            number={

                "suffix":"%",

                "font":{

                    "size":42
                }

            },

            title={

                "text":"Attendance Rate"

            },

            gauge={

                "axis":{

                    "range":[0,100]
                },

                "bar":{

                    "color":"#2563EB"
                },

                "steps":[

                    {
                        "range":[0,50],
                        "color":"#FECACA"
                    },

                    {
                        "range":[50,80],
                        "color":"#FDE68A"
                    },

                    {
                        "range":[80,100],
                        "color":"#BBF7D0"
                    }

                ]

            }

        )

    )

    fig.update_layout(

        height=350,

        margin=dict(

            l=20,
            r=20,
            t=60,
            b=20

        )

    )

    return fig

def attendance_chart(
    df,
    category,
    title,
    palette="blue"
):

    light, dark = PALETTES[palette]

    data = df.sort_values(
        "Attendance Rate",
        ascending=True
    )

    colors = [light] * len(data)

    idx = data["Attendance Rate"].idxmax()

    colors[data.index.get_loc(idx)] = dark

    fig = px.bar(

        data,

        x="Attendance Rate",

        y=category,

        orientation="h",

        text="Attendance Rate",

        title=title

    )

    fig.update_traces(

        marker_color=colors,

        texttemplate="%{text:.1f}%",

        textposition="outside",

        hovertemplate="<b>%{y}</b><br>%{x:.1f}%<extra></extra>"

    )

    fig.update_xaxes(

        range=[0,100],

        ticksuffix="%"

    )

    fig.update_layout(

        xaxis_title="",

        yaxis_title=""

    )

    return style(fig)

def attendance_chart(
    df,
    y,
    x,
    title,
    palette="blue"
):

    light, dark = PALETTES[palette]

    df = df.sort_values(x)

    colors = [light] * len(df)
    colors[df[x].idxmax()] = dark

    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation="h",
        text=x,
        title=title
    )

    fig.update_traces(
        marker_color=colors,
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_range=[0,100],
        xaxis_title="Attendance (%)",
        yaxis_title=""
    )

    return style(fig)


# ==========================================================
# MULTI LINE CHART
# ==========================================================

def multi_line_chart(df):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df["Webinar"],

            y=df["Registrasi"],

            mode="lines+markers+text",

            name="Registrasi",

            text=df["Registrasi"],

            textposition="top center",

            line=dict(

                color="#2563EB",

                width=4

            ),

            marker=dict(

                size=8,

                color="#2563EB"

            )

        )

    )

    fig.add_trace(

        go.Scatter(

            x=df["Webinar"],

            y=df["Presensi"],

            mode="lines+markers+text",

            name="Presensi",

            text=df["Presensi"],

            textposition="bottom center",

            line=dict(

                color="#F97316",

                width=4

            ),

            marker=dict(

                size=8,

                color="#EA580C"

            )

        )

    )

    fig.update_layout(

        title="Registrasi vs Presensi",

        yaxis_title="Peserta",

        xaxis_title="",

        legend=dict(

            orientation="h",

            y=1.08

        )

    )

    return style(fig)

# ==========================================================
# ATTENDANCE WEBINAR
# ==========================================================

def attendance_webinar_chart(df):

    data = df.sort_values(

        "Attendance Rate"

    )

    colors = [

        "#DBEAFE"

    ] * len(data)

    colors[-1] = "#2563EB"

    fig = px.bar(

        data,

        x="Attendance Rate",

        y="Webinar",

        orientation="h",

        text="Attendance Rate"

    )

    fig.update_traces(

        marker_color=colors,

        texttemplate="%{text:.1f}%",

        textposition="outside"

    )

    fig.update_layout(

        title="Attendance Rate per Webinar",

        xaxis_title="",

        yaxis_title=""

    )

    return style(fig)

# ==========================================================
# TREEMAP
# ==========================================================
def treemap_chart(summary):

    fig = px.treemap(

        summary,

        path=["Webinar"],

        values="Registrasi",

        color="Attendance Rate",

        color_continuous_scale="Blues",

        custom_data=[

            summary["Registrasi"],

            summary["Presensi"],

            summary["Attendance Rate"]

        ]

    )

    fig.update_traces(

        hovertemplate=

        "<b>%{label}</b><br>"

        "Registrasi : %{customdata[0]}<br>"

        "Presensi : %{customdata[1]}<br>"

        "Attendance : %{customdata[2]}%<extra></extra>"

    )

    fig.update_layout(

        margin=dict(

            l=10,

            r=10,

            t=50,

            b=10

        ),

        height=430

    )

    return fig

def treemap_chart(df):

    fig = px.treemap(

        df,

        path=["Webinar"],

        values="Registrasi",

        color="Registrasi",

        color_continuous_scale=[

            "#DBEAFE",

            "#60A5FA",

            "#2563EB"

        ]

    )

    fig.update_layout(

        title="Proporsi Peserta"

    )

    return style(fig)

# ==========================================================
# COMPARISON BAR
# ==========================================================

def comparison_bar_chart(

    df,

    category,

    title

):

    data = df.copy()

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            y=data[category],

            x=data["Registrasi"],

            orientation="h",

            name="Registrasi",

            marker_color="#93C5FD"

        )

    )

    fig.add_trace(

        go.Bar(

            y=data[category],

            x=data["Presensi"],

            orientation="h",

            name="Presensi",

            marker_color="#2563EB"

        )

    )

    fig.update_layout(

        barmode="group",

        title=title,

        xaxis_title="Jumlah",

        yaxis_title=""

    )

    return style(fig)

import streamlit as st

def metric_card(title,value,icon,color):

    st.markdown(f"""
<div style="
background:white;
padding:20px;
border-radius:16px;
box-shadow:0 3px 10px rgba(0,0,0,.08);
">

<div style="
font-size:18px;
color:{color};
font-weight:600;
">

{icon} {title}

</div>

<div style="
font-size:38px;
font-weight:700;
margin-top:10px;
">

{value}

</div>

</div>
""",unsafe_allow_html=True)
    
def cross_line_chart(summary):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=summary["Webinar"],

            y=summary["Registrasi"],

            mode="lines+markers",

            fill="tozeroy",

            fillcolor="rgba(37,99,235,.15)",

            line=dict(
                color="#2563EB",
                width=4
            ),

            name="Registrasi"

        )

    )

    fig.add_trace(

        go.Scatter(

            x=summary["Webinar"],

            y=summary["Presensi"],

            mode="lines+markers",

            fill="tozeroy",

            fillcolor="rgba(249,115,22,.15)",

            line=dict(
                color="#F97316",
                width=4
            ),

            name="Presensi"

        )

    )

    fig.update_layout(

        title="Tren Registrasi vs Presensi",

        height=430

    )

    return style(fig)

