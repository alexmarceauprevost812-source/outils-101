"""
Monitoring temps réel du trafic réseau.
Affiche qui communique avec qui en live.
"""

import subprocess
import re
from collections import defaultdict
from datetime import datetime


def get_active_connections():
    """Récupère les connexions réseau actives."""
    connections = defaultdict(int)
    
    try:
        # Linux
        result = subprocess.run(
            ["netstat", "-an", "-t"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        lines = result.stdout.split('\n')
        for line in lines:
            if 'ESTABLISHED' in line or 'LISTEN' in line:
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        local = parts[3].split(':')[0]
                        remote = parts[4].split(':')[0] if len(parts) > 4 else "N/A"
                        if local and remote != "N/A":
                            key = f"{local} → {remote}"
                            connections[key] += 1
                    except:
                        pass
    except Exception as e:
        print(f"⚠️ Erreur netstat: {e}")
    
    return connections


def get_active_processes():
    """Récupère les processus actifs réseau."""
    processes = []
    
    try:
        # Linux avec lsof
        result = subprocess.run(
            ["sudo", "lsof", "-i", "-P", "-n"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        lines = result.stdout.split('\n')[1:]  # Skip header
        for line in lines[:20]:  # Top 20
            if line.strip():
                parts = line.split()
                if len(parts) >= 9:
                    processes.append({
                        "command": parts[0],
                        "pid": parts[1],
                        "protocol": parts[7],
                        "connection": parts[8]
                    })
    except Exception as e:
        print(f"⚠️ Erreur lsof: {e}")
    
    return processes


def display_live_monitor(duration=30):
    """Affiche un monitoring live du trafic réseau."""
    
    print("\n" + "="*80)
    print("🔴 MONITORING TRAFIC RÉSEAU EN DIRECT")
    print("="*80)
    print(f"Démarrage à {datetime.now().strftime('%H:%M:%S')}")
    print(f"Durée : {duration} secondes | Appuyez sur Ctrl+C pour arrêter\n")
    
    try:
        import time
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Connexions actives
            connections = get_active_connections()
            processes = get_active_processes()
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Connexions actives:")
            print("-" * 80)
            
            if connections:
                sorted_conn = sorted(
                    connections.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]
                
                for conn, count in sorted_conn:
                    print(f"  {conn:<50} ({count} connexions)")
            else:
                print("  Aucune connexion détectée")
            
            # Processus réseau
            print(f"\n📊 Top processus réseau:")
            print("-" * 80)
            if processes:
                for proc in processes[:5]:
                    print(f"  {proc['command']:<15} (PID: {proc['pid']:<6}) → {proc['connection']}")
            else:
                print("  Aucun processus détecté")
            
            print("\n" + "="*80)
            time.sleep(5)
    
    except KeyboardInterrupt:
        print("\n\n⛔ Monitoring arrêté.")
    except Exception as e:
        print(f"❌ Erreur monitoring: {e}")


def detect_unusual_activity(threshold=50):
    """Détecte les activités réseau anormales."""
    
    print("\n" + "="*80)
    print("🚨 DÉTECTION ACTIVITÉ ANORMALE")
    print("="*80)
    print(f"Seuil : {threshold} connexions/intervalle\n")
    
    try:
        connections = get_active_connections()
        total = sum(connections.values())
        
        print(f"Total connexions : {total}")
        
        if total > threshold:
            print(f"⚠️ ALERTE : Nombre de connexions élevé ({total} > {threshold})")
            print("🔴 Possible attaque DDoS ou scan agressif détecté!\n")
            
            # Top talkers
            sorted_conn = sorted(
                connections.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            print("Top adresses suspectes:")
            for conn, count in sorted_conn:
                print(f"  - {conn} : {count} connexions")
        else:
            print("✅ Activité normale")
    
    except Exception as e:
        print(f"❌ Erreur : {e}")
