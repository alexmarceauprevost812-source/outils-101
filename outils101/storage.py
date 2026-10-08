"""
Gère la base locale des appareils connus (fichier JSON dans le
répertoire courant : devices.json).
"""

import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.getcwd(), "devices.json")


def load_devices() -> dict:
    if not os.path.exists(DB_PATH):
        return {}
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_devices(devices: dict) -> None:
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(devices, f, indent=2, ensure_ascii=False)


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def update_device(devices: dict, mac: str, ip: str, vendor: str) -> bool:
    """Ajoute ou met à jour un appareil. Retourne True si c'est un NOUVEL appareil."""
    mac = mac.lower()
    if mac in devices:
        devices[mac]["ip"] = ip
        devices[mac]["last_seen"] = now_str()
        return False

    devices[mac] = {
        "name": None,
        "ip": ip,
        "vendor": vendor,
        "first_seen": now_str(),
        "last_seen": now_str(),
    }
    return True


def rename_device(devices: dict, mac: str, name: str) -> bool:
    mac = mac.lower()
    if mac in devices:
        devices[mac]["name"] = name
        return True
    return False
