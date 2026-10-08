# 📦 Guide d'Installation Détaillé - Outils 101

## Prérequis Système

### Linux
- Python 3.7+
- Root/sudo pour les scans réseau
- Pip (gestionnaire paquets Python)

### Windows
- Python 3.7+
- Administrator mode requis
- Npcap (pour scapy)

### macOS
- Python 3.7+
- Root/sudo pour les scans réseau

---

## 🐧 Installation sur Linux (Ubuntu/Debian)

### Étape 1 : Mettre à jour le système
```bash
sudo apt update
sudo apt upgrade -y
```

### Étape 2 : Installer Python et pip
```bash
sudo apt install -y python3 python3-pip
python3 --version  # Vérifie que c'est 3.7+
```

### Étape 3 : Cloner Outils 101
```bash
git clone https://github.com/<USERNAME>/outils101.git
cd outils101
```

### Étape 4 : Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 5 : Lancer l'outil
```bash
sudo python3 main.py
```

✅ **Terminé!** Tu devrais voir le menu principal.

---

## 🪟 Installation sur Windows

### Étape 1 : Installer Python
1. Va sur https://www.python.org/downloads/
2. Télécharge Python 3.9+ (64-bit)
3. Lance l'installateur
4. ⚠️ **IMPORTANT** : Coche "Add Python to PATH"
5. Clique "Install Now"

### Étape 2 : Installer Npcap
1. Va sur https://npcap.com/
2. Télécharge **Npcap Installer**
3. Lance `npcap-*.exe`
4. Installe avec les options par défaut
5. ⚠️ Redémarre Windows

### Étape 3 : Cloner Outils 101
1. Ouvre PowerShell (Ctrl+X, puis clique PowerShell)
2. Tape :
```powershell
git clone https://github.com/<USERNAME>/outils101.git
cd outils101
```

### Étape 4 : Installer les dépendances
```powershell
pip install -r requirements.txt
```

### Étape 5 : Lancer en Mode Administrateur
1. Clique droit sur PowerShell
2. Sélectionne "Exécuter en tant qu'administrateur"
3. Tape :
```powershell
python main.py
```

✅ **Terminé!** Le menu devrait s'afficher.

---

## 🍎 Installation sur macOS

### Étape 1 : Installer Homebrew (si pas fait)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Étape 2 : Installer Python
```bash
brew install python3
python3 --version  # Vérifie que c'est 3.7+
```

### Étape 3 : Cloner Outils 101
```bash
git clone https://github.com/<USERNAME>/outils101.git
cd outils101
```

### Étape 4 : Installer les dépendances
```bash
pip3 install -r requirements.txt
```

### Étape 5 : Lancer l'outil
```bash
sudo python3 main.py
```

✅ **Terminé!**

---

## 🔧 Installation des Dépendances (Détail)

### Scapy (Scan ARP)
```bash
pip install scapy
```
- Nécessaire pour ARP scanning
- Manipulation de paquets réseau
- Cross-platform (Linux/Windows/macOS)

### Requests (Géolocalisation IP)
```bash
pip install requests
```
- Requêtes HTTP
- Appels API pour geoIP

---

## ✅ Vérifier l'Installation

### Test 1 : Python correct
```bash
python3 --version
# Doit afficher : Python 3.7+ (ou plus)
```

### Test 2 : Pip correct
```bash
pip3 --version
# Doit afficher : pip XX.X.X
```

### Test 3 : Scapy installé
```bash
python3 -c "import scapy; print('Scapy OK')"
# Doit afficher : Scapy OK
```

### Test 4 : Lancer Outils 101
```bash
sudo python3 main.py
# Doit afficher le menu principal
```

---

## 🚨 Problèmes Courants

### ❌ "Command not found: python3"
**Solution** :
- Linux : `sudo apt install python3`
- Windows : Réinstalle Python et coche "Add to PATH"
- macOS : `brew install python3`

### ❌ "No module named 'scapy'"
**Solution** :
```bash
pip install scapy
```

### ❌ "Permission denied" (Linux)
**Solution** :
```bash
sudo python3 main.py
```

### ❌ "Winsock error" (Windows)
**Solution** :
1. Installe Npcap depuis https://npcap.com/
2. Redémarre Windows
3. Relance en mode Administrateur

