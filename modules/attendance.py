import pandas as pd


def clean_wa(series):
    return (
        series.astype(str)
        .str.replace(r"\.0$", "", regex=True)
        .str.replace(" ", "")
        .str.strip()
    )


def compare_data(registrasi, presensi):

    reg = registrasi.copy()
    pre = presensi.copy()

    reg["WA"] = clean_wa(reg["Nomor whatsapp aktif"])
    pre["WA"] = clean_wa(pre["No Whatsapp aktif"])

    hadir = reg[reg["WA"].isin(pre["WA"])].copy()

    tidak_hadir = reg[~reg["WA"].isin(pre["WA"])].copy()

    attendance_rate = (
        len(hadir) / len(reg) * 100
        if len(reg) > 0
        else 0
    )

    return hadir, tidak_hadir, attendance_rate


def attendance_by_province(registrasi, presensi):

    reg = registrasi.copy()
    pre = presensi.copy()

    reg["WA"] = clean_wa(reg["Nomor whatsapp aktif"])
    pre["WA"] = clean_wa(pre["No Whatsapp aktif"])

    reg_count = (
        reg.groupby("Provinsi")
        .size()
        .reset_index(name="Registrasi")
    )

    hadir = reg[
        reg["WA"].isin(pre["WA"])
    ]

    hadir_count = (
        hadir.groupby("Provinsi")
        .size()
        .reset_index(name="Presensi")
    )

    hasil = reg_count.merge(
        hadir_count,
        on="Provinsi",
        how="left"
    )

    hasil["Presensi"] = hasil["Presensi"].fillna(0)

    hasil["Attendance Rate"] = (
        hasil["Presensi"]
        / hasil["Registrasi"]
        * 100
    ).round(1)

    return hasil.sort_values(
        "Attendance Rate",
        ascending=False
    )


def attendance_by_status(registrasi, presensi):

    reg = registrasi.copy()
    pre = presensi.copy()

    reg["WA"] = clean_wa(reg["Nomor whatsapp aktif"])
    pre["WA"] = clean_wa(pre["No Whatsapp aktif"])

    reg_count = (
        reg.groupby("Status Peserta")
        .size()
        .reset_index(name="Registrasi")
    )

    hadir = reg[
        reg["WA"].isin(pre["WA"])
    ]

    hadir_count = (
        hadir.groupby("Status Peserta")
        .size()
        .reset_index(name="Presensi")
    )

    hasil = reg_count.merge(
        hadir_count,
        on="Status Peserta",
        how="left"
    )

    hasil["Presensi"] = hasil["Presensi"].fillna(0)

    hasil["Attendance Rate"] = (
        hasil["Presensi"]
        / hasil["Registrasi"]
        * 100
    ).round(1)

    return hasil.sort_values(
        "Attendance Rate",
        ascending=False
    )

def summary(registrasi, presensi):

    reg = registrasi.copy()
    pre = presensi.copy()

    reg["WA"] = clean_wa(reg["Nomor whatsapp aktif"])
    pre["WA"] = clean_wa(pre["No Whatsapp aktif"])

    jumlah_registrasi = len(reg)

    jumlah_presensi = reg["WA"].isin(pre["WA"]).sum()

    attendance = (
        jumlah_presensi
        / jumlah_registrasi
        * 100
    ) if jumlah_registrasi else 0

    return (
        jumlah_registrasi,
        jumlah_presensi,
        attendance
    )