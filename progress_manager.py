import os
import json
from datetime import datetime

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), "user_progress.json")

def load_data():
    if not os.path.exists(PROGRESS_FILE):
        return {}

    try:
        with open(PROGRESS_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                os.remove(PROGRESS_FILE)
                return {}
            return json.loads(content)
    except Exception:
        os.remove(PROGRESS_FILE)
        return {}


def save_data(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_progress():
    return load_data()

def set_progress(key, value):
    data = load_data()
    data[key] = {
        "value": value,
        "timestamp": datetime.now().isoformat()
    }
    save_data(data)

def reset_progress():
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
