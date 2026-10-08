"""
Petite base de signatures de versions de logiciels obsolètes ou connues
comme vulnérables. Objectif : INFORMER, pas exploiter.
Si tu reconnais un de ces services sur ton réseau, pense à le mettre à jour.
"""

import re

SIGNATURES = [
    (r"vsftpd 2\.3\.4", "CRITIQUE",
     "vsftpd 2.3.4 contient une porte dérobée connue (CVE-2011-2523). Mets à jour immédiatement."),
    (r"OpenSSH_[1-6]\.", "ÉLEVÉ",
     "Version d'OpenSSH ancienne, plusieurs failles connues. Mets à jour."),
    (r"Apache/1\.", "ÉLEVÉ", "Apache 1.x est obsolète depuis très longtemps."),
    (r"Apache/2\.[0-2]\.", "MOYEN", "Version d'Apache ancienne, non maintenue."),
    (r"Microsoft-IIS/[1-6]\.", "ÉLEVÉ",
     "IIS ancien, fin de support, plusieurs failles connues."),
    (r"nginx/0\.", "MOYEN", "Version très ancienne de nginx."),
    (r"Samba [1-3]\.", "ÉLEVÉ",
     "Version de Samba ancienne (ex: faille type SambaCry possible)."),
    (r"ProFTPD 1\.3\.[0-4]", "ÉLEVÉ", "Ancienne version de ProFTPD, failles connues."),
]


def check_banner(banner: str):
    """Retourne une liste d'alertes (niveau, message) correspondant à la bannière."""
    if not banner:
        return []
    alertes = []
    for pattern, niveau, message in SIGNATURES:
        if re.search(pattern, banner, re.IGNORECASE):
            alertes.append((niveau, message))
    return alertes
