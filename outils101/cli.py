"""
Interface en ligne de commande d'Outils 101.
"""

import sys
from datetime import datetime

from . import storage, vendor, wifiaudit, automation, dnslookup, geoip, ssl_audit
from .banner import grab_banner
from .portscan import scan_ports
from .scanner import arp_scan, get_local_network
from .vulndb import check_banner
from .report_generator import generate_html_report, export_to_json
from .traffic_monitor import display_live_monitor, detect_unusual_activity
from .mac_spoofing_detector import MACSpoofer
from .wifi_security_audit import WiFiSecurityAudit
from .intrusion_detection import IntrusionDetectionSystem
from .honeypot import HoneypotServer
from .forensics import NetworkForensics
from .compliance import ComplianceChecker

BANNER = r"""
  ___       _   _ _          _  __  _
 / _ \ _  _| |_(_) |___   _ | |/ _|/ |
| | | | || |  _| | (_-<  | || |  _| |
 \___/ \_,_|\__|_|_/__/  |_||_|_|  |_|

      Outils 101 - Surveillance WiFi locale
"""

AVERTISSEMENT = (
    "⚠️  À utiliser UNIQUEMENT sur ton propre réseau WiFi.\n"
    "⚠️  Le scan réseau nécessite les droits administrateur/root.\n"
)


def afficher_resume(devices: dict) -> None:
    if not devices:
        print("Aucun appareil connu pour le moment. Lance un scan (option 1).")
        return

    print(f"\n{'MAC':<20}{'IP':<16}{'Nom':<20}{'Fabricant':<20}{'Dernière vue'}")
    print("-" * 95)
    for mac, info in devices.items():
        nom = info.get("name") or "(non nommé)"
        print(
            f"{mac:<20}{info.get('ip', ''):<16}{nom:<20}"
            f"{info.get('vendor', ''):<20}{info.get('last_seen', '')}"
        )


def action_scan(devices: dict) -> None:
    reseau_defaut = get_local_network()
    reseau = input(f"Réseau à scanner [{reseau_defaut}] : ").strip() or reseau_defaut

    print(f"\n🔎 Scan ARP sur {reseau} en cours (ça peut prendre quelques secondes)...")
    try:
        trouves = arp_scan(reseau)
    except PermissionError:
        print("❌ Ce scan nécessite les droits administrateur/root (essaie avec sudo).")
        return
    except Exception as e:  # scapy peut lever plusieurs types d'erreurs selon l'OS
        print(f"❌ Erreur pendant le scan : {e}")
        return

    if not trouves:
        print("Aucun appareil détecté. Vérifie que tu es bien connecté au réseau.")
        return

    nouveaux = []
    for d in trouves:
        v = vendor.get_vendor(d["mac"])
        if storage.update_device(devices, d["mac"], d["ip"], v):
            nouveaux.append(d)

    storage.save_devices(devices)

    print(f"\n✅ {len(trouves)} appareil(s) détecté(s) sur le réseau.")
    if nouveaux:
        print(f"\n⚠️  {len(nouveaux)} NOUVEL(LE) APPAREIL(S) détecté(s) :")
        for d in nouveaux:
            v = vendor.get_vendor(d["mac"])
            print(f"   - IP: {d['ip']}  MAC: {d['mac']}  Fabricant: {v}")
        print("   -> Si tu ne reconnais pas un appareil, pense à changer ton mot de passe WiFi.")
    else:
        print("Aucun nouvel appareil (tous déjà connus).")


def action_renommer(devices: dict) -> None:
    afficher_resume(devices)
    mac = input("\nAdresse MAC de l'appareil à renommer : ").strip().lower()
    if mac not in devices:
        print("❌ MAC inconnue. Fais d'abord un scan (option 1).")
        return
    nom = input("Nouveau nom pour cet appareil : ").strip()
    storage.rename_device(devices, mac, nom)
    storage.save_devices(devices)
    print(f"✅ Appareil {mac} renommé en '{nom}'.")


def action_portscan(devices: dict) -> None:
    afficher_resume(devices)
    ip = input("\nIP de l'appareil à scanner (ports) : ").strip()
    if not ip:
        print("IP vide, annulé.")
        return

    print(f"\n🔓 Scan des ports courants sur {ip}...")
    ouverts = scan_ports(ip)
    if not ouverts:
        print("Aucun port courant ouvert détecté (ou appareil injoignable).")
    else:
        print(f"Ports ouverts sur {ip} :")
        for port, service in ouverts:
            print(f"   - {port}/tcp  ({service})")


