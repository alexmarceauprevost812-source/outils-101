# 🚀 Démarrage Rapide - Outils 101

## ⚡ Installation (2 minutes)

### Linux
```bash
# 1. Clone le repo
git clone <repo_url>
cd outils101

# 2. Installe les dépendances
pip install -r requirements.txt

# 3. Lance l'outil
sudo python3 main.py
```

### Windows
```bash
# 1. Installe Npcap
# Télécharge: https://npcap.com/
# Double-clique et installe

# 2. Clone le repo
git clone <repo_url>
cd outils101

# 3. Installe les dépendances
pip install -r requirements.txt

# 4. Lance en mode Administrateur
python main.py
```

---

## 🎯 Première Utilisation (5 minutes)

### Étape 1 : Scanner ton réseau
```
Choix : 1
Réseau à scanner [192.168.1.0/24] : (appuie sur Entrée)
🔎 Scan ARP en cours...
✅ 5 appareil(s) détecté(s) !
```

### Étape 2 : Renommer tes appareils
```
Choix : 3
MAC de l'appareil : aa:bb:cc:dd:ee:ff
Nouveau nom : PC de Marc
✅ Renommé !
```

### Étape 3 : Audit WiFi
```
Choix : 16
🛡️ AUDIT SÉCURITÉ WiFi
[1] WPA2 | MonWiFi | -65dB | 🟡 BON
```

### Étape 4 : Générer un rapport
```
Choix : 13
✅ Rapport HTML généré !
📄 Ouvre : reports/audit_report_*.html
```

---

## 🔥 Les 5 Nouveaux Outils (STAR)

### ⭐ 1. Générer un rapport HTML complet
**Menu 13**
- Résumé du réseau
- Liste des appareils
- Historique complet
- Alertes détectées

👉 **Utilité** : Sauvegarde un audit professionnel du réseau

### ⭐ 2. Monitoring trafic réseau en direct
**Menu 14**
- Vois qui communique en temps réel
- Identifie les connexions anormales
- Détecte les activités suspectes

👉 **Utilité** : Surveille le trafic en live

### ⭐ 3. Détection MAC spoofing
**Menu 15**
- Détecte si une MAC change
- Identifie les usurpations d'identité
- Alerte si IP→MAC ou MAC→IP change

👉 **Utilité** : Sécurité - détecte les appareils piratés

### ⭐ 4. Audit WiFi avancé
**Menu 16**
- Analyse WPA2/WPA3
- Détecte WPS (vulnérable)
- Évalue la force du chiffrement
- Recommandations de sécurité

👉 **Utilité** : Vérifie ta sécurité WiFi

### ⭐ 5. Système de détection d'intrusion (IDS)
**Menu 17**
- Détecte les attaques DDoS
- Identifie les scans de ports agressifs
- Alerte sur les services dangereux
- Vérifie les comportements anormaux

👉 **Utilité** : Sécurité - alerte sur les attaques

---

## 🎓 Cas d'Usage Concrets

### "Je veux savoir qui est connecté à mon WiFi"
```
Choix : 1 (Scanner)
→ Liste complète des appareils
```

### "Je soupçonne un appareil pirate sur mon réseau"
```
Choix : 15 (MAC spoofing)
→ Détecte les changements de MAC
```

### "Mon WiFi est-il sécurisé?"
```
Choix : 16 (Audit WiFi avancé)
→ Évaluation complète + recommandations
```

### "Il y a une activité bizarre sur mon réseau"
```
Choix : 17 (Système d'intrusion)
→ Détecte les attaques possibles
Choix : 14 (Monitoring trafic)
→ Vois les connexions en temps réel
```

### "Je veux un rapport professionnel"
```
Choix : 13 (Rapport HTML)
→ Fichier beautifully formé
→ Partageable facilement
```

---

## 📊 Fichiers Générés Automatiquement

Après chaque utilisation :

```
devices.json                  # Tous tes appareils
logs/
├── devices_history.json     # Quand ils se connectent
└── alerts.json              # Alertes détectées

reports/
└── audit_report_*.html      # Rapports HTML

exports/
└── audit_export_*.json      # Exports JSON structurés

threats/
└── threats_*.json           # Menaces détectées (IDS)
```

---

## 💡 Astuces Pratiques

### Automatiser les scans
```
Choix : 10 (Automatisation)
Intervalle : 300 (5 minutes)
→ Scan toutes les 5 min + logs auto
```

### Renommer les appareils (important!)
```
Choix : 3 (Renommer)
"iPhone de Maman"
"Smart TV Samsung"
"Laptop de Marc"
→ Plus facile d'identifier les intrus
```

### Vérifier les logs
```
Choix : 11 (Alertes)
Choix : 12 (Historique)
→ Vois tous les changements du réseau
```

---

## ⚠️ Points Importants

✅ À faire :
- Scanner TON réseau
- Renommer tes appareils
- Auditer la sécurité WiFi
- Générer des rapports réguliers
- Vérifier les alertes

❌ À NE PAS faire :
- Scanner le réseau de quelqu'un d'autre
- Essayer de "casser" le WiFi
- Utiliser sur un réseau public
- Faire du brute-force

---

## 🆘 Aide Rapide

### "Pas d'appareil détecté"
→ Assure-toi d'être connecté au WiFi
→ Lance avec `sudo` sur Linux
→ Vérifie que le DHCP est actif

### "Erreur de permission"
→ Linux : `sudo python3 main.py`
→ Windows : Lance en Admin (clic droit)

### "Scapy ne marche pas"
→ Windows : Installe Npcap (https://npcap.com/)
→ Linux : `sudo apt install python3-scapy`

---

## 🎯 Prochaines Étapes

1. **Fais un premier scan** (Menu 1)
2. **Renomme tes appareils** (Menu 3)
3. **Audite ton WiFi** (Menu 16)
4. **Active l'automation** (Menu 10)
5. **Génère un rapport** (Menu 13)

---

## 📞 Support

Si tu as des problèmes :
1. Vérifie les prérequis (sudo, admin, connecté au réseau)
2. Relance le script
3. Cherche l'erreur dans les logs

Happy hacking! 🐧🌀
