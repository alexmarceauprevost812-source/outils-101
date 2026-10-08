"""
Détecteur de MAC spoofing.
Identifie si une adresse MAC change subitement (usurpation d'identité d'appareil).
"""

import json
from pathlib import Path
from datetime import datetime


class MACSpoofer:
    def __init__(self, history_file="logs/devices_history.json"):
        self.history_file = Path(history_file)
        self.history = self._load_history()
    
    def _load_history(self):
        """Charge l'historique des appareils."""
        if self.history_file.exists():
            try:
                with open(self.history_file, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def check_ip_mac_consistency(self, devices):
        """
        Vérifie si une IP a plusieurs MACs différentes.
        Potentiellement une usurpation d'identité.
        """
        ip_to_macs = {}
        suspicious = []
        
        # Analyser l'historique
        for device_id, entries in self.history.items():
            if isinstance(entries, list):
                for entry in entries:
                    ip = entry.get("ip")
                    mac = entry.get("mac")
                    
                    if ip and mac:
                        if ip not in ip_to_macs:
                            ip_to_macs[ip] = set()
                        ip_to_macs[ip].add(mac)
        
        # Déterminer les IPs suspectes
        for ip, macs in ip_to_macs.items():
            if len(macs) > 1:
                suspicious.append({
                    "ip": ip,
                    "macs": list(macs),
                    "risk": "🔴 CRITIQUE" if len(macs) > 2 else "🟠 MOYEN"
                })
        
        return suspicious
    
    def check_mac_ip_change(self, current_devices):
        """
        Vérifie si une MAC a changé d'IP rapidement.
        Peut indiquer une usurpation d'identité.
        """
        changes = []
        mac_to_ips = {}
        
        # Charger les mappings MAC→IP de l'historique
        for device_id, entries in self.history.items():
            if isinstance(entries, list):
                for entry in entries:
                    mac = entry.get("mac")
                    ip = entry.get("ip")
                    
                    if mac and ip:
                        if mac not in mac_to_ips:
                            mac_to_ips[mac] = []
                        mac_to_ips[mac].append(ip)
        
        # Vérifier les changements actuels
        for device in current_devices:
            mac = device.get("mac")
            ip = device.get("ip")
            
            if mac and ip and mac in mac_to_ips:
                previous_ips = set(mac_to_ips[mac])
                if ip not in previous_ips and len(previous_ips) >= 2:
                    changes.append({
                        "mac": mac,
                        "new_ip": ip,
                        "previous_ips": list(previous_ips),
                        "name": device.get("name", "Inconnu"),
                        "risk": "🔴 CRITIQUE"
                    })
        
        return changes
    
    def check_vendor_mismatch(self, devices):
        """
        Vérifie si le fabricant (OUI) d'une MAC change.
        Peut indiquer un changement d'appareil ou usurpation.
        """
        from outils101.vendor import get_vendor
        
        mismatches = []
        mac_vendors = {}
        
        # Charger les vendeurs de l'historique
        for device_id, entries in self.history.items():
            if isinstance(entries, list):
                for entry in entries:
                    mac = entry.get("mac")
                    if mac:
                        if mac not in mac_vendors:
                            mac_vendors[mac] = set()
                        vendor = entry.get("vendor", "Inconnu")
                        mac_vendors[mac].add(vendor)
        
        # Vérifier les changements actuels
        for device in devices:
            mac = device.get("mac")
            current_vendor = get_vendor(mac)
            
            if mac and mac in mac_vendors:
                previous_vendors = mac_vendors[mac]
                if current_vendor not in previous_vendors and len(previous_vendors) > 0:
                    mismatches.append({
                        "mac": mac,
                        "current_vendor": current_vendor,
                        "previous_vendors": list(previous_vendors),
                        "name": device.get("name", "Inconnu"),
                        "risk": "🟠 MOYEN - Possible usurpation"
                    })
        
        return mismatches
    
    def generate_report(self, devices):
        """Génère un rapport complet de détection d'usurpation."""
        
        print("\n" + "="*80)
        print("🚨 RAPPORT DÉTECTION MAC SPOOFING")
        print("="*80)
        print(f"Généré : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Check 1 : IP → MAC
        print("1️⃣ Vérification : Plusieurs MACs pour une même IP")
        print("-" * 80)
        ip_mac_issues = self.check_ip_mac_consistency(devices)
        
        if ip_mac_issues:
            for issue in ip_mac_issues:
                print(f"\n{issue['risk']} IP {issue['ip']}")
                for mac in issue['macs']:
                    print(f"   └─ MAC: {mac}")
        else:
            print("✅ Aucun problème détecté")
        
        # Check 2 : MAC → IP
        print("\n\n2️⃣ Vérification : Changements d'IP pour une même MAC")
        print("-" * 80)
        mac_ip_changes = self.check_mac_ip_change(devices)
        
        if mac_ip_changes:
            for change in mac_ip_changes:
                print(f"\n{change['risk']} Appareil: {change['name']}")
                print(f"   MAC: {change['mac']}")
                print(f"   Nouvelle IP: {change['new_ip']}")
                print(f"   IPs précédentes: {change['previous_ips']}")
        else:
            print("✅ Aucun changement d'IP suspect")
        
        # Check 3 : Vendor mismatch
        print("\n\n3️⃣ Vérification : Changement de fabricant (OUI)")
        print("-" * 80)
        vendor_mismatches = self.check_vendor_mismatch(devices)
        
        if vendor_mismatches:
            for mismatch in vendor_mismatches:
                print(f"\n{mismatch['risk']} Appareil: {mismatch['name']}")
                print(f"   MAC: {mismatch['mac']}")
                print(f"   Fabricant actuel: {mismatch['current_vendor']}")
                print(f"   Fabricants précédents: {mismatch['previous_vendors']}")
        else:
            print("✅ Aucune usurpation d'identité détectée")
        
        # Résumé
        total_issues = len(ip_mac_issues) + len(mac_ip_changes) + len(vendor_mismatches)
        print("\n" + "="*80)
        print(f"📊 RÉSUMÉ : {total_issues} problème(s) détecté(s)")
        print("="*80)
        
        return {
            "ip_mac_issues": ip_mac_issues,
            "mac_ip_changes": mac_ip_changes,
            "vendor_mismatches": vendor_mismatches,
            "total_issues": total_issues
        }
