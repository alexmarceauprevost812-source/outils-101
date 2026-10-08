# 🚀 START HERE - Outils 101

**Bienvenue! Ce fichier te guide pour démarrer immédiatement.**

---

## ⚡ Installation Super Rapide (2 min)

### Linux/macOS
```bash
# 1. Clone le projet
git clone <repo_url>
cd outils101

# 2. Installe
sudo bash install.sh

# 3. Lance
sudo python3 main.py
```

### Windows
```bash
# 1. Installe Npcap
# Télécharge: https://npcap.com/ et installe

# 2. Clone le projet
git clone <repo_url>
cd outils101

# 3. Installe
pip install -r requirements.txt

# 4. Lance (en Admin)
python main.py
```

---

## 🎯 Première Utilisation (5 min)

```
1. Lance Outils 101

2. Menu > Option 1
   (Scanne ton réseau, détecte les appareils)

3. Menu > Option 3
   (Renomme tes appareils pour les identifier)

4. Menu > Option 16
   (Vérifies la sécurité de ton WiFi)

5. Menu > Option 13
   (Génères un rapport HTML professionnel)
```

✅ **Terminé! Tu as maintenant:**
- Liste de tes appareils
- Vérification WiFi
- Rapport complet en HTML

---

## 📚 Documentation (Choisis Ton Chemin)

### 🏃 Pressé? (5-10 min)
→ **Lis QUICKSTART.md**
- Exemples concrets
- Les 5 nouveaux outils
- Cas d'usage courants

### 📖 Veut Comprendre? (30 min)
→ **Lis README.md**
- Fonctionnalités complètes
- Menu détaillé
- Explications professionnelles

### 🔧 Problèmes d'Installation?
→ **Lis INSTALLATION.md**
- Installation par OS
- Troubleshooting
- Optimisations

### 💻 Développeur?
→ **Lis DEV_SUMMARY.md**
- Architecture du projet
- Code internal
- Guide de contribution

### ❓ Besoin d'Aide Rapide?
→ **Lis HELP.txt**
- Menu et options
- Cas d'usage
- Problèmes courants

---

## ⭐ Les 5 Nouveaux Outils (v2.0)

### 1. 📊 Générer un Rapport (Menu 13)
Crée un beau rapport HTML avec tous les détails du réseau.
```
✨ Rapport professionnel
📈 Statistiques
📋 Appareils
🚨 Alertes
```

### 2. 📡 Monitoring Trafic (Menu 14)
Vois qui communique sur le réseau EN TEMPS RÉEL.
```
🔌 Connexions actives
⚡ Processus réseau
🚨 Activités anormales
```

### 3. 🚨 Détection MAC Spoofing (Menu 15)
Détecte si quelqu'un se fait passer pour un autre appareil.
```
🔴 1 IP avec plusieurs MACs
🔴 MAC changeant d'IP
🔴 Changement de fabricant
```

### 4. 🛡️ Audit WiFi Avancé (Menu 16)
Évalue la sécurité complète de ton WiFi.
```
📊 Score 0-10
🔍 Détecte WPS
⚠️ Détecte TKIP
💡 Recommandations
```

### 5. 🚨 Système d'Intrusion (Menu 17)
Détecte les attaques et comportements anormaux.
```
🔴 Détecte DDoS
🔍 Scan de ports agressifs
⚠️ Afflux d'appareils
🚨 Services dangereux
```

---

## 🎮 Menu Principal (18 Options)

```
DÉCOUVERTE (1-4)
  1. Scanner réseau
  2. Résumé appareils
  3. Renommer appareil
  4. Scanner ports

AUDIT (5-9)
  5. Versions vulnérables
  6. Audit WiFi
  7. DNS lookup
  8. Géolocalisation
  9. Audit SSL/TLS

AUTOMATISATION (10-12)
  10. Scan continu
  11. Voir alertes
  12. Voir historique

⭐ NOUVEAUX (13-17)
  13. Rapport HTML
  14. Monitoring trafic
  15. MAC spoofing
  16. Audit WiFi avancé
  17. Système IDS

QUITTER
  18. Quitter
```

---

## 💡 Cas d'Usage Courants

### "Qui est connecté à mon WiFi ?"
```
1. Menu > Option 1 (Scanner)
2. Menu > Option 3 (Renommer appareils)
3. Menu > Option 2 (Voir résumé)
```

### "Un appareil bizarre s'est connecté!"
```
1. Menu > Option 1 (Scanner)
2. Menu > Option 15 (Détection MAC spoofing)
3. Menu > Option 16 (Audit WiFi)
```

### "Mon WiFi est-il sécurisé?"
```
1. Menu > Option 16 (Audit WiFi avancé)
   → Score, protocole, WPS, etc.
```

### "Il y a une activité suspecte"
```
1. Menu > Option 17 (Système IDS)
   → Détecte attaques/anomalies
2. Menu > Option 14 (Monitoring)
   → Vois trafic en live
```

