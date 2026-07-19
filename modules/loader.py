from pathlib import Path
import pandas as pd
import re

DATA_FOLDER = Path("data")


def load_all_webinars():
    webinars = {}

    for file in DATA_FOLDER.glob("*.xlsx"):

        filename = file.stem.lower()

        match = re.match(r"(\d+)", filename)

        if not match:
            continue

        nomor = int(match.group(1))
        nama_webinar = f"Webinar {nomor}"

        if nama_webinar not in webinars:
            webinars[nama_webinar] = {}

        df = pd.read_excel(file)

        if "registrasi" in filename:
            webinars[nama_webinar]["registrasi"] = df

        elif "presensi" in filename:
            webinars[nama_webinar]["presensi"] = df

    return webinars