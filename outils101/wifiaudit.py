"""
Audit basique de la sécurité WiFi : liste les réseaux visibles autour de
toi et évalue leur niveau de chiffrement (ouvert, WEP, WPA, WPA2, WPA3).
But : repérer si TON réseau utilise un chiffrement faible, ce qui explique
souvent comment un appareil inconnu a pu s'y connecter.
Aucune tentative de connexion, de cassage ou de désauthentification n'est
faite ici : on lit seulement ce que le système d'exploitation voit déjà.
"""

import platform
import re
import subprocess


def _scan_linux():
    try:
        out = subprocess.run(
            ["nmcli", "-t", "-f", "SSID,SECURITY,SIGNAL", "dev", "wifi", "list"],
            capture_output=True, text=True, timeout=15, check=True,
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None

    reseaux = []
    for ligne in out.splitlines():
        if not ligne.strip():
            continue
        parts = ligne.split(":")
        if len(parts) < 3:
            continue
        ssid, security, signal = parts[0], parts[1], parts[-1]
        reseaux.append({"ssid": ssid or "(caché)", "security": security or "--", "signal": signal})
    return reseaux


def _scan_windows():
    try:
        out = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            capture_output=True, text=True, timeout=15, check=True,
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None

    reseaux = []
    ssid, security, signal = None, "--", "?"
    for ligne in out.splitlines():
        ligne = ligne.strip()
        if ligne.startswith("SSID"):
            if ssid is not None:
                reseaux.append({"ssid": ssid, "security": security, "signal": signal})
            match = re.search(r":\s*(.*)", ligne)
            ssid = match.group(1).strip() if match else "(caché)"
            security, signal = "--", "?"
        elif "Authentication" in ligne:
            security = ligne.split(":", 1)[1].strip()
        elif "Signal" in ligne:
            signal = ligne.split(":", 1)[1].strip()
    if ssid is not None:
        reseaux.append({"ssid": ssid, "security": security, "signal": signal})
    return reseaux


def scan_wifi_networks():
    """Retourne la liste des réseaux WiFi visibles, ou None si impossible
    (outil système manquant : nmcli sur Linux, ou netsh sur Windows)."""
    systeme = platform.system()
    if systeme == "Linux":
        return _scan_linux()
    if systeme == "Windows":
        return _scan_windows()
    return None


def evaluate_security(security: str):
    """Retourne (niveau, message) selon le type de sécurité détecté."""
    s = (security or "").upper()
    if s in ("", "--", "NONE", "OPEN"):
        return "CRITIQUE", "Réseau ouvert, sans chiffrement : n'importe qui peut s'y connecter."
    if "WEP" in s:
        return "CRITIQUE", "WEP se casse en quelques minutes avec des outils publics."
    if "WPA3" in s:
        return "BON", "WPA3 : chiffrement récent et solide."
    if "WPA2" in s:
        return "OK", "WPA2 : correct si le mot de passe est fort (12+ caractères, pas un mot courant)."
    if "WPA" in s:
        return "MOYEN", "WPA (v1) est ancien, préfère WPA2/WPA3 si ton routeur le permet."
    return "INCONNU", "Type de sécurité non reconnu."
