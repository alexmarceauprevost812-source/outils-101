"""
Système de détection d'intrusion basique.
Détecte les comportements anormaux du réseau (DDoS, scans agressifs, etc.).
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict


class IntrusionDetectionSystem:
    
    def __init__(self, history_file="logs/devices_history.json", 
                 alerts_file="logs/alerts.json"):
        self.history_file = Path(history_file)
        self.alerts_file = Path(alerts_file)
        self.thresholds = {
            "new_devices_per_hour": 10,  # Plus de 10 nouveaux appareils/heure = suspect
            "connection_rate": 50,        # Plus de 50 connexions simultanées
            "port_scans": 20,             # Plus de 20 ports en peu de temps
            "failed_auth_attempts": 5,    # Plus de 5 tentatives de connexion échouées
            "mac_changes_per_device": 3,  # Une MAC changeant 3+ fois = spoofing
        }
    
    def _load_history(self):
        """Charge l'historique des appareils."""
        if self.history_file.exists():
            try:
                with open(self.history_file, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _load_alerts(self):
        """Charge les alertes précédentes."""
        if self.alerts_file.exists():
            try:
                with open(self.alerts_file, "r") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def detect_ddos_attempt(self, current_devices):
        """
        Détecte une possibilité d'attaque DDoS.
        Critères : trop de connexions simultanées d'une même source.
        """
        issues = []
        
        # Analyser les connexions par IP source
        ip_connections = defaultdict(int)
        
        for device in current_devices:
            ip = device.get("ip")
            if ip:
                ip_connections[ip] += 1
        
        # Vérifier les seuils
        for ip, count in ip_connections.items():
            if count > self.thresholds["connection_rate"]:
                issues.append({
                    "type": "POSSIBLE_DDOS",
                    "ip": ip,
                    "connections": count,
                    "threshold": self.thresholds["connection_rate"],
                    "risk": "🔴 CRITIQUE",
                    "description": f"Trop de connexions depuis {ip} ({count} > {self.thresholds['connection_rate']})"
                })
        
        return issues
    
    def detect_port_scan(self, current_devices):
        """
        Détecte un scan de ports agressif.
        Critères : un appareil contactant trop de ports en peu de temps.
        """
        issues = []
        
        history = self._load_history()
        
        # Pour chaque appareil, compter les ports touchés récemment
        for device_id, entries in history.items():
            if isinstance(entries, list) and len(entries) > 0:
                recent_entries = entries[-self.thresholds["port_scans"]:]
                
                ports_touched = set()
                for entry in recent_entries:
                    # Extraire info ports si disponible
                    ports = entry.get("open_ports", [])
                    if ports:
                        ports_touched.update(ports)
                
                if len(ports_touched) > self.thresholds["port_scans"]:
                    device = current_devices[0] if current_devices else {}
                    issues.append({
                        "type": "AGGRESSIVE_PORT_SCAN",
                        "device_id": device_id,
                        "ports_scanned": len(ports_touched),
                        "threshold": self.thresholds["port_scans"],
                        "risk": "🟠 MOYEN",
                        "description": f"Scan de ports agressif détecté ({len(ports_touched)} ports)"
                    })
        
        return issues
    
    def detect_new_devices_flood(self):
        """
        Détecte un afflux anormal de nouveaux appareils.
        Critères : trop de NEW_DEVICE alerts en peu de temps.
        """
        issues = []
        alerts = self._load_alerts()
        
        # Compter les alertes NEW_DEVICE de la dernière heure
        new_device_alerts = []
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        
        for alert in alerts:
            if "NEW_DEVICE" in alert.get("alert_type", ""):
                try:
                    alert_time = datetime.fromisoformat(alert.get("timestamp", ""))
                    if alert_time > one_hour_ago:
                        new_device_alerts.append(alert)
                except:
                    pass
        
        if len(new_device_alerts) > self.thresholds["new_devices_per_hour"]:
            issues.append({
                "type": "DEVICE_FLOOD",
                "count": len(new_device_alerts),
                "threshold": self.thresholds["new_devices_per_hour"],
                "risk": "🟠 MOYEN",
                "description": f"Afflux anormal de nouveaux appareils ({len(new_device_alerts)} > {self.thresholds['new_devices_per_hour']} en 1h)"
            })
        
        return issues
    
    def detect_mac_spoofing_attempt(self, current_devices):
        """
        Détecte une tentative de MAC spoofing.
        Critères : une MAC changeant rapidement plusieurs fois.
        """
        issues = []
        history = self._load_history()
        
        mac_changes = defaultdict(int)
        
        for device_id, entries in history.items():
            if isinstance(entries, list) and len(entries) > 1:
                # Vérifier si les MACs changent
                macs_seen = set()
                for entry in entries[-10:]:  # Dernières 10 entrées
                    mac = entry.get("mac")
                    if mac:
                        macs_seen.add(mac)
                
                if len(macs_seen) >= self.thresholds["mac_changes_per_device"]:
                    issues.append({
                        "type": "MAC_SPOOFING_ATTEMPT",
                        "device_id": device_id,
                        "macs_count": len(macs_seen),
                        "threshold": self.thresholds["mac_changes_per_device"],
                        "risk": "🔴 CRITIQUE",
                        "description": f"Tentative possible de MAC spoofing ({len(macs_seen)} MACs différentes)"
                    })
        
        return issues
    
    def detect_suspicious_services(self, current_devices):
        """
        Détecte des services suspects ouverts.
        Critères : ports dangereux (Telnet, FTP non chiffré, etc.)
        """
        issues = []
        
        dangerous_ports = {
            23: ("Telnet", "🔴 CRITIQUE - Non chiffré!"),
            21: ("FTP", "🔴 CRITIQUE - Non chiffré!"),
            69: ("TFTP", "🟠 MOYEN - Pas d'authentification"),
            111: ("RPC", "🟠 MOYEN - Peut exposer services"),
            135: ("RPC (Windows)", "🟠 MOYEN - Exploitation possible"),
        }
        
        for device in current_devices:
            ports = device.get("open_ports", [])
            if ports:
                for port in ports:
                    if port in dangerous_ports:
                        service, risk = dangerous_ports[port]
                        issues.append({
                            "type": "DANGEROUS_SERVICE",
                            "ip": device.get("ip"),
                            "mac": device.get("mac"),
                            "port": port,
                            "service": service,
                            "risk": risk,
                            "description": f"{service} ouvert sur port {port}"
                        })
        
        return issues
    
    def generate_ids_report(self, current_devices):
        """Génère un rapport IDS complet."""
        
        print("\n" + "="*100)
        print("🚨 SYSTÈME DE DÉTECTION D'INTRUSION (IDS) - OUTILS 101")
        print("="*100)
        print(f"Généré : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        all_issues = []
        
        # Détection DDoS
        print("1️⃣ Vérification attaques DDoS...")
        ddos_issues = self.detect_ddos_attempt(current_devices)
        all_issues.extend(ddos_issues)
        if ddos_issues:
            for issue in ddos_issues:
                print(f"   {issue['risk']} {issue['description']}")
        else:
            print("   ✅ Aucune attaque DDoS détectée")
        
        # Détection scans de ports
        print("\n2️⃣ Vérification scans de ports agressifs...")
        port_scan_issues = self.detect_port_scan(current_devices)
        all_issues.extend(port_scan_issues)
        if port_scan_issues:
            for issue in port_scan_issues:
                print(f"   {issue['risk']} {issue['description']}")
        else:
            print("   ✅ Aucun scan de port agressif détecté")
        
        # Détection afflux d'appareils
        print("\n3️⃣ Vérification afflux de nouveaux appareils...")
        device_flood_issues = self.detect_new_devices_flood()
        all_issues.extend(device_flood_issues)
        if device_flood_issues:
            for issue in device_flood_issues:
                print(f"   {issue['risk']} {issue['description']}")
        else:
            print("   ✅ Afflux normal d'appareils")
        
        # Détection MAC spoofing
        print("\n4️⃣ Vérification tentatives MAC spoofing...")
        spoofing_issues = self.detect_mac_spoofing_attempt(current_devices)
        all_issues.extend(spoofing_issues)
        if spoofing_issues:
            for issue in spoofing_issues:
                print(f"   {issue['risk']} {issue['description']}")
        else:
            print("   ✅ Aucune tentative de spoofing détectée")
        
        # Détection services dangereux
        print("\n5️⃣ Vérification services dangereux ouverts...")
        service_issues = self.detect_suspicious_services(current_devices)
        all_issues.extend(service_issues)
        if service_issues:
            for issue in service_issues:
                print(f"   {issue['risk']} {issue['description']}")
        else:
            print("   ✅ Aucun service dangereux détecté")
        
        # Résumé
        print("\n" + "="*100)
        print(f"📊 RÉSUMÉ : {len(all_issues)} menace(s) détectée(s)")
        print("="*100)
        
        if all_issues:
            critiques = len([i for i in all_issues if "CRITIQUE" in i.get("risk", "")])
            moyennes = len([i for i in all_issues if "MOYEN" in i.get("risk", "")])
            
            print(f"\n  🔴 Critiques: {critiques}")
            print(f"  🟠 Moyennes: {moyennes}")
            print("\n⚠️ Veuillez vérifier les menaces détectées ci-dessus.")
        else:
            print("\n✅ Aucune menace détectée. Votre réseau semble sécurisé.")
        
        return all_issues