### "Je veux un rapport professionnel"
```
1. Menu > Option 13 (Rapport HTML)
   → Télécharge et partage
```

---

## 🐧 Installation Linux (Détail)

```bash
# Si tu veux faire manuellement:

# 1. Prérequis
sudo apt update
sudo apt install -y python3 python3-pip git

# 2. Clone
git clone https://github.com/user/outils101.git
cd outils101

# 3. Installe deps
pip3 install scapy requests

# 4. Crée dossiers
mkdir -p logs reports exports threats

# 5. Lance
sudo python3 main.py
```

Ou simplement:
```bash
sudo bash install.sh  # Tout automatique!
```

---

## 🪟 Installation Windows (Détail)

```bash
# 1. Installe Npcap
# Télécharge: https://npcap.com/
# Lance le .exe installer

# 2. Redémarre Windows

# 3. Clone
git clone https://github.com/user/outils101.git
cd outils101

# 4. Installe deps
pip install -r requirements.txt

# 5. Lance en Admin
# - Clic droit PowerShell
# - "Exécuter en tant qu'administrateur"
python main.py
```

---

## 🧪 Test d'Installation

```bash
# Vérifie que tout marche
python3 test_installation.py

# Devrait afficher: ✅ ✅ ✅ ... (7 tests)
```

---

## 📁 Fichiers Importants

### Docs Principales
- **START_HERE.md** ← Tu es ici
- **QUICKSTART.md** ← Guide 5min
- **README.md** ← Documentation complète
- **HELP.txt** ← Aide rapide

### Installation
- **INSTALLATION.md** ← Installation détaillée
- **install.sh** ← Script auto (Linux)
- **requirements.txt** ← Dépendances

### Code
- **main.py** ← Point d'entrée
- **outils101/cli.py** ← Menu principal
- **outils101/*.py** ← 17 outils

### Config
- **config_example.json** ← Exemple config
- **.gitignore** ← Fichiers ignorés

### Dev
- **DEV_SUMMARY.md** ← Architecture code
- **CHANGELOG.md** ← Historique v2.0
- **CONTRIBUTING.md** ← Comment contribuer

---

## ✅ Checklist Démarrage

- [ ] Python 3.7+ installé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Répertoires créés (`logs/`, `reports/`, etc.)
- [ ] Test passé (`python3 test_installation.py`)
- [ ] Première utilisation ok (`sudo python3 main.py`)
- [ ] Appareils détectés (Menu 1)
- [ ] Rapport généré (Menu 13)

---

## 🚨 Rappel Important

⚖️ **À usage DÉFENSIF UNIQUEMENT**

✅ Ce que tu peux faire:
- Scanner TON réseau
- Auditer TON WiFi
- Détecter les intrusions chez toi
- Générer des rapports
- Apprendre la cybersecurité

❌ Ce que tu NE peux PAS faire:
- Scanner le réseau de quelqu'un d'autre (ILLÉGAL!)
- Essayer de "casser" le WiFi
- Utiliser sur un réseau public
- Faire du brute-force
- Exploiter les vulnérabilités

---

## 🆘 Problèmes?

### "Permission denied"
```bash
# Linux/macOS: préfixe avec sudo
sudo python3 main.py
```

### "Aucun appareil détecté"
- Assure-toi d'être connecté au WiFi
- Vérifie que le DHCP est actif

### "Erreur Scapy Windows"
- Installe Npcap: https://npcap.com/
- Redémarre Windows
- Lance en mode Administrateur

### Plus de problèmes?
→ Lis **INSTALLATION.md** → Section Troubleshooting

---

## 🎓 Prochaines Étapes

### Immédiat (Hoje!)
1. Installe
2. Scanne ton réseau
3. Vérifie ton WiFi

### Demain
1. Active automation (Menu 10)
2. Génère rapport HTML (Menu 13)
3. Explore les autres outils

### Cette Semaine
1. Consulte la doc complète
2. Configure tes appareils
3. Mets à jour ton WiFi si nécessaire

### Pour Apprendre
1. Lis DEV_SUMMARY.md (architecture)
2. Explore le code Python
3. Modifie/améliore l'outil

---

## 📞 Besoin d'Aide?

| Besoin | Fichier |
|--------|---------|
| Aide rapide | HELP.txt |
| Guide 5min | QUICKSTART.md |
| Docs complètes | README.md |
| Installation | INSTALLATION.md |
| Architecture | DEV_SUMMARY.md |
| Problèmes | INSTALLATION.md → Troubleshooting |
| Contribuer | CONTRIBUTING.md |

---

## 🐧🌀 Prêt?

```bash
# Lance l'outil
sudo python3 main.py

# Et explore! 🚀
```

**Bon scanning! 🛡️**

---

**P.S. Si tu as des questions, lis d'abord HELP.txt ou README.md - probablement ta réponse y est!**
