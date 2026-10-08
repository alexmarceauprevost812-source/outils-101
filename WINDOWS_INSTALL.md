# 🪟 Guide Installation Outils 101 sur Windows 11

## ⚠️ Problèmes Courants & Solutions

---

## **PROBLÈME 1 : Espace dans le chemin d'utilisateur**

### ❌ Ça ne marche PAS :
```
cd C:\Users\alex marceau\Desktop
```

### ✅ SOLUTIONS :

#### **Option A : Utilise des guillemets** (plus facile)
```cmd
cd "C:\Users\alex marceau\Desktop"
```

#### **Option B : Utilise le chemin court DOS**
```cmd
# Voir le chemin court
dir /X

# Exemple de résultat : C:\Users\ALEXMA~1\Desktop
cd C:\Users\ALEXMA~1\Desktop
```

#### **Option C : Clone ailleurs sans espaces** (recommandé)
```cmd
cd C:\Dev
git clone https://github.com/username/outils101.git
cd outils101
```

---

## **PROBLÈME 2 : Npcap Manquant** ⚠️

### ❌ Erreur typique :
```
ERROR: Npcap is not installed or is not in PATH
```

### ✅ FIX : Installe Npcap

**Étape 1 : Télécharge Npcap**
- Va sur : https://npcap.com/download/
- Télécharge la dernière version (`.exe`)

**Étape 2 : Installe Npcap**
- Double-clique sur le fichier téléchargé
- ✅ **IMPORTANT** : Cochez cette option lors de l'installation :
  - `[✓] Install Npcap in WinPcap API-compatible Mode`
- Redémarre l'ordi

**Étape 3 : Vérifie l'installation**
```cmd
# Devrait afficher la version
npcap-config --version
```

---

## **ÉTAPES COMPLÈTES WINDOWS 11**

### **1. Prépare le dossier**
```cmd
# Ouvre Command Prompt (cmd.exe) en tant qu'ADMINISTRATEUR
# (Clique droit sur cmd → Exécuter en tant qu'administrateur)

# Va sur le Bureau
cd "C:\Users\alex marceau\Desktop"

# Ou crée un dossier sans espaces
mkdir C:\Dev
cd C:\Dev
```

### **2. Clone le projet**
```cmd
# Si tu as Git installé
git clone https://github.com/username/outils101.git
cd outils101

# Sinon, télécharge le ZIP et extrais-le ici
```

### **3. Installe Npcap** (OBLIGATOIRE)
```cmd
# Va sur https://npcap.com/download/
# Télécharge et installe l'exe
# Redémarre l'ordi après !
```

### **4. Installe Python (si pas encore)**
```cmd
# Télécharge Python 3.10+ depuis python.org
# ✅ IMPORTANT : Cochez "Add Python to PATH" lors de l'installation

# Vérifie
python --version
```

### **5. Installe les dépendances**
```cmd
# Reste en administrateur (IMPORTANT!)
pip install -r requirements.txt

# Ou spécifiquement
pip install scapy requests
```

### **6. Lance l'outil** ✅
```cmd
# Reste en administrateur
python main.py

# Tu dois voir le menu 👇
```

---

## **Menu Principal (tu devrais voir ceci)**

```
=== Outils 101 - Audit Réseau ===
1. Scanner le réseau (ARP scan)
2. Voir les appareils enregistrés
3. Renommer un appareil
4. Scanner les ports ouverts
5. Auditer un appareil (vulnérabilités)
6. Auditer la sécurité WiFi
7. DNS Reverse Lookup
8. Géolocalisation d'IP
9. Audit SSL/TLS
10. Automatisation (scan continu)
[...]
20. Compliance Check
21. Quitter

Choix :
```

---

## **⚡ QUICK FIX : Si ça marche pas encore**

### **Erreur 1 : "python not found"**
```cmd
# Python n'est pas dans PATH
# Solution : réinstalle Python en cochant "Add Python to PATH"
```

### **Erreur 2 : "Npcap is not installed"**
```cmd
# Npcap manquant ou mal installé
# Solution : https://npcap.com/download/ puis redémarre
```

### **Erreur 3 : "Access Denied"**
```cmd
# Tu n'es pas en administrateur
# Solution : Ouvre cmd en cliquant droit → "Exécuter en tant qu'administrateur"
```

### **Erreur 4 : "ModuleNotFoundError: scapy"**
```cmd
# Les dépendances ne sont pas installées
# Solution :
pip install --upgrade pip
pip install -r requirements.txt
```

### **Erreur 5 : "Port already in use" (Honeypot)**
```cmd
# Le port est déjà utilisé
# Solution : change le port dans config_example.json
```

---

## **✅ Test Rapide**

Une fois installé, teste comme ceci :

```cmd
python main.py

# Appuie sur 1 (Scanner le réseau)
# Tu devrais voir ton réseau local

# Appuie sur 20 (Compliance Check)
# Tu devrais voir un score de sécurité
```

---

## **🎯 Chemins Importants Windows**

| Élément | Chemin |
|---------|--------|
| Dossier projet | `C:\Dev\outils101` |
| Python | `C:\Users\alex marceau\AppData\Local\Programs\Python\Python311` |
| Npcap | `C:\Program Files\Npcap` |
| Logs générés | `C:\Dev\outils101\logs\` |
| Config | `C:\Dev\outils101\config_example.json` |

---

## **📱 Alternative : PowerShell (plus moderne)**

Si Command Prompt ne marche pas, utilise **PowerShell** :

```powershell
# Ouvre PowerShell en admin (clique droit → "Exécuter en tant qu'administrateur")

cd "C:\Users\alex marceau\Desktop"
python main.py
```

---

## **🆘 Besoin d'aide ?**

Si ça marche toujours pas :

1. Donne-moi l'**erreur exacte** (copie-colle le message rouge)
2. Dis-moi la version de Windows (`winver`)
3. Dis-moi si Npcap est bien installé (`npcap-config --version`)

Ensuite on debug ensemble ! 🐧💪

---

## **✨ Une fois ça marche...**

```cmd
# Teste chaque feature
python main.py

Menu 1  → Scanner réseau
Menu 6  → Audit WiFi
Menu 18 → Honeypot (piège à attaquants)
Menu 20 → Compliance (score sécurité)
Menu 21 → Quitter
```

**Bonne chance ! 🚀**