def action_vulncheck(devices: dict) -> None:
    afficher_resume(devices)
    ip = input("\nIP de l'appareil à auditer : ").strip()
    if not ip:
        print("IP vide, annulé.")
        return

    print(f"\n🔓 Scan des ports courants sur {ip}...")
    ouverts = scan_ports(ip)
    if not ouverts:
        print("Aucun port courant ouvert détecté (ou appareil injoignable).")
        return

    print(f"\n🔎 Analyse des services détectés sur {ip} :")
    rien_trouve = True
    for port, service in ouverts:
        banniere = grab_banner(ip, port)
        if not banniere:
            print(f"   - {port}/tcp ({service}) : bannière non récupérable.")
            continue

        print(f"   - {port}/tcp ({service}) : {banniere}")
        for niveau, message in check_banner(banniere):
            rien_trouve = False
            print(f"       ⚠️  [{niveau}] {message}")

    if rien_trouve:
        print("\n✅ Aucune version connue comme vulnérable dans notre base locale.")
    print("\nℹ️  Cette analyse est informative : elle ne tente aucune exploitation.")


def action_wifiaudit() -> None:
    print("\n📡 Scan des réseaux WiFi visibles en cours...")
    reseaux = wifiaudit.scan_wifi_networks()

    if reseaux is None:
        print(
            "❌ Impossible de scanner le WiFi ici.\n"
            "   - Linux : installe 'network-manager' (commande nmcli).\n"
            "   - Windows : vérifie que 'netsh' est disponible (normalement oui).\n"
        )
        return

    if not reseaux:
        print("Aucun réseau WiFi détecté (carte WiFi désactivée ou hors de portée).")
        return

    print(f"\n{'SSID':<25}{'Sécurité':<15}{'Signal':<10}{'Évaluation'}")
    print("-" * 85)
    for r in reseaux:
        niveau, message = wifiaudit.evaluate_security(r["security"])
        print(f"{r['ssid']:<25}{r['security']:<15}{r['signal']:<10}[{niveau}]")
        if niveau in ("CRITIQUE", "MOYEN"):
            print(f"      ⚠️  {message}")

    print(
        "\nℹ️  Repère TON réseau dans la liste (SSID). S'il est marqué "
        "CRITIQUE ou MOYEN, c'est probablement par là qu'un appareil "
        "inconnu a pu se connecter. Passe en WPA2/WPA3 avec un mot de "
        "passe fort si ce n'est pas déjà le cas."
    )


def action_dnslookup() -> None:
    afficher_resume(storage.load_devices())
    ip = input("\nIP à analyser (reverse DNS lookup) : ").strip()
    if not ip:
        print("IP vide, annulé.")
        return

    hostname = dnslookup.reverse_dns_lookup(ip)
    if hostname:
        print(f"✅ {ip} → {hostname}")
    else:
        print(f"ℹ️  Pas de reverse DNS disponible pour {ip} (appareil sans hostname).")


def action_geoip() -> None:
    afficher_resume(storage.load_devices())
    ip = input("\nIP à géolocaliser : ").strip()
    if not ip:
        print("IP vide, annulé.")
        return

    print(f"\n🌍 Géolocalisation de {ip}...")
    geo = geoip.geolocate_ip(ip)
    
    if not geo:
        print(f"❌ Impossible de géolocaliser {ip} (pas de connexion ou IP invalide).")
        return

    print(f"   Pays : {geo.get('country', '?')}")
    print(f"   Ville : {geo.get('city', '?')}")
    print(f"   Coordonnées : {geo.get('lat', '?')}, {geo.get('lon', '?')}")
    print(f"   ISP : {geo.get('isp', '?')}")
    print(f"   Org : {geo.get('org', '?')}")

    # Évaluer
    local_country = input("\nCode pays LOCAL (ex: CA, FR, US) [CA] : ").strip().upper() or "CA"
    niveau, message = geoip.evaluate_geo_risk(geo, local_country)
    print(f"   [{niveau}] {message}")


