"""
DNS reverse lookup et résolution d'adresses IP.
Trouve le nom d'hôte associé à une IP.
"""

import socket
from typing import Optional


def reverse_dns_lookup(ip: str) -> Optional[str]:
    """
    Effectue un reverse DNS lookup sur une IP.
    Retourne le nom d'hôte, ou None si impossible.
    """
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except (socket.herror, socket.error):
        return None


def forward_dns_lookup(hostname: str) -> Optional[str]:
    """
    Résout un nom d'hôte vers une IP.
    """
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except (socket.herror, socket.error):
        return None


def get_hostname_or_ip(ip: str) -> str:
    """
    Retourne le hostname d'une IP, ou l'IP elle-même si impossible.
    """
    hostname = reverse_dns_lookup(ip)
    return hostname if hostname else ip
