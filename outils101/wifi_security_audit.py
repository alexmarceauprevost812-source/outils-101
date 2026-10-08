"""
Audit avancé de sécurité WiFi.
Détecte WPS, open broadcast, vieux protocoles, etc.
"""

import subprocess
import re
from datetime import datetime


class WiFiSecurityAudit:
    
    SECURITY_LEVELS = {
        "Open": {"score": 0, "emoji": "🔓", "risk": "CRITIQUE"},
        "WEP": {"score": 1, "emoji": "🔴", "risk": "CRITIQUE"},
        "WPA": {"score": 5, "emoji": "🟠", "risk": "MOYEN"},
        "WPA2": {"score": 8, "emoji": "🟡", "risk": "FAIBLE"},
        "WPA3": {"score": 10, "emoji": "🟢", "risk": "SÉCURISÉ"},
    }
    
    def scan_networks(self):
        """Scanne les réseaux WiFi visibles."""
        networks = []
        
        try:
            # Linux avec nmcli
            result = subprocess.run(
                ["sudo", "nmcli", "device", "wifi", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            lines = result.stdout.split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 7:
                        networks.append({
                            "ssid": " ".join(parts[:-6]),
                            "bssid": parts[-6],
                            "mode": parts[-5],
                            "chan": parts[-4],
                            "rate": parts[-3],
                            "signal": parts[-2],
                            "security": parts[-1]
                        })
        except Exception as e:
            print(f"⚠️ Erreur scan WiFi: {e}")
        
        return networks
    
    def analyze_security(self, security_string):
        """Analyse le type de sécurité d'un réseau."""
        
        security_string = security_string.lower()
        
        security_info = {
            "wpa3": False,
            "wpa2": False,
            "wpa": False,
            "wep": False,
            "open": False,
            "wps": False,
            "pmf": False,
            "tkip": False,
            "ccmp": False,
        }
        
        if "wpa3" in security_string:
            security_info["wpa3"] = True
        if "wpa2" in security_string or "rsn" in security_string:
            security_info["wpa2"] = True
        if "wpa" in security_string:
            security_info["wpa"] = True
        if "wep" in security_string:
            security_info["wep"] = True
        if "open" in security_string or security_string == "":
            security_info["open"] = True
        if "wps" in security_string:
            security_info["wps"] = True
        if "pmf" in security_string:
            security_info["pmf"] = True
        if "tkip" in security_string:
            security_info["tkip"] = True
        if "ccmp" in security_string:
            security_info["ccmp"] = True
        
        return security_info
    
    def get_security_level(self, security_string):
        """Détermine le niveau de sécurité (0-10)."""
        
        analysis = self.analyze_security(security_string)
        
        if analysis["open"]:
            return "Open", 0, "🔓 CRITIQUE"
        elif analysis["wep"]:
            return "WEP", 1, "🔴 CRITIQUE (cassable en minutes)"
        elif analysis["wpa"] and not analysis["wpa2"]:
            return "WPA", 5, "🟠 MOYEN (WPA1 est obsolète)"
        elif analysis["wpa2"] and not analysis["wpa3"]:
            if analysis["tkip"]:
                return "WPA2 (TKIP)", 6, "🟠 MOYEN (TKIP faible)"
            return "WPA2", 8, "🟡 BON (sauf si vieux pwd)"
        elif analysis["wpa3"]:
            return "WPA3", 10, "🟢 EXCELLENT"
        else:
            return "Unknown", 5, "❓ INCONNU"
    
    def check_wps_vulnerability(self, network):
        """Vérifie si WPS est activé (vulnérable)."""
        
        security = network.get("security", "").lower()
        
        if "wps" in security:
            return {
                "vulnerable": True,
                "risk": "🔴 CRITIQUE",
                "description": "WPS activé - Cassable en heures avec Reaver/Bully",
                "fix": "Désactiver WPS dans les paramètres du routeur"
            }
        
        return {
            "vulnerable": False,
            "risk": "✅ OK",
            "description": "WPS désactivé",
            "fix": None
        }
    
    def check_broadcast_ssid(self, network):
        """Vérifie si le SSID est visible (broadcast)."""
        
        ssid = network.get("ssid", "").strip()
        
        if ssid == "":
            return {
                "hidden": True,
                "risk": "🟡 MOYEN",
                "description": "SSID caché - Fausse sécurité (facilement trouvable)",
                "note": "Ralentit seulement les scans automatiques"
            }
        
        return {
            "hidden": False,
            "risk": "ℹ️ INFO",
            "description": "SSID visible (normal)",
            "note": None
        }
    
    def generate_report(self):
        """Génère un rapport complet d'audit WiFi."""
        
        print("\n" + "="*100)
        print("🛡️ AUDIT SÉCURITÉ WiFi - OUTILS 101")
        print("="*100)
        print(f"Généré : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        networks = self.scan_networks()
        
        if not networks:
            print("❌ Aucun réseau WiFi détecté. Assurez-vous que WiFi est activé.")
            return
        
        print(f"📡 Réseaux détectés : {len(networks)}\n")
        
        vulnerabilities = []
        
        for i, network in enumerate(networks, 1):
            ssid = network.get("ssid", "Unknown")
            bssid = network.get("bssid", "N/A")
            signal = network.get("signal", "N/A")
            security = network.get("security", "Unknown")
            
            sec_type, sec_score, sec_risk = self.get_security_level(security)
            wps_check = self.check_wps_vulnerability(network)
            broadcast_check = self.check_broadcast_ssid(network)
            
            print(f"[{i}] {sec_type.split()[0]:8} | {ssid:25} | {signal:>6} | {sec_risk}")
            print(f"    └─ BSSID: {bssid}")
            print(f"    └─ Protocole: {sec_type} (Score: {sec_score}/10)")
            print(f"    └─ Sécurité complète: {security}")
            
            # WPS Check
            if wps_check["vulnerable"]:
                print(f"    └─ {wps_check['risk']} WPS: {wps_check['description']}")
                vulnerabilities.append({
                    "ssid": ssid,
                    "type": "WPS_ENABLED",
                    "risk": "CRITIQUE"
                })
            
            # Broadcast Check
            if broadcast_check["hidden"]:
                print(f"    └─ {broadcast_check['risk']} SSID: {broadcast_check['description']}")
            
            # Analyse détaillée
            analysis = self.analyze_security(security)
            if analysis["tkip"]:
                print(f"    └─ 🟠 ALERTE: TKIP détecté (chiffrement faible)")
                vulnerabilities.append({
                    "ssid": ssid,
                    "type": "TKIP_ENCRYPTION",
                    "risk": "MOYEN"
                })
            
            if analysis["wpa"] and not analysis["wpa2"]:
                print(f"    └─ 🟠 ALERTE: WPA1 détecté (obsolète, préférer WPA2/WPA3)")
                vulnerabilities.append({
                    "ssid": ssid,
                    "type": "OLD_WPA",
                    "risk": "MOYEN"
                })
            
            print()
        
        # Résumé des vulnérabilités
        print("="*100)
        print("📊 RÉSUMÉ DES VULNÉRABILITÉS")
        print("="*100)
        
        if vulnerabilities:
            print(f"\n🔴 {len(vulnerabilities)} vulnérabilité(s) trouvée(s):\n")
            for vuln in vulnerabilities:
                print(f"  {vuln['risk']:8} | {vuln['type']:20} | {vuln['ssid']}")
        else:
            print("\n✅ Aucune vulnérabilité critique détectée.")
        
        # Recommandations
        print("\n" + "="*100)
        print("💡 RECOMMANDATIONS DE SÉCURITÉ")
        print("="*100)
        print("""
1. ✅ Utiliser WPA3 si disponible, sinon WPA2 minimum
2. ✅ Utiliser CCMP (AES) comme chiffrement, éviter TKIP
3. ✅ Désactiver WPS (très vulnérable)
4. ✅ Mot de passe fort (20+ caractères, mélange complexe)
5. ✅ Masquer SSID est une fausse sécurité, pas prioritaire
6. ✅ Mettre à jour le firmware du routeur régulièrement
7. ✅ Isoler les appareils IoT sur un réseau invité
8. ✅ Vérifier les appareils connectés régulièrement
        """)
        
        print("="*100)
