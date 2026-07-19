import pandas as pd

from modules.attendance import clean_wa

def get_wa_column(df):
    for col in df.columns:

        c = col.strip().lower()

        if (
            "whatsapp" in c
            or "whats app" in c
            or "wa" in c
        ):
            return col

    return None

# ==========================================================
# SUMMARY
# ==========================================================

def webinar_summary(webinars):

    rows = []

    for nama, data in webinars.items():

        reg = data.get("registrasi")
        pre = data.get("presensi")

        if reg is None:
            continue

        jumlah_reg = len(reg)
        jumlah_pre = len(pre) if pre is not None else 0

        attendance = (
            jumlah_pre / jumlah_reg * 100
            if jumlah_reg > 0
            else 0
        )

        rows.append({

            "Webinar": nama,

            "Registrasi": jumlah_reg,

            "Presensi": jumlah_pre,

            "Attendance Rate": round(attendance, 1)

        })

    return pd.DataFrame(rows)


# ==========================================================
# KPI
# ==========================================================

def overall_summary(webinars):

    summary = webinar_summary(webinars)

    total_webinar = len(summary)

    total_registrasi = summary["Registrasi"].sum()

    total_presensi = summary["Presensi"].sum()

    attendance = (
        total_presensi
        /
        total_registrasi
        * 100
        if total_registrasi > 0
        else 0
    )

    return (

        total_webinar,

        total_registrasi,

        total_presensi,

        round(attendance,1)

    )


# ==========================================================
# PROVINSI
# ==========================================================

def province_summary(webinars):

    hasil = []

    for nama,data in webinars.items():

        reg = data.get("registrasi")
        pre = data.get("presensi")

        if reg is None:
            continue

        reg = reg.copy()

        wa_reg = get_wa_column(reg)

        if wa_reg is None:
            raise ValueError("Kolom WhatsApp pada registrasi tidak ditemukan.")

        reg["WA"] = clean_wa(reg[wa_reg])

        if pre is not None:

            pre = pre.copy()

            wa_pre = get_wa_column(pre)

            if wa_pre is None:
                raise ValueError("Kolom WhatsApp pada presensi tidak ditemukan.")

            pre["WA"] = clean_wa(pre[wa_pre])

            hadir = reg[
                reg["WA"].isin(pre["WA"])
            ]

        else:

            hadir = reg.iloc[0:0]

        reg_count = (

            reg.groupby("Provinsi")

            .size()

            .reset_index(name="Registrasi")

        )

        pre_count = (

            hadir.groupby("Provinsi")

            .size()

            .reset_index(name="Presensi")

        )

        gabung = reg_count.merge(

            pre_count,

            on="Provinsi",

            how="left"

        )

        gabung["Presensi"] = (

            gabung["Presensi"]

            .fillna(0)

        )

        gabung["Webinar"] = nama

        hasil.append(gabung)

    return pd.concat(

        hasil,

        ignore_index=True

    )


# ==========================================================
# STATUS PESERTA
# ==========================================================

def status_summary(webinars):

    hasil = []

    for nama,data in webinars.items():

        reg = data.get("registrasi")
        pre = data.get("presensi")

        if reg is None:
            continue

        reg = reg.copy()

        reg["WA"] = clean_wa(
            reg["Nomor whatsapp aktif"]
        )

        if pre is not None:

            pre = pre.copy()

            pre["WA"] = clean_wa(
                pre["No Whatsapp aktif"]
            )

            hadir = reg[
                reg["WA"].isin(pre["WA"])
            ]

        else:

            hadir = reg.iloc[0:0]

        reg_count = (

            reg.groupby("Status Peserta")

            .size()

            .reset_index(name="Registrasi")

        )

        pre_count = (

            hadir.groupby("Status Peserta")

            .size()

            .reset_index(name="Presensi")

        )

        gabung = reg_count.merge(

            pre_count,

            on="Status Peserta",

            how="left"

        )

        gabung["Presensi"] = (

            gabung["Presensi"]

            .fillna(0)

        )

        gabung["Webinar"] = nama

        hasil.append(gabung)

    return pd.concat(

        hasil,

        ignore_index=True

    )


# ==========================================================
# TOP WEBINAR
# ==========================================================

def top_webinar(webinars):

    summary = webinar_summary(webinars)

    return summary.sort_values(

        "Registrasi",

        ascending=False

    )


# ==========================================================
# TABEL RINGKASAN
# ==========================================================

def summary_table(webinars):

    return webinar_summary(

        webinars

    ).sort_values(

        "Webinar"

    )