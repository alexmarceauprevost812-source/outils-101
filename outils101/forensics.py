#!/usr/bin/env python3
"""
Network Forensics - Analyse les logs pour détecter les attaques passées
Reconstruit les incidents de sécurité à partir des logs système
"""

import json
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


class NetworkForensics:
    """Analyse forensique des logs réseau"""
    
    def __init__(self):
        self.findings = []
        self.log_sources = {
            "auth": "/var/log/auth.log",
            "syslog": "/var/log/syslog",
            "apache": "/var/log/apache2/access.log",
            "nginx": "/var/log/nginx/access.log",
            "firewall": "/var/log/ufw.log"
        }
        self.forensics_report = Path("logs/forensics_report.json")
        self.forensics_report.parent.mkdir(parents=True, exist_ok=True)
    
    def parse_auth_log(self):
        """Analyse le log d'authentification"""
        findings = {
            "failed_logins": [],
            "successful_logins": [],
            "sudo_commands": [],
            "suspicious_activity": []
        }
        
        try:
            with open(self.log_sources["auth"]) as f:
                for line in f:
                    # Failed login attempts
                    if "Failed password" in line or "Invalid user" in line:
                        findings["failed_logins"].append({
                            "type": "FAILED_LOGIN",
                            "line": line.strip(),
                            "timestamp": self._extract_timestamp(line),
                            "severity": "MEDIUM"
                        })
                    
                    # Sudo commands
                    if "sudo:" in line and "COMMAND=" in line:
                        findings["sudo_commands"].append({
                            "type": "SUDO_COMMAND",
                            "line": line.strip(),
                            "timestamp": self._extract_timestamp(line),
                            "severity": "HIGH"
                        })
                    
                    # Suspicious patterns
                    if any(x in line for x in ["break-in attempt", "hacking", "exploit"]):
                        findings["suspicious_activity"].append({
                            "type": "SUSPICIOUS_PATTERN",
                            "line": line.strip(),
                            "timestamp": self._extract_timestamp(line),
                            "severity": "HIGH"
                        })
        except FileNotFoundError:
            print(f"   ⚠️  {self.log_sources['auth']} non accessible (besoin root)")
        
        return findings
    
    def parse_apache_log(self):
        """Analyse les logs Apache"""
        findings = {
            "sql_injection_attempts": [],
            "xss_attempts": [],
            "path_traversal": [],
            "unusual_requests": []
        }
        
        try:
            with open(self.log_sources["apache"]) as f:
                for line in f:
                    # SQL Injection patterns
                    if any(x in line.lower() for x in ["union select", "drop table", "insert into", "exec(", "script>"]):
                        attack_type = "SQL_INJECTION" if "union" in line or "drop" in line else "XSS"
                        findings["sql_injection_attempts"].append({
                            "type": attack_type,
                            "line": line.strip()[:200],
                            "timestamp": self._extract_timestamp(line),
                            "severity": "CRITICAL"
                        })
                    
                    # Path traversal
                    if any(x in line for x in ["../", "..\\", "%2e%2e"]):
                        findings["path_traversal"].append({
                            "type": "PATH_TRAVERSAL",
                            "line": line.strip()[:200],
                            "timestamp": self._extract_timestamp(line),
                            "severity": "HIGH"
                        })
        except FileNotFoundError:
            print(f"   ⚠️  {self.log_sources['apache']} non accessible")
        
        return findings
    
    def detect_brute_force(self):
        """Détecte les attaques par brute-force"""
        brute_forces = defaultdict(list)
        
        try:
            with open(self.log_sources["auth"]) as f:
                lines = f.readlines()
                
            for line in lines:
                if "Failed password" in line:
                    # Extrait l'IP (simplifié)
                    ip_match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line)
                    if ip_match:
                        ip = ip_match.group(1)
                        brute_forces[ip].append(self._extract_timestamp(line))
        except FileNotFoundError:
            pass
        
        # Identifie les attaques (>5 tentatives en 5 min)
        attacks = []
        for ip, timestamps in brute_forces.items():
            if len(timestamps) > 5:
                attacks.append({
                    "type": "BRUTE_FORCE_ATTACK",
                    "source_ip": ip,
                    "attempt_count": len(timestamps),
                    "severity": "CRITICAL" if len(timestamps) > 20 else "HIGH"
                })
        
        return attacks
    
    def detect_privilege_escalation(self):
        """Détecte les tentatives d'escalade de privilèges"""
        escalations = []
        
        try:
            with open(self.log_sources["auth"]) as f:
                for line in f:
                    if "sudo" in line and "COMMAND=" in line:
                        if any(x in line for x in ["/bin/bash", "/bin/sh", "chmod 777", "chown"]):
                            escalations.append({
                                "type": "PRIVILEGE_ESCALATION",
                                "line": line.strip(),
                                "timestamp": self._extract_timestamp(line),
                                "severity": "CRITICAL"
                            })
        except FileNotFoundError:
            pass
        
        return escalations
    
    def detect_data_exfiltration(self):
        """Détecte les signes d'exfiltration de données"""
        exfils = []
        
        try:
            with open(self.log_sources["apache"]) as f:
                for line in f:
                    # Téléchargements massifs (HTTP 206 = Range)
                    if "206" in line or "HTTP/1.1\" 206" in line:
                        exfils.append({
                            "type": "POTENTIAL_DATA_EXFILTRATION",
                            "line": line.strip()[:200],
                            "timestamp": self._extract_timestamp(line),
                            "severity": "MEDIUM"
                        })
        except FileNotFoundError:
            pass
        
        return exfils
    
    def _extract_timestamp(self, line):
        """Extrait le timestamp d'une ligne de log"""
        # Formats courants: "Jan 15 10:30:45" ou "[15/Jan/2024:10:30:45"
        patterns = [
            r'\[(\d+/\w+/\d+:\d+:\d+:\d+)',
            r'(\w+ \d+ \d+:\d+:\d+)',
            r'(\d+-\d+-\d+ \d+:\d+:\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(1)
        return "Unknown"
    
    def generate_forensics_report(self):
        """Génère un rapport forensique complet"""
        print("\n📋 Analyse forensique en cours...\n")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {},
            "findings": {},
            "threats": [],
            "recommendations": []
        }
        
        # Analyse auth.log
        print("   🔍 Analyse auth.log...")
        auth_findings = self.parse_auth_log()
        report["findings"]["auth_log"] = auth_findings
        
        # Analyse Apache
        print("   🔍 Analyse Apache logs...")
        apache_findings = self.parse_apache_log()
        report["findings"]["apache_log"] = apache_findings
        
        # Détecte brute-force
        print("   🔍 Recherche d'attaques brute-force...")
        brute_force = self.detect_brute_force()
        report["threats"].extend(brute_force)
        
        # Détecte escalade de privilèges
        print("   🔍 Recherche d'escalade de privilèges...")
        escalations = self.detect_privilege_escalation()
        report["threats"].extend(escalations)
        
        # Détecte exfiltration
        print("   🔍 Recherche de signes d'exfiltration...")
        exfils = self.detect_data_exfiltration()
        report["threats"].extend(exfils)
        
        # Résumé
        total_threats = len(report["threats"])
        critical = len([t for t in report["threats"] if t.get("severity") == "CRITICAL"])
        high = len([t for t in report["threats"] if t.get("severity") == "HIGH"])
        
        report["summary"] = {
            "total_threats": total_threats,
            "critical": critical,
            "high": high,
            "medium": total_threats - critical - high
        }
        
        # Recommandations
        if critical > 0:
            report["recommendations"].append("🔴 CRITIQUE: Enquête immédiate requise!")
        if brute_force:
            report["recommendations"].append("Activer fail2ban pour les attaques brute-force")
        if escalations:
            report["recommendations"].append("Vérifier les logs sudo - activité anormale détectée")
        if exfils:
            report["recommendations"].append("Monitorer les débits réseau - possibilité d'exfiltration")
        
        # Sauvegarde
        with open(self.forensics_report, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def display_report(self, report):
        """Affiche le rapport de façon lisible"""
        print("\n" + "="*70)
        print("🔬 RAPPORT FORENSIQUE RÉSEAU")
        print("="*70)
        
        summary = report.get("summary", {})
        print(f"\n📊 RÉSUMÉ:")
        print(f"   Total menaces détectées: {summary.get('total_threats', 0)}")
        print(f"   🔴 Critique: {summary.get('critical', 0)}")
        print(f"   🟠 Haute: {summary.get('high', 0)}")
        print(f"   🟡 Moyenne: {summary.get('medium', 0)}")
        
        print(f"\n🚨 MENACES DÉTECTÉES:")
        threats = report.get("threats", [])
        if not threats:
            print("   ✅ Aucune menace majeure détectée")
        else:
            for i, threat in enumerate(threats[:10], 1):
                severity_emoji = "🔴" if threat.get("severity") == "CRITICAL" else "🟠" if threat.get("severity") == "HIGH" else "🟡"
                print(f"\n   {i}. {severity_emoji} {threat.get('type', 'Unknown')}")
                print(f"      Source: {threat.get('source_ip', 'N/A')}")
                print(f"      Détails: {threat.get('line', 'N/A')[:80]}...")
        
        print(f"\n💡 RECOMMANDATIONS:")
        for rec in report.get("recommendations", []):
            print(f"   • {rec}")
        
        print(f"\n📁 Rapport complet sauvegardé: {self.forensics_report}")


def run_forensics():
    """Fonction principale"""
    forensics = NetworkForensics()
    
    print("\n" + "="*60)
    print("🔬 NETWORK FORENSICS - Analyse des Incidents")
    print("="*60)
    
    report = forensics.generate_forensics_report()
    forensics.display_report(report)


if __name__ == "__main__":
    run_forensics()
