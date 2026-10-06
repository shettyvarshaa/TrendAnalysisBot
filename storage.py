import json
import os
from pathlib import Path


BASE_DATA_FILE = Path(__file__).with_name("sales_data.json")
DATA_FILE = (
    Path("/tmp/sales_data.json")
    if os.environ.get("VERCEL")
    else BASE_DATA_FILE
)


def load_data():
    if not DATA_FILE.exists():
        if DATA_FILE != BASE_DATA_FILE and BASE_DATA_FILE.exists():
            source = BASE_DATA_FILE
        else:
            return []
    else:
        source = DATA_FILE

    try:
        with source.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
