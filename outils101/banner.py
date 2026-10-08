"""
Récupération de bannière (banner grabbing) sur un port ouvert.
But : identifier la version d'un service pour repérer un logiciel
obsolète / connu comme vulnérable. Aucune exploitation n'est faite ici.
"""

import socket

HTTP_PORTS = {80, 8080, 443, 8443}


def grab_banner(ip: str, port: int, timeout: float = 1.5):
    """Essaie de récupérer la bannière d'un service. Retourne None si échec."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((ip, port))

            if port in HTTP_PORTS:
                sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")

            data = sock.recv(1024)
            if not data:
                return None

            texte = data.decode(errors="ignore")

            if port in HTTP_PORTS:
                for ligne in texte.splitlines():
                    if ligne.lower().startswith("server:"):
                        return ligne.split(":", 1)[1].strip()
                return None

            return texte.strip()
    except (socket.timeout, socket.error, OSError):
        return None
