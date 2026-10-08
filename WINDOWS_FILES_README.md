# 🪟 Fichiers Windows - Guide Complet

## 📦 Fichiers Créés pour Windows 11

Ce projet contient **plusieurs fichiers** pour faciliter l'installation sur Windows 11. Voici ce que tu dois utiliser :

---

## 🎯 Fichiers d'Installation

### **1. `WINDOWS_COMMANDS.bat` ⭐ (LE PLUS FACILE)**

**Qu'est-ce que c'est ?**
- Script batch automatisé pour Windows
- Fait tout d'un coup (vérifie, clone, installe)
- Le plus simple pour débuter

**Comment l'utiliser :**
```
1. Double-clique sur WINDOWS_COMMANDS.bat
2. Clic droit > "Exécuter en tant qu'administrateur"
3. Suis les messages à l'écran
4. Attends 2-3 minutes
```

**Avantages :**
- ✅ Entièrement automatisé
- ✅ Détecte les erreurs
- ✅ Installe tout (Python, Git, dépendances...)
- ✅ Affichage coloré + clair

**Inconvénients :**
- ❌ Batch (plus vieux) que PowerShell
- ❌ Dépend de Windows native features

---

### **2. `install.ps1` (MODERNE)**

**Qu'est-ce que c'est ?**
- Script PowerShell (plus moderne que batch)
- Fait tout comme le .bat
- Interface colorée & professionnelle

**Comment l'utiliser :**
```powershell
# 1. Ouvre PowerShell EN ADMINISTRATEUR
# 2. Tape ceci une fois :
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 3. Va dans le dossier du projet :
cd C:\Users\...\source

# 4. Lance le script :
.\install.ps1

# 5. Suis les messages
```

**Avantages :**
- ✅ Plus moderne que batch
- ✅ Mieux pour les scripts complexes
- ✅ Intégration Windows avancée

**Inconvénients :**
- ❌ Nécessite de configurer ExecutionPolicy
- ❌ Plus d'étapes pour démarrer

---

### **3. `run.bat` (LANCER L'OUTIL)**

**Qu'est-ce que c'est ?**
- Lance Outils 101 facilement
- À utiliser APRÈS l'installation

**Comment l'utiliser :**
```
1. Double-clique sur run.bat
2. Clic droit > "Exécuter en tant qu'administrateur"
3. L'outil démarre !
```

**Avantages :**
- ✅ Ultra simple
- ✅ Une seule ligne de code
- ✅ Parfait pour les utilisateurs non-tech

---

## 📖 Fichiers de Documentation

### **4. `WINDOWS_INSTALL_SIMPLE.md` ⭐ (GUIDE COMPLET)**

**Le plus complet !** Guide pas-à-pas avec :
- Prérequis détaillés
- 2 méthodes (automatique + manuel)
- Erreurs courantes + solutions
- Tests de vérification
- Conseils utiles

**Quand l'utiliser :**
- Tu veux tout comprendre
- Tu as une erreur spécifique
- Tu veux la méthode manuelle

**Sections principales :**
1. Prérequis (Python, Git, Npcap)
2. Installation (auto + manuelle)
3. Erreurs & solutions (5 erreurs couvertes)
4. Tests de vérification
5. Premiers pas

---

### **5. `QUICK_FIX_WINDOWS.txt` (AIDE RAPIDE)**

**Le plus court !** Pour les cas urgents :
- Lancer en 3 clics
- Erreurs + solutions rapides
- Vérifications rapides
- Points clés

**Quand l'utiliser :**
- Tu es pressé
- Tu as juste besoin d'une solution rapide
- Tu veux du concis

---

### **6. `WINDOWS_INSTALL.md` (ANCIENNE VERSION)**

**Attention :** Ceci est l'ancienne documentation.  
→ Utilise plutôt `WINDOWS_INSTALL_SIMPLE.md`

---

## 🎯 Recommandation : QUEL FICHIER UTILISER ?

```
┌─────────────────────────────────────────────────────┐
│     JE SUIS... → J'UTILISE...                       │
├─────────────────────────────────────────────────────┤
│ Pressé & débutant      → WINDOWS_COMMANDS.bat       │
│ Qui aime Windows        → install.ps1               │
│ Qui veut comprendre    → WINDOWS_INSTALL_SIMPLE.md │
│ Qui a une erreur       → QUICK_FIX_WINDOWS.txt     │
│ Qui relance l'outil    → run.bat                    │
└─────────────────────────────────────────────────────┘
```