def action_ssl_audit() -> None:
    afficher_resume(storage.load_devices())
    ip = input("\nIP à auditer (SSL/TLS) : ").strip()
    if not ip:
        print("IP vide, annulé.")
        return

    port_str = input("Port HTTPS [443] : ").strip() or "443"
    try:
        port = int(port_str)
    except ValueError:
        print("Port invalide.")
        return

    ssl_audit.audit_https(ip, port)


def action_automation() -> None:
    print("\n🤖 Mode automatisation (scan continu).")
    reseau = input("Réseau à scanner [auto-detect] : ").strip() or None
    interval_str = input("Intervalle entre scans en secondes [60] : ").strip() or "60"
    
    try:
        interval = int(interval_str)
    except ValueError:
        print("Intervalle invalide.")
        return

    automation.auto_scan_and_log(reseau, interval)


def action_view_alerts() -> None:
    print("\n📋 Dernières alertes :")
    automation.show_alerts(limit=30)


def action_view_history() -> None:
    automation.show_history()


def action_generate_report(devices: dict) -> None:
    """Génère un rapport HTML complet du réseau."""
    alerts = automation.load_alerts()
    history = automation.load_history()
    
    devices_list = [
        {
            "ip": info.get("ip"),
            "mac": mac,
            "name": info.get("name", "(sans nom)"),
            "vendor": info.get("vendor", "Inconnu"),
            "last_seen": info.get("last_seen")
        }
        for mac, info in devices.items()
    ]
    
    html_file = generate_html_report(devices_list, alerts, history)
    
    print(f"\n✅ Rapport HTML généré avec succès!")
    print(f"📄 Fichier: {html_file}")
    print("\nLe rapport contient:")
    print("  - Résumé des statistiques réseau")
    print("  - Liste complète des appareils")
    print("  - Alertes récentes")
    print("  - Historique des connexions")
    print("\n💡 Ouvre le fichier dans un navigateur pour voir le rapport.")
    
    # Optionnel : exporter aussi en JSON
    export = input("\nExporter aussi les données en JSON? (o/n) [n] : ").strip().lower()
    if export == "o":
        json_file = export_to_json(devices_list, alerts, history)
        print(f"✅ Données JSON exportées: {json_file}")


def action_traffic_monitor() -> None:
    """Lance le monitoring trafic réseau en direct."""
    print("\n" + "="*80)
    print("📡 MONITORING TRAFIC RÉSEAU")
    print("="*80)
    
    duration_str = input("Durée du monitoring en secondes [30] : ").strip() or "30"
    try:
        duration = int(duration_str)
    except ValueError:
        print("Durée invalide.")
        return
    
    display_live_monitor(duration)
    
    # Option détection anormale
    detect = input("\nVérifier les activités anormales? (o/n) [o] : ").strip().lower() or "o"
    if detect == "o":
        detect_unusual_activity()


def action_mac_spoofing(devices: dict) -> None:
    """Détecte les tentatives de MAC spoofing."""
    devices_list = [
        {
            "ip": info.get("ip"),
            "mac": mac,
            "name": info.get("name", "(sans nom)"),
            "vendor": info.get("vendor", "Inconnu")
        }
        for mac, info in devices.items()
    ]
    
    spoofer = MACSpoofer()
    spoofer.generate_report(devices_list)


def action_advanced_wifi_audit() -> None:
    """Audit avancé sécurité WiFi."""
    audit = WiFiSecurityAudit()
    audit.generate_report()


def action_ids_system(devices: dict) -> None:
    """Lance le système de détection d'intrusion."""
    devices_list = [
        {
            "ip": info.get("ip"),
            "mac": mac,
            "name": info.get("name", "(sans nom)"),
            "vendor": info.get("vendor", "Inconnu"),
            "open_ports": []
        }
        for mac, info in devices.items()
    ]
    
    ids = IntrusionDetectionSystem()
    issues = ids.generate_ids_report(devices_list)
    
    if issues:
        export = input("\nExporter les menaces détectées? (o/n) [o] : ").strip().lower() or "o"
        if export == "o":
            from pathlib import Path
            import json
            
            threat_dir = Path("threats")
            threat_dir.mkdir(exist_ok=True)
            
            filename = threat_dir / f"threats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w") as f:
                json.dump(issues, f, indent=2)
            
            print(f"\n✅ Menaces exportées: {filename}")


