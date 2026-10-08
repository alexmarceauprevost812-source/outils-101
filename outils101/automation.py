"""
Automatisation : scan continu du réseau et logging dans des fichiers.
Crée un historique détaillé des appareils et alertes.
"""

import json
import os
import time
from datetime import datetime
from typing import List, Dict
from . import scanner, vendor, storage


LOG_DIR = os.path.join(os.getcwd(), "logs")
HISTORY_FILE = os.path.join(LOG_DIR, "devices_history.json")
ALERTS_FILE = os.path.join(LOG_DIR, "alerts.json")


def init_log_dir() -> None:
    """Crée le répertoire logs s'il n'existe pas."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def log_alert(alert_type: str, message: str, device_mac: str = "", device_ip: str = "") -> None:
    """
    Enregistre une alerte dans alerts.json.
    alert_type : "NEW_DEVICE", "DEVICE_DISCONNECTED", "PORT_CHANGE", etc.
    """
    init_log_dir()
    
    alerts = []
    if os.path.exists(ALERTS_FILE):
        try:
            with open(ALERTS_FILE, "r", encoding="utf-8") as f:
                alerts = json.load(f)
        except json.JSONDecodeError:
            alerts = []

    alert = {
        "timestamp": datetime.now().isoformat(),
        "type": alert_type,
        "message": message,
        "device_mac": device_mac,
        "device_ip": device_ip,
    }
    alerts.append(alert)

    with open(ALERTS_FILE, "w", encoding="utf-8") as f:
        json.dump(alerts, f, indent=2, ensure_ascii=False)


def log_device_to_history(mac: str, ip: str, vendor_name: str, action: str) -> None:
    """
    Enregistre chaque appareil détecté dans l'historique.
    action : "DISCOVERED", "CONNECTED", "DISCONNECTED", etc.
    """
    init_log_dir()
    
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

    entry = {
        "timestamp": datetime.now().isoformat(),
        "mac": mac.lower(),
        "ip": ip,
        "vendor": vendor_name,
        "action": action,
    }
    history.append(entry)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def auto_scan_and_log(reseau: str = None, interval_seconds: int = 60) -> None:
    """
    Lance un scan périodique du réseau et log tout automatiquement.
    
    reseau : le réseau à scanner (ex: "192.168.1.0/24")
    interval_seconds : attendre N secondes entre chaque scan
    """
    if reseau is None:
        reseau = scanner.get_local_network()
    
    devices = storage.load_devices()
    print(f"\n🤖 Scan automatique démarré sur {reseau}.")
    print(f"    Scan chaque {interval_seconds} secondes (Ctrl+C pour arrêter).")
    print(f"    Logs : {LOG_DIR}/\n")

    devices_seen_previous = set(devices.keys())

    try:
        while True:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Scan en cours...")
            try:
                trouves = scanner.arp_scan(reseau)
            except Exception as e:
                print(f"  ❌ Erreur scan : {e}")
                time.sleep(interval_seconds)
                continue

            devices_seen_now = set()
            for d in trouves:
                mac = d["mac"].lower()
                ip = d["ip"]
                v = vendor.get_vendor(mac)
                
                devices_seen_now.add(mac)
                
                if mac not in devices:
                    # Nouvel appareil
                    print(f"  ⚠️  NOUVEL APPAREIL : {ip} ({mac}) - {v}")
                    storage.update_device(devices, mac, ip, v)
                    log_alert("NEW_DEVICE", f"Nouvel appareil détecté", mac, ip)
                    log_device_to_history(mac, ip, v, "DISCOVERED")
                else:
                    # Appareil connu, mise à jour IP/vendor
                    old_ip = devices[mac].get("ip")
                    if old_ip != ip:
                        print(f"  ℹ️  {mac} : IP changée {old_ip} → {ip}")
                        log_alert("IP_CHANGE", f"IP changée de {old_ip} à {ip}", mac, ip)
                    devices[mac]["ip"] = ip
                    devices[mac]["vendor"] = v
                    devices[mac]["last_seen"] = storage.now_str()
                    log_device_to_history(mac, ip, v, "CONNECTED")

            # Détecter les déconnexions
            disconnected = devices_seen_previous - devices_seen_now
            for mac in disconnected:
                ip = devices[mac].get("ip", "?")
                print(f"  ℹ️  DÉCONNECTÉ : {mac} ({ip})")
                log_alert("DEVICE_DISCONNECTED", f"Appareil déconnecté", mac, ip)
                log_device_to_history(mac, ip, devices[mac].get("vendor", "?"), "DISCONNECTED")

            devices_seen_previous = devices_seen_now
            storage.save_devices(devices)
            
            print(f"  ✅ {len(trouves)} appareil(s) actuellement connecté(s).")
            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\n\n🛑 Scan automatique arrêté.")
        print(f"📊 Historique sauvegardé dans {HISTORY_FILE}")
        print(f"📋 Alertes sauvegardées dans {ALERTS_FILE}")


def show_alerts(limit: int = 20) -> None:
    """Affiche les dernières alertes."""
    init_log_dir()
    
    if not os.path.exists(ALERTS_FILE):
        print("Aucune alerte enregistrée pour le moment.")
        return

    try:
        with open(ALERTS_FILE, "r", encoding="utf-8") as f:
            alerts = json.load(f)
    except json.JSONDecodeError:
        print("Erreur lecture des alertes.")
        return

    if not alerts:
        print("Aucune alerte enregistrée pour le moment.")
        return

    # Afficher les N dernières
    alerts = alerts[-limit:]
    print(f"\n{'Timestamp':<20}{'Type':<20}{'MAC':<20}{'IP':<16}{'Message':<40}")
    print("-" * 120)
    for alert in alerts:
        ts = alert.get("timestamp", "")[:19]
        typ = alert.get("type", "")
        mac = alert.get("device_mac", "")
        ip = alert.get("device_ip", "")
        msg = alert.get("message", "")[:40]
        print(f"{ts:<20}{typ:<20}{mac:<20}{ip:<16}{msg:<40}")


def show_history() -> None:
    """Affiche l'historique complet des appareils."""
    init_log_dir()
    
    if not os.path.exists(HISTORY_FILE):
        print("Aucun historique pour le moment.")
        return

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except json.JSONDecodeError:
        print("Erreur lecture de l'historique.")
        return

    if not history:
        print("Aucun historique pour le moment.")
        return

    # Grouper par MAC
    by_mac = {}
    for entry in history:
        mac = entry.get("mac", "")
        if mac not in by_mac:
            by_mac[mac] = []
        by_mac[mac].append(entry)

    print(f"\n📊 Historique des appareils ({len(history)} entrées) :\n")
    for mac in sorted(by_mac.keys()):
        entries = by_mac[mac]
        vendor_name = entries[-1].get("vendor", "?")
        first_seen = entries[0].get("timestamp", "")
        last_seen = entries[-1].get("timestamp", "")
        actions = ", ".join(set(e.get("action", "") for e in entries))
        print(f"  MAC: {mac}")
        print(f"      Vendor: {vendor_name}")
        print(f"      Premier vu : {first_seen}")
        print(f"      Dernier vu : {last_seen}")
        print(f"      Actions : {actions}")
        print()