---

## 📋 Flux d'Installation Complet

### **Première Installation**

```
START
  │
  ├─ Défaut? (NO) ──────→ Lire WINDOWS_INSTALL_SIMPLE.md
  │
  ├─ Oui, fais-le vite! ──→ WINDOWS_COMMANDS.bat
  │                         └─→ Double-clique
  │                             └─→ Admin
  │                                 └─→ Attends
  │                                     └─→ FIN ✅
  │
  └─ J'aime PowerShell ──→ install.ps1
                          └─→ PowerShell Admin
                              └─→ Set-ExecutionPolicy...
                                  └─→ .\install.ps1
                                      └─→ FIN ✅
```

### **Utilisation Quotidienne**

```
Tu veux lancer l'outil?
  │
  ├─ Je veux juste ça ──→ Double-clique run.bat (Admin)
  │
  └─ Terminal ──────────→ Command Prompt (Admin) → python main.py
```

---

## ✅ Checklist Avant de Lancer

- [ ] Windows 11 64-bit ?
- [ ] Python 3.8+ installé ? (`python --version`)
- [ ] Git installé ? (`git --version`)
- [ ] Npcap installé ? (`npcap-config --version`)
- [ ] PC redémarré après Npcap ?
- [ ] Lancé en ADMINISTRATEUR ?

Si tout ✅ → tu peux y aller !

---

## 🚀 Les 3 Étapes Magiques

### **Étape 1 : Installer**
```batch
Double-clique WINDOWS_COMMANDS.bat (Admin)
```

### **Étape 2 : Attendre**
```
Ça prend 2-3 minutes (normal)
```

### **Étape 3 : Lancer**
```batch
Double-clique run.bat (Admin)
```

**Boum ! C'est lancé ! 🎉**

---

## 🔧 Troubleshooting Rapide

| Erreur | Fichier à Consulter |
|--------|-------------------|
| Python not found | QUICK_FIX_WINDOWS.txt |
| Npcap missing | WINDOWS_INSTALL_SIMPLE.md |
| Access denied | WINDOWS_INSTALL_SIMPLE.md |
| Je suis bloqué | QUICK_FIX_WINDOWS.txt |
| Je veux tout | README.md |
| Je veux manual | WINDOWS_INSTALL_SIMPLE.md |

---

## 📞 Support

**Je suis bloqué ?**

1. Lis `QUICK_FIX_WINDOWS.txt` (30 sec)
2. Si pas de réponse, lis `WINDOWS_INSTALL_SIMPLE.md` (5 min)
3. Copie l'erreur exacte et partage-la

**Output à donner :**
```cmd
python --version
pip --version
git --version
npcap-config --version
# + l'erreur exacte en rouge
```

---

## 📁 Vue d'Ensemble des Fichiers

```
outils101/
├── WINDOWS_COMMANDS.bat          ⭐ Installation automatique
├── install.ps1                   ⭐ Installation PowerShell
├── run.bat                        ⭐ Lancer l'outil
├── WINDOWS_INSTALL_SIMPLE.md     📖 Guide complet
├── WINDOWS_INSTALL.md            📖 Guide old (obsolète)
├── QUICK_FIX_WINDOWS.txt         📖 Aide rapide
├── WINDOWS_FILES_README.md       📖 CE FICHIER
│
├── main.py                       🐍 Point d'entrée
├── requirements.txt              📦 2 dépendances (scapy, requests)
├── README.md                     📖 Doc générale
│
└── outils101/                    📦 Tous les modules Python
    ├── cli.py
    ├── scanner.py
    ├── honeypot.py
    ├── forensics.py
    └── 25+ autres modules...
```

---

## 🎊 Résumé

**Pour Windows 11, tu as :**

1. **Scripts d'installation** : 2 fichiers (batch + PowerShell)
2. **Script de lancement** : 1 fichier (run.bat)
3. **Documentation** : 3 fichiers (complet + rapide + old)

**Le chemin le plus simple :**
```
WINDOWS_COMMANDS.bat → run.bat → Explorer l'outil
```

**Bonne installation ! 🐧🌀**

---

*Dernière mise à jour : Outils 101 v3.0*  
*Platform: Windows 11 64-bit*  
*Status: ✅ Production-Ready*
