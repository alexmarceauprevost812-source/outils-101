"""
Scan de ports simple (TCP connect) sur une IP de TON réseau local.
But : voir quels services tournent sur un appareil (web, SSH, SMB...),
pas d'exploitation de faille.
"""

import socket

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    548: "AFP",
    554: "RTSP",
    3389: "RDP",
    5900: "VNC",
    8080: "HTTP-alt",
    8443: "HTTPS-alt",
}


def scan_ports(ip: str, ports=None, timeout: float = 0.5) -> list:
    """Retourne la liste des (port, nom_service) ouverts sur l'IP donnée."""
    if ports is None:
        ports = COMMON_PORTS.keys()

    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            if sock.connect_ex((ip, port)) == 0:
                open_ports.append((port, COMMON_PORTS.get(port, "Inconnu")))
        except socket.error:
            pass
        finally:
            sock.close()
    return open_ports
