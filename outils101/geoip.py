"""
Géolocalisation simple d'une adresse IP (service public gratuit).
Attention : les API publiques ont des limites de requêtes.
Utile pour détecter si un appareil vient d'un endroit anormal.
"""

import json
import urllib.request
from typing import Optional


def geolocate_ip(ip: str) -> Optional[dict]:
    """
    Utilise l'API gratuite ip-api.com pour récupérer la localisation d'une IP.
    Retourne un dictionnaire avec : country, city, lat, lon, isp, etc.
    
    ⚠️  Limité à ~45 requêtes/minute en accès gratuit.
    """
    if ip in ("127.0.0.1", "localhost", "::1"):
        return {"country": "Local", "city": "Localhost", "isp": "Loopback"}

    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,city,lat,lon,isp,org"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            
        if data.get("status") == "success":
            return {
                "country": data.get("country", "?"),
                "city": data.get("city", "?"),
                "lat": data.get("lat", "?"),
                "lon": data.get("lon", "?"),
                "isp": data.get("isp", "?"),
                "org": data.get("org", "?"),
            }
        return None
    except (urllib.error.URLError, json.JSONDecodeError, Exception):
        return None


def evaluate_geo_risk(geo_data: Optional[dict], local_country: str = "CA") -> tuple[str, str]:
    """
    Évalue si une géolocalisation est anormale pour ton réseau.
    Retourne (niveau, message).
    
    local_country : code pays à 2 lettres (CA, FR, US, etc.)
    """
    if not geo_data:
        return "INFO", "Géolocalisation impossible."

    country = geo_data.get("country", "?")
    city = geo_data.get("city", "?")
    isp = geo_data.get("isp", "?")

    if country == "Local" or ip == "127.0.0.1":
        return "OK", "Adresse locale."

    if country != local_country:
        return (
            "ALERTE",
            f"Appareil depuis {city}, {country} (ISP: {isp}). "
            f"Anormal si tu n'as pas de VPN/proxy activé.",
        )

    return "OK", f"{city}, {country} (même pays)."
