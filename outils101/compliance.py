#!/usr/bin/env python3
"""
Compliance Checker - Vérifie la conformité de sécurité du système
Teste la config réseau contre les bonnes pratiques de sécurité
"""

import socket
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime


class ComplianceChecker:
    """Teste la conformité de sécurité"""
    
    def __init__(self):
        self.checks = []
        self.score = 0
        self.max_score = 0
        self.compliance_report = Path("logs/compliance_report.json")
        self.compliance_report.parent.mkdir(parents=True, exist_ok=True)
    
    def run_all_checks(self):
        """Lance tous les contrôles de conformité"""
        print("\n" + "="*70)
        print("✅ VÉRIFICATION DE CONFORMITÉ SÉCURITÉ")
        print("="*70 + "\n")
        
        print("   🔍 Vérification des services en écoute...")
        self.check_open_ports()
        
        print("   🔍 Vérification des protocoles sécurisés...")
        self.check_secure_protocols()
        
        print("   🔍 Vérification du firewall...")
        self.check_firewall()
        
        print("   🔍 Vérification des mots de passe (local)...")
        self.check_password_policy()
        
        print("   🔍 Vérification SSH...")
        self.check_ssh_hardening()
        
        print("   🔍 Vérification des services inutiles...")
        self.check_unnecessary_services()
        
        print("   🔍 Vérification des permissions de fichiers...")
        self.check_file_permissions()
        
        print("   🔍 Vérification des mises à jour...")
        self.check_updates()
        
        print("   🔍 Vérification de l'encryption WiFi...")
        self.check_wifi_encryption()
        
        return self.generate_report()
    
    def add_check(self, name, status, severity, details):
        """Ajoute un résultat de contrôle"""
        self.max_score += 10
        
        if status == "PASS":
            self.score += 10
            emoji = "✅"
            color_status = f"{emoji} CONFORME"
        elif status == "WARNING":
            self.score += 5
            emoji = "⚠️"
            color_status = f"{emoji} ATTENTION"
        else:
            emoji = "❌"
            color_status = f"{emoji} NON-CONFORME"
        
        self.checks.append({
            "name": name,
            "status": status,
            "severity": severity,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "status": status,
            "emoji": emoji,
            "display": color_status
        }
    
    def check_open_ports(self):
        """Vérifie les ports ouverts"""
        dangerous_ports = {
            21: "FTP (non chiffré)",
            23: "Telnet (non chiffré)",
            25: "SMTP sans TLS",
            69: "TFTP (non sécurisé)",
            3306: "MySQL exposé",
            5432: "PostgreSQL exposé",
            6379: "Redis exposé"
        }
        
        open_ports = []
        for port in dangerous_ports.keys():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                open_ports.append((port, dangerous_ports[port]))
        
        if open_ports:
            details = f"Ports dangereux ouverts: {', '.join([f'{p}({d})' for p, d in open_ports])}"
            self.add_check("Ports ouverts", "FAIL", "HIGH", details)
        else:
            self.add_check("Ports ouverts", "PASS", "INFO", "Aucun port dangereux détecté")
    
    def check_secure_protocols(self):
        """Vérifie l'utilisation de protocoles sécurisés"""
        checks = {
            "SSH": (22, "SSH sécurisé"),
            "HTTPS": (443, "HTTPS sécurisé"),
        }
        
        insecure = []
        for name, (port, desc) in checks.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                self.add_check(f"Protocole {name}", "PASS", "INFO", f"{desc} actif")
            else:
                insecure.append(name)
        
        if insecure:
            self.add_check("Protocoles sécurisés", "WARNING", "MEDIUM", f"{', '.join(insecure)} non détectés")
    
    def check_firewall(self):
        """Vérifie l'état du firewall"""
        try:
            result = subprocess.run(['sudo', 'ufw', 'status'], 
                                  capture_output=True, text=True, timeout=5)
            
            if "active" in result.stdout.lower():
                self.add_check("Firewall UFW", "PASS", "INFO", "Firewall activé et actif")
            else:
                self.add_check("Firewall UFW", "FAIL", "HIGH", "Firewall désactivé - activation recommandée")
        except:
            self.add_check("Firewall UFW", "WARNING", "MEDIUM", "UFW non disponible ou pas d'accès root")
    
    def check_password_policy(self):
        """Vérifie la politique de mots de passe"""
        try:
            with open('/etc/pam.d/common-password') as f:
                content = f.read()
            
            checks_passed = 0
            total_checks = 4
            
            if 'minlen=12' in content or 'minlen=14' in content:
                checks_passed += 1
            if 'dcredit' in content:
                checks_passed += 1
            if 'ucredit' in content:
                checks_passed += 1
            if 'ocredit' in content:
                checks_passed += 1
            
            if checks_passed >= 3:
                self.add_check("Politique mots de passe", "PASS", "INFO", "Politique forte détectée")
            else:
                self.add_check("Politique mots de passe", "WARNING", "MEDIUM", f"Seulement {checks_passed}/{total_checks} critères")
        except:
            self.add_check("Politique mots de passe", "WARNING", "MEDIUM", "Impossible de vérifier - besoin root")
    
    def check_ssh_hardening(self):
        """Vérifie le durcissement SSH"""
        try:
            with open('/etc/ssh/sshd_config') as f:
                content = f.read()
            
            hardening_checks = {
                'PermitRootLogin no': 'Connexion root désactivée',
                'PubkeyAuthentication yes': 'Auth par clé publique',
                'PasswordAuthentication no': 'Auth par mot de passe désactivée'
            }
            
            passed = sum(1 for check in hardening_checks if check in content)
            total = len(hardening_checks)
            
            if passed >= 2:
                status = "PASS"
                details = f"SSH bien durci ({passed}/{total} recommandations)"
            elif passed >= 1:
                status = "WARNING"
                details = f"SSH partiellement durci ({passed}/{total})"
            else:
                status = "FAIL"
                details = f"SSH non durci ({passed}/{total})"
            
            self.add_check("Durcissement SSH", status, "HIGH", details)
        except:
            self.add_check("Durcissement SSH", "WARNING", "HIGH", "Impossible de vérifier - besoin root")
    
    def check_unnecessary_services(self):
        """Vérifie les services inutiles"""
        dangerous_services = [
            'telnet', 'vsftpd', 'snmpd', 'rsync', 'nfs-server'
        ]
        
        running_dangerous = []
        try:
            result = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=running'],
                                  capture_output=True, text=True, timeout=5)
            
            for service in dangerous_services:
                if service in result.stdout:
                    running_dangerous.append(service)
        except:
            pass
        
        if running_dangerous:
            details = f"Services dangereux actifs: {', '.join(running_dangerous)}"
            self.add_check("Services inutiles", "FAIL", "HIGH", details)
        else:
            self.add_check("Services inutiles", "PASS", "INFO", "Aucun service dangereux détecté")
    
    def check_file_permissions(self):
        """Vérifie les permissions de fichiers critiques"""
        critical_files = {
            '/etc/passwd': '644',
            '/etc/shadow': '640',
            '/etc/ssh/sshd_config': '600'
        }
        
        issues = []
        for filepath, expected_perm in critical_files.items():
            try:
                stat_info = subprocess.run(['stat', '-c', '%a', filepath],
                                         capture_output=True, text=True, timeout=2)
                actual_perm = stat_info.stdout.strip()
                
                if actual_perm != expected_perm:
                    issues.append(f"{filepath} ({actual_perm} au lieu de {expected_perm})")
            except:
                pass
        
        if issues:
            details = f"Permissions incorrectes: {', '.join(issues)}"
            self.add_check("Permissions fichiers", "WARNING", "MEDIUM", details)
        else:
            self.add_check("Permissions fichiers", "PASS", "INFO", "Permissions correctes")
    
    def check_updates(self):
        """Vérifie si des mises à jour sont disponibles"""
        try:
            result = subprocess.run(['apt', 'list', '--upgradable'],
                                  capture_output=True, text=True, timeout=5)
            
            updates = len([l for l in result.stdout.split('\n') if 'upgradable' in l])
            
            if updates == 0:
                self.add_check("Mises à jour", "PASS", "INFO", "Système à jour")
            elif updates < 5:
                self.add_check("Mises à jour", "WARNING", "MEDIUM", f"{updates} mises à jour disponibles")
            else:
                self.add_check("Mises à jour", "FAIL", "HIGH", f"{updates} mises à jour critiques disponibles")
        except:
            self.add_check("Mises à jour", "WARNING", "MEDIUM", "Impossible de vérifier")
    
    def check_wifi_encryption(self):
        """Vérifie le chiffrement WiFi"""
        try:
            result = subprocess.run(['nmcli', 'dev', 'wifi', 'list'],
                                  capture_output=True, text=True, timeout=5)
            
            open_networks = result.stdout.count("--")
            
            if open_networks == 0:
                self.add_check("WiFi chiffré", "PASS", "INFO", "Tous les réseaux WiFi sont chiffrés")
            else:
                details = f"{open_networks} réseau(x) WiFi non chiffré(s) détecté(s)"
                self.add_check("WiFi chiffré", "FAIL", "HIGH", details)
        except:
            self.add_check("WiFi chiffré", "WARNING", "MEDIUM", "Impossible de vérifier WiFi")
    
    def generate_report(self):
        """Génère le rapport de conformité"""
        percentage = int((self.score / self.max_score * 100)) if self.max_score > 0 else 0
        
        # Détermine le grade
        if percentage >= 90:
            grade = "A (Excellent)"
            emoji = "🟢"
        elif percentage >= 75:
            grade = "B (Bon)"
            emoji = "🟢"
        elif percentage >= 60:
            grade = "C (Acceptable)"
            emoji = "🟡"
        elif percentage >= 45:
            grade = "D (Faible)"
            emoji = "🟠"
        else:
            grade = "F (Critique)"
            emoji = "🔴"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "score": self.score,
            "max_score": self.max_score,
            "percentage": percentage,
            "grade": grade,
            "checks": self.checks
        }
        
        # Sauvegarde
        with open(self.compliance_report, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Affichage
        print("\n" + "="*70)
        print("📊 RÉSUMÉ DE CONFORMITÉ")
        print("="*70)
        print(f"\nScore: {emoji} {self.score}/{self.max_score} ({percentage}%)")
        print(f"Grade: {grade}\n")
        
        # Détails
        print("Résultats détaillés:")
        for check in self.checks:
            status_emoji = "✅" if check['status'] == "PASS" else "⚠️" if check['status'] == "WARNING" else "❌"
            print(f"\n   {status_emoji} {check['name']}")
            print(f"      Détails: {check['details']}")
        
        print(f"\n📁 Rapport complet sauvegardé: {self.compliance_report}")
        
        # Recommandations
        failures = [c for c in self.checks if c['status'] == 'FAIL']
        if failures:
            print(f"\n🔴 ACTIONS RECOMMANDÉES ({len(failures)} éléments non-conformes):")
            for check in failures:
                print(f"   • {check['name']}: {check['details']}")
        
        return report


def run_compliance():
    """Fonction principale"""
    checker = ComplianceChecker()
    checker.run_all_checks()


if __name__ == "__main__":
    run_compliance()