### ❌ "No networks detected"
**Solution** :
- Vérifie que tu es connecté au WiFi
- Linux : `iwconfig` ou `nmcli` pour vérifier la connexion
- Windows : `ipconfig` pour vérifier l'IP

### ❌ "Cannot connect to API" (géolocalisation)
**Solution** :
- Vérifie ta connexion Internet
- ip-api.com peut être bloqué dans certains réseaux

---

## 🎯 Configuration Post-Installation

### 1. Tester le premier scan
```bash
sudo python3 main.py
# Menu > Option 1
# Valide le réseau proposé (Entrée)
# Attends 10-30 secondes
```

### 2. Renommer tes appareils
```bash
# Menu > Option 3
# Renomme tes 3-4 appareils principaux
# ("PC de Marc", "iPhone de Maman", etc.)
```

### 3. Activer l'automation
```bash
# Menu > Option 10
# Intervalle : 300 (5 minutes)
# Laisse tourner en arrière-plan
```

### 4. Vérifier les logs
```bash
# Menu > Option 11 (Alertes)
# Menu > Option 12 (Historique)
```

---

## 📁 Arborescence Post-Installation

```
outils101/
├── main.py                      # Point d'entrée
├── requirements.txt             # Dépendances
├── README.md                    # Documentation
├── QUICKSTART.md               # Guide rapide
├── INSTALLATION.md             # Ce fichier
├── CHANGELOG.md                # Historique
├── outils101/                  # Package principal
│   ├── __init__.py
│   ├── scanner.py
│   ├── portscan.py
│   ├── vendor.py
│   ├── storage.py
│   ├── automation.py
│   ├── dnslookup.py
│   ├── geoip.py
│   ├── ssl_audit.py
│   ├── banner.py
│   ├── vulndb.py
│   ├── wifiaudit.py
│   ├── cli.py
│   ├── report_generator.py      # ⭐ NEW
│   ├── traffic_monitor.py       # ⭐ NEW
│   ├── mac_spoofing_detector.py # ⭐ NEW
│   ├── wifi_security_audit.py   # ⭐ NEW
│   └── intrusion_detection.py   # ⭐ NEW
├── devices.json                 # (créé après 1er scan)
└── logs/                        # (créé après automation)
    ├── devices_history.json
    └── alerts.json
```

Après les premières utilisations :
```
reports/                        # Rapports HTML
exports/                        # Exports JSON
threats/                        # Menaces détectées
```

---

## 🔐 Permissions Réseau

### Linux
```bash
# Tester qui a accès au réseau
sudo python3 main.py
# Taper root password
```

### Windows
1. Clic droit sur PowerShell
2. "Exécuter en tant qu'administrateur"
3. Tape le mot de passe administrateur

### macOS
```bash
sudo python3 main.py
# Taper mot de passe de session
```

---

## 🆕 Mise à Jour Future

Pour mettre à jour Outils 101 :

```bash
cd outils101
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## 💡 Optimisations (Optionnel)

### Créer un alias Linux (raccourci)
```bash
echo "alias outils101='sudo python3 /chemin/vers/outils101/main.py'" >> ~/.bashrc
source ~/.bashrc

# Ensuite, tape juste :
outils101
```

### Créer un raccourci Windows
1. Fais clic droit sur le bureau
2. "New" → "Shortcut"
3. Localisation : `powershell.exe -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process; & 'C:\chemin\vers\outils101\main.py'"`
4. Clic droit sur le raccourci → Propriétés
5. Avancé → Cocher "Exécuter en tant qu'administrateur"

---

## 📞 Support d'Installation

Si tu rencontres des problèmes :

1. **Vérifie les prérequis** (Python 3.7+, pip, sudo/admin)
2. **Relance l'installateur**
3. **Redémarre** (Windows particulièrement)
4. **Regarde les logs** (Error messages)
5. **Fais un issue** sur GitHub

---

## 🎉 Prêt à utiliser!

Après l'installation réussie :

```bash
sudo python3 main.py
# Tu verras :
#   ___       _   _ _          _  __  _
#  / _ \ _  _| |_(_) |___   _ | |/ _|/ |
# | | | | || |  _| | (_-<  | || |  _| |
#  \___/ \_,_|\__|_|_/__/  |_||_|_|  |_|
# 
#      Outils 101 - Surveillance WiFi locale
```

🐧🌀 Happy scanning!
