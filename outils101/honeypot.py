#!/usr/bin/env python3
"""
Honeypot Simulator - Piège les attaquants potentiels
Crée des faux services (SSH, HTTP, FTP) pour détecter les tentatives d'accès
"""

import socket
import threading
import time
import json
from datetime import datetime
from pathlib import Path


class HoneypotServer:
    """Serveur honeypot multi-service"""
    
    def __init__(self, log_file="logs/honeypot_alerts.json"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.alerts = []
        self.running = False
        self.ports = {
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            80: "HTTP",
            443: "HTTPS",
            3306: "MySQL",
            5432: "PostgreSQL",
            8080: "HTTP-Alt"
        }
        self.load_alerts()
    
    def load_alerts(self):
        """Charge les alertes existantes"""
        if self.log_file.exists():
            try:
                with open(self.log_file) as f:
                    self.alerts = json.load(f)
            except:
                self.alerts = []
    
    def save_alert(self, alert):
        """Sauvegarde une alerte"""
        self.alerts.append(alert)
        with open(self.log_file, 'w') as f:
            json.dump(self.alerts, f, indent=2)
    
    def log_connection_attempt(self, ip, port, service, data=""):
        """Enregistre une tentative de connexion"""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "source_ip": ip,
            "port": port,
            "service": service,
            "data": data[:100] if data else "",
            "threat_level": self._assess_threat(service, data)
        }
        self.save_alert(alert)
        return alert
    
    def _assess_threat(self, service, data):
        """Évalue le niveau de menace"""
        threat_keywords = [
            "admin", "root", "password", "passwd", "login",
            "select", "drop", "union", "inject", "script",
            "wget", "curl", "nc", "bash"
        ]
        
        data_lower = data.lower() if data else ""
        
        if any(kw in data_lower for kw in threat_keywords):
            return "HIGH"
        elif service in ["SSH", "Telnet", "MySQL"]:
            return "MEDIUM"
        else:
            return "LOW"
    
    def handle_ssh_connection(self, sock, ip):
        """Simule un serveur SSH"""
        try:
            sock.send(b"SSH-2.0-OpenSSH_7.4\r\n")
            data = sock.recv(1024).decode('utf-8', errors='ignore')
            
            if data:
                alert = self.log_connection_attempt(ip, 22, "SSH", data)
                print(f"[🚨 HONEYPOT SSH] {ip} - Menace: {alert['threat_level']}")
            
            sock.send(b"Invalid authentication request\r\n")
        except:
            pass
    
    def handle_http_connection(self, sock, ip):
        """Simule un serveur HTTP"""
        try:
            data = sock.recv(1024).decode('utf-8', errors='ignore')
            
            if data:
                alert = self.log_connection_attempt(ip, 80, "HTTP", data)
                print(f"[🚨 HONEYPOT HTTP] {ip} - Menace: {alert['threat_level']}")
            
            response = b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
            sock.send(response)
        except:
            pass
    
    def handle_telnet_connection(self, sock, ip):
        """Simule un serveur Telnet"""
        try:
            sock.send(b"Welcome to Telnet Server\r\nLogin: ")
            data = sock.recv(1024).decode('utf-8', errors='ignore')
            
            if data:
                alert = self.log_connection_attempt(ip, 23, "Telnet", data)
                print(f"[🚨 HONEYPOT TELNET] {ip} - Menace: {alert['threat_level']}")
            
            sock.send(b"Access Denied\r\n")
        except:
            pass
    
    def handle_ftp_connection(self, sock, ip):
        """Simule un serveur FTP"""
        try:
            sock.send(b"220 FTP Server Ready\r\n")
            data = sock.recv(1024).decode('utf-8', errors='ignore')
            
            if data:
                alert = self.log_connection_attempt(ip, 21, "FTP", data)
                print(f"[🚨 HONEYPOT FTP] {ip} - Menace: {alert['threat_level']}")
            
            sock.send(b"530 Login incorrect\r\n")
        except:
            pass
    
    def start_port_listener(self, port, handler_func):
        """Lance un écouteur sur un port"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server.bind(("0.0.0.0", port))
            server.listen(5)
            server.settimeout(1)
            
            while self.running:
                try:
                    sock, (ip, _) = server.accept()
                    t = threading.Thread(target=handler_func, args=(sock, ip))
                    t.daemon = True
                    t.start()
                except socket.timeout:
                    continue
        except Exception as e:
            print(f"[❌] Erreur port {port}: {e}")
        finally:
            server.close()
    
    def start_honeypot(self, ports=None):
        """Démarre le honeypot sur les ports spécifiés"""
        if ports is None:
            ports = [22, 23, 80]
        
        self.running = True
        handlers = {
            22: self.handle_ssh_connection,
            23: self.handle_telnet_connection,
            80: self.handle_http_connection,
            21: self.handle_ftp_connection,
            25: self.handle_smtp_connection if hasattr(self, 'handle_smtp_connection') else self.handle_http_connection
        }
        
        print(f"\n🍯 Honeypot en cours de démarrage sur les ports: {ports}")
        print("    Les attaquants seront détectés et enregistrés...")
        print("    Appuyez sur Ctrl+C pour arrêter\n")
        
        threads = []
        for port in ports:
            if port in handlers:
                handler = handlers[port]
                t = threading.Thread(target=self.start_port_listener, args=(port, handler))
                t.daemon = True
                t.start()
                threads.append(t)
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⏹️  Honeypot arrêté")
            self.running = False
    
    def show_alerts_summary(self):
        """Affiche un résumé des alertes"""
        if not self.alerts:
            print("\n✅ Aucune tentative de connexion détectée")
            return
        
        print(f"\n📊 RÉSUMÉ HONEYPOT - {len(self.alerts)} tentatives détectées\n")
        
        by_ip = {}
        by_service = {}
        by_threat = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        
        for alert in self.alerts:
            ip = alert["source_ip"]
            service = alert["service"]
            threat = alert["threat_level"]
            
            by_ip[ip] = by_ip.get(ip, 0) + 1
            by_service[service] = by_service.get(service, 0) + 1
            by_threat[threat] += 1
        
        print("⚠️  Menaces par niveau:")
        for level, count in by_threat.items():
            emoji = "🔴" if level == "HIGH" else "🟡" if level == "MEDIUM" else "🟢"
            print(f"   {emoji} {level}: {count}")
        
        print("\n🔗 IPs suspectes:")
        for ip, count in sorted(by_ip.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {ip}: {count} tentatives")
        
        print("\n🎯 Services ciblés:")
        for service, count in sorted(by_service.items(), key=lambda x: x[1], reverse=True):
            print(f"   {service}: {count} tentatives")


def run_honeypot():
    """Fonction principale pour lancer le honeypot"""
    honeypot = HoneypotServer()
    
    print("\n" + "="*60)
    print("🍯 HONEYPOT - Piège à Attaquants")
    print("="*60)
    print("\nOptions:")
    print("1. Démarrer le honeypot (ports 22, 23, 80)")
    print("2. Afficher les alertes détectées")
    print("3. Quitter")
    
    choice = input("\nChoisir une option (1-3): ").strip()
    
    if choice == "1":
        honeypot.start_honeypot([22, 23, 80])
    elif choice == "2":
        honeypot.show_alerts_summary()
    else:
        print("Quitter...")


if __name__ == "__main__":
    run_honeypot()
