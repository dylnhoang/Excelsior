import json
import os
from datetime import datetime

STATUS_FILE = "file_statuses.json"

def load_statuses():
    if not os.path.exists(STATUS_FILE):
        return {}
    with open(STATUS_FILE, "r") as f:
        return json.load(f)

def save_statuses(statuses):
    with open(STATUS_FILE, "w") as f:
        json.dump(statuses, f, indent=2)

def update_status(file_id: str, status: str):
    statuses = load_statuses()
    statuses[file_id] = {
        "status": status,
        "timestamp": datetime.utcnow().isoformat() + "Z"  
    }
    save_statuses(statuses)

def get_status(file_id: str):
    statuses = load_statuses()
    return statuses.get(file_id, {
        "status": "not_found",
        "timestamp": None
    })