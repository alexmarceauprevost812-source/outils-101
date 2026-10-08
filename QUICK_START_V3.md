# ⚡ Quick Start Outils 101 v3.0

## 1️⃣ Installation (2 min)

### Linux
```bash
cd outils101
pip install -r requirements.txt
sudo python3 main.py
```

### Windows
```bash
# Télécharge Npcap: https://npcap.com/
pip install -r requirements.txt
python main.py  # En mode Administrateur
```

---

## 2️⃣ Premier Test (5 min)

### Scan ton réseau
```bash
Menu : 1
→ Réseau à scanner [auto] : (Appuie sur Enter)
→ ✅ Vois tous les appareils connectés
```

### Renomme tes appareils
```bash
Menu : 2
Menu : 3
→ Renomme chaque MAC pour pouvoir l'identifier
```

---

## 3️⃣ Les 3 Nouveaux Outils (v3.0)

### 🍯 Honeypot (Option 18)
**Pour** : Détecter les attaquants  
**Fait** : Piège qui enregistre les tentatives de connexion  
**Usage** : Laisse-le tourner, il enregistre automatiquement
```bash
Menu : 18
→ Option 1: Démarrer (Ctrl+C pour arrêter)
→ Option 2: Voir les alertes
→ 📁 Fichier log: logs/honeypot_alerts.json
```

### 🔬 Forensics (Option 19)
**Pour** : Enquêter sur une attaque passée  
**Fait** : Analyse les logs pour retrouver les traces  
**Usage** : Après un incident de sécurité
```bash
Menu : 19
→ Automatique: scan et rapport
→ 📁 Fichier log: logs/forensics_report.json
```

### ✅ Compliance (Option 20)
**Pour** : Vérifier ta sécurité  
**Fait** : Teste 9 domaines, note ta config (A-F)  
**Usage** : Avant un incident (prévention)
```bash
Menu : 20
→ Automatique: scan complet
→ 📊 Score + Recommandations
→ 📁 Fichier log: logs/compliance_report.json
```

---

## 🎯 Utilisation Recommandée

### Chaque jour (5 min)
```bash
Menu : 1   → Scanner réseau
Menu : 11  → Voir les alertes
```

### Chaque semaine (15 min)
```bash
Menu : 18  → Honeypot (30 sec)
Menu : 20  → Compliance (5 min)
Menu : 13  → Générer rapport HTML
```

### Après un incident
```bash
Menu : 19  → Forensics (enquête)
Menu : 14  → Traffic monitor (voir le trafic)
```

---

## 📁 Fichiers Générés

```
devices.json                 ← Appareils connus
logs/
├── devices_history.json    ← Historique connexions
├── alerts.json             ← Alertes du système
├── honeypot_alerts.json    ← 🍯 Alertes honeypot
├── forensics_report.json   ← 🔬 Rapport enquête
└── compliance_report.json  ← ✅ Score conformité

reports/
└── audit_report_*.html     ← Rapport HTML beau

exports/
└── network_audit_*.json    ← Données JSON
```

---

## 🔥 Top 5 Commandes Utiles

```bash
# 1. Scan complet du réseau
Menu : 1

# 2. Voir qui est connecté
Menu : 2

# 3. Générer un rapport PDF/HTML
Menu : 13

# 4. Lancer honeypot (détecter attaquants)
Menu : 18

# 5. Vérifier ta conformité de sécurité
Menu : 20
```

---

## ⚠️ Rappels Importants

✅ **À faire**
- Utilise sur **TON** réseau uniquement
- Lance avec `sudo` sur Linux
- Lance en mode Admin sur Windows
- Renomme tes appareils pour t'y retrouver

❌ **À NE PAS faire**
- Pas de brute-force de mot de passe
- Pas de déauthentification (deauth)
- Pas d'injection de paquets
- Pas d'exploitation de failles

---

## 📊 Résultats Attendus

### Après un scan (Menu 1)
```
✅ 12 appareils détectés
⚠️ 1 nouvel appareil (vérifier si reconnu)
```

### Après Compliance (Menu 20)
```
Score: 78/100
Grade: B (Bon)
Recommendations: 3 actions
```

### Après Honeypot (Menu 18)
```
Alertes: 0 (bon signe!)
Menaces: Aucune
Status: Sécurisé
```

---

## 🚀 Cas d'Usage

### 👤 Utilisateur lambda
```
Menu 1  → Scanner réseau (qui est connecté ?)
Menu 20 → Compliance (suis-je sécurisé ?)
Menu 13 → Générer rapport (garde une trace)
```

### 🔒 Admin réseau
```
Menu 10 → Automation (scan continu)
Menu 18 → Honeypot (détecte attaquants)
Menu 19 → Forensics (enquête si incident)
```

### 🎓 Étudiant cybersec
```
Explore tous les outils!
Menu 1-20 pour apprendre la sécurité réseau
```

---

## 💡 Tips & Tricks

### 1. Automatiser les scans
```bash
Menu : 10
→ Lance scan continu (par ex. 1 scan/min)
→ Historique auto-sauvegardé
→ Alertes auto si nouveau device
```

### 2. Générer rapports récurrents
```bash
Menu : 13
→ HTML : ouvre dans navigateur
→ JSON : pour traiter automatiquement
→ PDF : pour partager
```

### 3. Combiner outils
```bash
Menu 1 + 20 = Scanner + Compliance
Menu 18 + 19 = Honeypot + Forensics
Menu 14 + 17 = Monitor + IDS
```

### 4. Lire les logs JSON
```bash
# Terminal
cat logs/honeypot_alerts.json | python3 -m json.tool

# Python
import json
with open('logs/compliance_report.json') as f:
    data = json.load(f)
print(f"Score: {data['percentage']}%")
```

---

## 🆘 Problèmes Courants

| Problème | Solution |
|----------|----------|
| "Permission denied" | Utilise `sudo` sur Linux |
| "Port already in use" | Change de port ou arrête le service |
| "Aucun appareil détecté" | Vérifie que tu es connecté au réseau |
| "ImportError: scapy" | `pip install -r requirements.txt` |
| "Honeypot : pas de résultats" | Laisse-le tourner + attends attaques |

---

## 📚 Pour Aller Plus Loin

```bash
# Lire la doc complète
cat README.md

# Lire les détails des 3 nouveaux outils
cat NEW_TOOLS_V3.md

# Lire les logs générés
cat logs/honeypot_alerts.json | json.tool
cat logs/compliance_report.json | json.tool

# Regarder le code
cat outils101/honeypot.py
cat outils101/forensics.py
cat outils101/compliance.py
```

---

## ✅ Checklist de Démarrage

- [ ] Installation (`pip install -r requirements.txt`)
- [ ] Lancement (`sudo python3 main.py`)
- [ ] Scanner réseau (Menu 1)
- [ ] Renommer appareils (Menu 3)
- [ ] Générer rapport (Menu 13)
- [ ] Essayer Honeypot (Menu 18)
- [ ] Essayer Compliance (Menu 20)
- [ ] Lire les logs JSON
- [ ] Appliquer recommandations
- [ ] Re-scanner pour vérifier

---

**Outils 101 v3.0 - Démarrage Rapide ⚡**

🐧🌀 Prêt? Lance `sudo python3 main.py` maintenant!
