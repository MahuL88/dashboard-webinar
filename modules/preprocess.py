import pandas as pd

PROVINSI_MAP = {

    "DKI Jakarta": "DAERAH KHUSUS IBUKOTA JAKARTA",

    "DI Yogyakarta": "DAERAH ISTIMEWA YOGYAKARTA",

    "Kepulauan Bangka Belitung": "KEPULAUAN BANGKA BELITUNG",

    "Kepulauan Riau": "KEPULAUAN RIAU",

    "Nusa Tenggara Timur": "NUSA TENGGARA TIMUR",

    "Jawa Timur": "JAWA TIMUR",

    "Jawa Barat": "JAWA BARAT",

    "Jawa Tengah": "JAWA TENGAH",

    "Banten": "BANTEN",

    "Bali": "BALI",

    "Lampung": "LAMPUNG",

    "Aceh": "ACEH",

    "Riau": "RIAU",

    "Sumatera Utara": "SUMATERA UTARA",

    "Sumatera Selatan": "SUMATERA SELATAN",

    "Sulawesi Selatan": "SULAWESI SELATAN",

    "Sulawesi Tenggara": "SULAWESI TENGGARA",

    "Kalimantan Barat": "KALIMANTAN BARAT",

    "Kalimantan Tengah": "KALIMANTAN TENGAH",

    "Kalimantan Selatan": "KALIMANTAN SELATAN",

    "Kalimantan Timur": "KALIMANTAN TIMUR",

    "Papua Barat Daya": "PAPUA BARAT DAYA"

}

def preprocess_registrasi(df):
    """
    Membersihkan data registrasi.
    """

    df = df.copy()

    # Hilangkan spasi pada nama kolom
    df.columns = df.columns.str.strip()

    # Hilangkan spasi pada isi cell string
    df = df.apply(
        lambda col: col.str.strip() if col.dtype == "object" else col
    )

    # Timestamp menjadi datetime
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(
            df["Timestamp"],
            errors="coerce"
        )
        df["Tanggal"] = df["Timestamp"].dt.date
        df["Jam"] = df["Timestamp"].dt.hour

    # Umur menjadi angka
    if "Usia" in df.columns:
        df["Usia"] = pd.to_numeric(
            df["Usia"],
            errors="coerce"
        )

    # Normalisasi jenis kelamin
    if "Jenis Kelamin" in df.columns:

        df["Jenis Kelamin"] = (
            df["Jenis Kelamin"]
            .str.lower()
            .replace({
                "l": "Laki-laki",
                "laki laki": "Laki-laki",
                "laki-laki": "Laki-laki",
                "pria": "Laki-laki",

                "p": "Perempuan",
                "wanita": "Perempuan",
                "perempuan": "Perempuan"
            })
        )
    if "Provinsi" in df.columns:
        df["Provinsi"] = (
            df["Provinsi"]
            .astype(str)
            .str.strip()
            .replace(PROVINSI_MAP)
)
    return df


def preprocess_presensi(df):
    """
    Membersihkan data presensi.
    """

    df = df.copy()

    df.columns = df.columns.str.strip()

    df = df.apply(
        lambda col: col.str.strip() if col.dtype == "object" else col
    )

    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(
            df["Timestamp"],
            errors="coerce"
        )
        df["Tanggal"] = df["Timestamp"].dt.date

        df["Jam"] = df["Timestamp"].dt.hour

    if "Usia" in df.columns:
        df["Usia"] = pd.to_numeric(
            df["Usia"],
            errors="coerce"
        )

    if "Jenis Kelamin" in df.columns:

        df["Jenis Kelamin"] = (
            df["Jenis Kelamin"]
            .str.lower()
            .replace({
                "l": "Laki-laki",
                "laki laki": "Laki-laki",
                "laki-laki": "Laki-laki",
                "pria": "Laki-laki",

                "p": "Perempuan",
                "wanita": "Perempuan",
                "perempuan": "Perempuan"
            })
        )

    return df

