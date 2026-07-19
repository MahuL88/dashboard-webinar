import pandas as pd


def total_peserta(df):
    return len(df)


def jumlah_laki(df):

    if "Jenis Kelamin" not in df.columns:
        return 0

    return (df["Jenis Kelamin"] == "Laki-laki").sum()


def jumlah_perempuan(df):

    if "Jenis Kelamin" not in df.columns:
        return 0

    return (df["Jenis Kelamin"] == "Perempuan").sum()


def rata_usia(df):

    if "Usia" not in df.columns:
        return 0

    return round(df["Usia"].mean(), 1)


def jumlah_provinsi(df):

    if "Provinsi" not in df.columns:
        return 0

    return df["Provinsi"].nunique()


def jumlah_status(df, column):

    if column not in df.columns:
        return 0

    return df[column].nunique()