"""
Scan ARP du réseau local : détecte les appareils connectés (IP + MAC).
Nécessite les droits administrateur/root (envoi de paquets bruts).
"""

import ipaddress
import socket

from scapy.all import ARP, Ether, srp


def get_local_network() -> str:
    """Devine le réseau local (ex: 192.168.1.0/24) à partir de l'IP locale."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    network = ipaddress.ip_network(local_ip + "/24", strict=False)
    return str(network)


def arp_scan(network: str, timeout: int = 3) -> list:
    """Envoie des requêtes ARP broadcast et retourne les appareils qui répondent."""
    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=timeout, verbose=0)[0]

    devices = []
    for _sent, received in result:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})
    return devices
