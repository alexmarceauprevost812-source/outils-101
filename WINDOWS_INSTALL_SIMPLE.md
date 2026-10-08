# 🪟 Installation Outils 101 sur Windows 11 - GUIDE SIMPLIFIÉ

## ✅ Prérequis (avant de commencer)

Tu dois avoir installé **3 trucs** :

1. **Python 3.8+** → https://www.python.org/downloads/
   - ⚠️ **IMPORTANT** : Pendant l'installation, COCHE "Add Python to PATH"
   
2. **Git** → https://git-scm.com/download/win
   - Lance l'installateur, accepte tout par défaut

3. **Npcap** → https://npcap.com/download/ 
   - ⚠️ **IMPORTANT** : Coche "Install Npcap in WinPcap API-compatible Mode"
   - **Redémarre ton PC après**

---

## 🚀 Installation (2 minutes)

### **Option 1 : Script Automatique (FACILE)**

1. **Télécharge** `WINDOWS_COMMANDS.bat` depuis le projet
2. **Fais un clic droit dessus** → `Exécuter en tant qu'administrateur`
3. **Suis les instructions à l'écran**
4. **Attends la fin** (~2 minutes)

✅ Terminé ! L'outil est installé.

---

### **Option 2 : Manuel (si le script ne marche pas)**

1. **Ouvre Command Prompt EN ADMINISTRATEUR**
   - Appuie sur `Win + X`
   - Clique `Terminal (Admin)` ou `Cmd (Admin)`

2. **Va dans un dossier sans espaces** (exemple) :
   ```cmd
   cd C:\Dev
   ```
   
   OU créé un nouveau dossier :
   ```cmd
   mkdir C:\Dev
   cd C:\Dev
   ```

3. **Clone le projet** :
   ```cmd
   git clone https://github.com/Alexmarceauprevost812/source.git
   cd source
   ```

4. **Installe les dépendances** :
   ```cmd
   pip install -r requirements.txt
   ```
   
   (Ça prend ~1-2 minutes, c'est normal)

5. **Lance l'outil** :
   ```cmd
   python main.py
   ```

✅ L'outil démarre !

---

## 🎯 Lancer Outils 101 à chaque fois

### **Méthode 1 : Script (FACILE)**
- Double-clique sur `run.bat` → clic droit → `Exécuter en tant qu'administrateur`

### **Méthode 2 : Manuel**
1. Ouvre Command Prompt EN ADMINISTRATEUR
2. `cd C:\Dev\source` (ou ton dossier)
3. `python main.py`

---

## ❌ Erreurs Courantes & Solutions

### **Erreur 1 : "Python n'est pas reconnu"**
```
'python' n'est pas reconnu comme une commande interne ou externe
```
**Solution** :
- Réinstalle Python : https://www.python.org/downloads/
- ⚠️ COCHE "Add Python to PATH"
- **Redémarre ton PC**

---

### **Erreur 2 : "OSError: Npcap not installed"**
```
OSError: Npcap is not installed or not in the PATH
```
**Solution** :
- Installe Npcap : https://npcap.com/download/
- ⚠️ COCHE "Install Npcap in WinPcap API-compatible Mode"
- **Redémarre ton PC**

---

### **Erreur 3 : "No module named 'scapy'"**
```
ModuleNotFoundError: No module named 'scapy'
```
**Solution** :
```cmd
pip install scapy requests
```

---

### **Erreur 4 : "Access denied" ou "Permission denied"**
```
PermissionError: [Errno 13] Permission denied
```
**Solution** :
- Lance toujours Command Prompt EN ADMINISTRATEUR
- Appuie sur `Win + X` → `Terminal (Admin)`

---

### **Erreur 5 : "Git n'est pas installé"**
```
'git' n'est pas reconnu
```
**Solution** :
- Installe Git : https://git-scm.com/download/win
- **Redémarre ton PC**

---

## 🧪 Vérifier que tout marche

### **Test 1 : Python**
```cmd
python --version
```
Doit afficher : `Python 3.8.0` (ou plus récent)

### **Test 2 : Scapy**
```cmd
python -c "import scapy; print('OK')"
```
Doit afficher : `OK`

### **Test 3 : Npcap**
```cmd
npcap-config --version
```
Doit afficher un numéro de version

Si tout affiche `OK` → tu es prêt ! 🎉

---

## 🚀 Premiers pas avec Outils 101

Une fois lancé (`python main.py`), tu verras ce menu :

```
╔════════════════════════════════════════════════════════════╗
║        OUTILS 101 - Audit Réseau WiFi                     ║
║        Votre Assistant de Sécurité Locale                  ║
╚════════════════════════════════════════════════════════════╝

1. 🔍 Scanner le réseau (voir les appareils connectés)
2. 📋 Voir les appareils connus
3. 🏷️  Renommer un appareil
4. 🔓 Scanner les ports ouverts
... (18 options en tout)
```

**Recommandation d'ordre** :
1. Option **1** → Scanner ton réseau (voir qui est connecté)
2. Option **16** → Auditer la sécurité WiFi (WPA2/WPA3)
3. Option **20** → Compliance check (score de sécurité)

---

## 💡 Conseils Utiles

- **Lance TOUJOURS en admin** (certains outils réseau le demandent)
- **Le premier scan prend ~30 secondes** (c'est normal)
- **Les logs se sauvegardent** dans `logs/` automatiquement
- **Tu peux quitter anytime** avec `Ctrl + C`

---

## 📞 Aide Supplémentaire

Si tu as toujours un problème :

1. **Copie l'erreur exacte** (en rouge) en entière
2. **Dis-moi** :
   - Ton système (Windows 11 64-bit ?)
   - La version Python (`python --version`)
   - La version Npcap (`npcap-config --version`)

Je vais te fixer ça ! 🐧💪

---

## 🎊 Installation Réussie !

Bravo ! Tu as **Outils 101** prêt à l'emploi sur Windows 11.

Maintenant tu peux :
- 🔍 Scanner ton WiFi
- 🍯 Déployer des honeypots
- 🔬 Faire de la forensics
- ✅ Vérifier ta compliance de sécurité
- ... et 17 autres trucs !

**Lance l'outil et explore** : `python main.py` 🚀
