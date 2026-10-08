"""
Petit annuaire de préfixes MAC (OUI) -> fabricant.
Ce n'est pas exhaustif, mais ça couvre les marques les plus courantes
dans un réseau domestique (téléphones, ordis, box, Raspberry Pi...).
"""

OUI_TABLE = {
    "3C5AB4": "Google",
    "DCA632": "Raspberry Pi Foundation",
    "B827EB": "Raspberry Pi Foundation",
    "E45F01": "Raspberry Pi Foundation",
    "001A11": "Google",
    "F0D1A9": "Apple",
    "A4C361": "Apple",
    "F4F15A": "Apple",
    "001D4F": "Samsung",
    "5C0A5B": "Samsung",
    "E8508B": "Samsung",
    "9C2A70": "Huawei",
    "00259C": "Huawei",
    "F8A9D0": "Huawei",
    "7C1E52": "Xiaomi",
    "2C4D54": "Xiaomi",
    "641CB0": "TP-Link",
    "A42BB0": "TP-Link",
    "0022F4": "Dell",
    "D4BED9": "Dell",
    "3417EB": "HP",
    "9C8E99": "HP",
    "0023AE": "Cisco",
    "00D0C0": "Cisco",
    "001B21": "Intel",
    "E09D31": "Intel",
}


def get_vendor(mac: str) -> str:
    """Retourne le fabricant probable à partir d'une adresse MAC."""
    prefix = mac.replace(":", "").replace("-", "").upper()[:6]
    return OUI_TABLE.get(prefix, "Inconnu")
