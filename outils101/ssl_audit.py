"""
Audit SSL/TLS : vérifie le certificat HTTPS d'une cible.
Détecte les certificats expirés, auto-signés, ou avec mauvaises versions TLS.
"""

import socket
import ssl
from datetime import datetime
from typing import Optional, Tuple


def get_ssl_cert_info(ip: str, port: int = 443, timeout: int = 5) -> Optional[dict]:
    """
    Récupère les infos du certificat SSL/TLS d'un serveur.
    Retourne un dict avec : subject, issuer, notBefore, notAfter, version.
    """
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.create_connection((ip, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=ip) as ssock:
                cert = ssock.getpeercert()
                cert_der = ssock.getpeercert(binary_form=True)

                if not cert:
                    return None

                return {
                    "subject": dict(x[0] for x in cert.get("subject", [])),
                    "issuer": dict(x[0] for x in cert.get("issuer", [])),
                    "notBefore": cert.get("notBefore"),
                    "notAfter": cert.get("notAfter"),
                    "version": ssock.getpeercert_chain()[0] if hasattr(ssock, "getpeercert_chain") else "N/A",
                    "san": cert.get("subjectAltName", []),
                }
    except (socket.error, ssl.SSLError, Exception):
        return None


def evaluate_cert(cert_info: Optional[dict]) -> list[Tuple[str, str]]:
    """
    Évalue un certificat SSL et retourne une liste d'alertes.
    Format : [(niveau, message), ...]
    """
    findings = []

    if not cert_info:
        findings.append(("MOYEN", "Pas de certificat SSL/TLS détecté (ou serveur injoignable)."))
        return findings

    # Vérifier l'expiration
    try:
        not_after_str = cert_info.get("notAfter", "")
        # Format: 'Dec 31 23:59:59 2025 GMT'
        if not_after_str:
            not_after = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")
            if datetime.now() > not_after:
                findings.append(("CRITIQUE", f"Certificat EXPIRÉ (depuis {not_after_str})."))
            elif (not_after - datetime.now()).days < 30:
                findings.append(("ALERTE", f"Certificat expire bientôt ({not_after_str})."))
    except (ValueError, TypeError):
        pass

    # Vérifier auto-signature
    subject = cert_info.get("subject", {})
    issuer = cert_info.get("issuer", {})
    if subject == issuer:
        findings.append(("MOYEN", "Certificat auto-signé (pas de CA reconnue)."))

    # Vérifier le CN (Common Name)
    cn = subject.get("commonName", subject.get("CN", "Unknown"))
    if not cn or cn == "Unknown":
        findings.append(("ALERTE", "Nom d'hôte du certificat absent ou invalide."))

    if not findings:
        findings.append(("OK", f"Certificat valide pour {cn}."))

    return findings


def audit_https(ip: str, port: int = 443) -> None:
    """
    Audit complet SSL/TLS d'une cible.
    """
    print(f"\n🔐 Audit SSL/TLS de {ip}:{port}...")
    cert = get_ssl_cert_info(ip, port)
    findings = evaluate_cert(cert)

    for niveau, msg in findings:
        print(f"   [{niveau}] {msg}")