def action_honeypot() -> None:
    """Lance le honeypot (piège à attaquants)."""
    honeypot = HoneypotServer()
    
    print("\n" + "="*70)
    print("🍯 HONEYPOT - Piège à Attaquants")
    print("="*70)
    print("\nLe honeypot va simuler des services (SSH, Telnet, HTTP)")
    print("et enregistrer toute tentative de connexion suspecte.\n")
    
    print("Options:")
    print("1. Démarrer le honeypot (ports 22, 23, 80)")
    print("2. Afficher les alertes détectées")
    print("3. Quitter")
    
    choice = input("\nChoisir une option (1-3): ").strip()
    
    if choice == "1":
        print("\n⚠️  Le honeypot nécessite les droits root/admin")
        honeypot.start_honeypot([22, 23, 80])
    elif choice == "2":
        honeypot.show_alerts_summary()
    else:
        print("Retour au menu principal...")


def action_forensics() -> None:
    """Lance l'analyse forensique des logs."""
    forensics = NetworkForensics()
    
    print("\n" + "="*70)
    print("🔬 NETWORK FORENSICS - Analyse des Incidents")
    print("="*70)
    print("\nCet outil analyse les logs système pour détecter:")
    print("  • Tentatives de brute-force")
    print("  • Injections SQL/XSS")
    print("  • Escalade de privilèges")
    print("  • Signatures de hack")
    print("  • Exfiltration de données\n")
    
    print("⚠️  Cela nécessite l'accès aux logs système (root requis)\n")
    
    report = forensics.generate_forensics_report()
    forensics.display_report(report)


def action_compliance() -> None:
    """Lance la vérification de conformité."""
    checker = ComplianceChecker()
    
    print("\n" + "="*70)
    print("✅ VÉRIFICATION DE CONFORMITÉ SÉCURITÉ")
    print("="*70)
    print("\nCet outil teste la conformité de ta config système avec")
    print("les meilleures pratiques de sécurité réseau.\n")
    
    checker.run_all_checks()


MENU = """
1. Scanner le réseau (voir les appareils connectés)
2. Afficher le résumé des appareils connus
3. Renommer un appareil
4. Scanner les ports ouverts d'un appareil
5. Auditer un appareil (versions de services vulnérables connues)
6. Auditer la sécurité du WiFi (chiffrement, WPA/WEP...)
7. DNS Reverse Lookup (trouver le hostname d'une IP)
8. Géolocalisation d'IP (détecte si un appareil vient d'ailleurs)
9. Audit SSL/TLS (certificat HTTPS, sécurité)
10. Automatisation (scan continu + historique auto)
11. Voir les alertes (NEW_DEVICE, DISCONNECTED, etc.)
12. Voir l'historique des appareils
13. 📊 Générer un rapport HTML complet
14. 📡 Monitoring trafic réseau en direct
15. 🚨 Détection MAC spoofing
16. 🛡️ Audit avancé sécurité WiFi
17. 🚨 Système de détection d'intrusion (IDS)
18. 🍯 HONEYPOT - Piège à Attaquants
19. 🔬 FORENSICS - Analyse des Incidents
20. ✅ COMPLIANCE - Vérification de Conformité
21. Quitter
"""


def main() -> None:
    print(BANNER)
    print(AVERTISSEMENT)

    devices = storage.load_devices()

    while True:
        print(MENU)
        choix = input("Choix : ").strip()

        if choix == "1":
            action_scan(devices)
        elif choix == "2":
            afficher_resume(devices)
        elif choix == "3":
            action_renommer(devices)
        elif choix == "4":
            action_portscan(devices)
        elif choix == "5":
            action_vulncheck(devices)
        elif choix == "6":
            action_wifiaudit()
        elif choix == "7":
            action_dnslookup()
        elif choix == "8":
            action_geoip()
        elif choix == "9":
            action_ssl_audit()
        elif choix == "10":
            action_automation()
        elif choix == "11":
            action_view_alerts()
        elif choix == "12":
            action_view_history()
        elif choix == "13":
            action_generate_report(devices)
        elif choix == "14":
            action_traffic_monitor()
        elif choix == "15":
            action_mac_spoofing(devices)
        elif choix == "16":
            action_advanced_wifi_audit()
        elif choix == "17":
            action_ids_system(devices)
        elif choix == "18":
            action_honeypot()
        elif choix == "19":
            action_forensics()
        elif choix == "20":
            action_compliance()
        elif choix == "21":
            print("À bientôt 👋")
            sys.exit(0)
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()
