# 🛡️ Guide Affichage des Logos - Outils 101

## 🚀 Au Démarrage (Terminal)

Quand tu lances l'application :

```bash
python main.py      # Windows (Admin)
sudo python3 main.py # Linux
python3 main.py     # macOS
```

**Tu verras automatiquement** :

1. **Logo ASCII art** avec épées et bouclier
2. **Message de bienvenue**
3. **Menu avec 21 options**

---

## 🌐 Voir le Logo Interactif (Navigateur)

### 📱 **Avec Animations**

Double-clique sur **`logo.html`** (dans le dossier du projet)

**OU** ouvre-le dans un navigateur :

```bash
# Windows
start logo.html

# Linux
xdg-open logo.html

# macOS
open logo.html
```

**Tu verras** :
- ⚔️ Épées qui se balancent (left & right)
- 🛡️ Bouclier au centre qui pulse (émet une lumière)
- Couleurs vertes (cybersécurité)
- Animations fluides et professionnelles

---

## 🎨 Logo Vectoriel (Éditable)

### 📊 **Format SVG**

Double-clique sur **`logo.svg`** (dans le dossier du projet)

**OU** ouvre-le dans un navigateur ou logiciel de design :

```bash
# Navigateur (tous les OS)
Ouvre le navigateur → Drag & drop logo.svg

# Inkscape (libre, tous les OS)
# Télécharge : https://inkscape.org
# Puis : File → Open → logo.svg

# Affinity Designer (payant, macOS/Windows)
# Adobe Illustrator (payant, tous les OS)
```

**Avantages du SVG** :
- ✅ Redimensionnable sans perte de qualité
- ✅ Éditable (change les couleurs, le texte)
- ✅ Utilisable partout (web, PDF, impression)

---

## 📋 Fichiers Logos & Où les Trouver

| Fichier | Chemin | Type | Ouverture |
|---------|--------|------|-----------|
| **ASCII** | Terminal automatique | Texte | `python main.py` |
| **HTML** | `logo.html` | Navigateur | Double-clique |
| **SVG** | `logo.svg` | Éditeur/Navigateur | Double-clique |
| **Code** | `outils101/banner_new.py` | Python | Éditeur texte |

---

## 💡 Utilisations Pratiques

### 1️⃣ **Tu veux voir le logo en direct**
```bash
python main.py  # S'affiche au démarrage
```
👉 **Résultat** : ASCII art + menu interactif

---

### 2️⃣ **Tu veux une présentation visuelle (réunion, présentation)**
```bash
double-clique sur logo.html
```
👉 **Résultat** : Beau, animé, professionnel
📱 Partageables par email ou web

---

### 3️⃣ **Tu veux éditer le logo**
```bash
Ouvre Inkscape + logo.svg
OU
Ouvre logo.html dans VS Code et modifie le CSS
```
👉 **Résultat** : Personnalisation complète

---

### 4️⃣ **Tu veux l'utiliser dans ta documentation**
```bash
- Utilise logo.svg pour web (scalable)
- Exporte logo.svg en PNG haute résolution
- Copie le code HTML de logo.html
```
👉 **Résultat** : Intégrable partout

---

## 🎯 Symboles & Significations

```
        ⚔️ ← Épée Gauche (Attaques détectées)
         |
    _____|____
   /   🛡️    \  ← Bouclier (Protection)
  |  DÉFENSE  |
   \   101   /
    \       /
     ╰─────╯
         |
        ⚔️ ← Épée Droite (Forensics)
```

**Signification globale** : **Défense active et proactive du réseau**

---

## ⚙️ Personnalisation

### 🎨 Changer les Couleurs

#### HTML (logo.html)
```css
/* Trouve la section <style> */
.shield {
    background: linear-gradient(135deg, #00ff88 0%, #00cc6f 100%);
    /* Remplace par tes couleurs */
    /* Ex: #ff5500 pour orange, #0066ff pour bleu */
}
```

#### Terminal (banner_new.py)
```python
# Change les caractères et emojis
# Ex: 🛡️ → 🔰 ou ⚔️ → ⚒️
```

---

## 📊 Comparaison des Formats

| Critère | ASCII | HTML | SVG |
|---------|-------|------|-----|
| Affichage | Terminal | Navigateur | Navigateur/Éditeur |
| Animations | ❌ | ✅ | ✅ |
| Éditable | ✅ (simple) | ✅ (CSS) | ✅ (XML) |
| Résolution | Fixe | Adaptative | Scalable |
| Taille | Très petit | Petit | Très petit |
| Mobile | ✅ (terminal) | ✅ | ✅ |
| Impression | ❌ | ✅ | ✅ |

---

## 🚀 Cas d'Usage

### 🏠 **Chez toi (protection réseau)**
- Lance `python main.py` → Voir le logo + menu
- Scanner ton WiFi
- Installer sur Windows/Linux

### 🏢 **En entreprise (pentest)**
- Utilise `logo.html` pour présentation client
- Export `logo.svg` pour rapport professionnel
- ASCII dans les logs de scanning

### 📚 **Documentation/Présentation**
- Utilise `logo.html` pour slides
- Intègre `logo.svg` dans docs PDF
- Copie ASCII pour fichiers texte

### 🌐 **Site Web**
- Utilise `logo.svg` (vectoriel)
- Intègre le HTML directement
- Optimise les couleurs pour ton thème

---

## 🔧 Troubleshooting

### ❌ Logo.html ne s'ouvre pas
**Solution 1** : Double-clique dessus
**Solution 2** : Drag & drop dans navigateur
**Solution 3** : `start logo.html` dans CMD

### ❌ Logo ne montre pas d'animations
**Cause** : Vieux navigateur
**Solution** : Mets à jour Chrome/Firefox/Safari

### ❌ ASCII art déformé dans terminal
**Cause** : Terminal trop petit ou vieille version
**Solution** : Agrandis la fenêtre ou utilise `logo.html`

### ❌ SVG ne s'édite pas
**Solution** : Utilise Inkscape (gratuit) au lieu de Notepad

---

## 📞 Support

Si les logos ne s'affichent pas :

1. Vérifie que les fichiers existent :
   - `outils101/banner_new.py` ✅
   - `logo.html` ✅
   - `logo.svg` ✅

2. Relance l'application :
   ```bash
   python main.py
   ```

3. Si encore problème : cherche "AIDE_EMERGENCY.txt"

---

## 🎉 Résumé

| Action | Commande | Résultat |
|--------|----------|----------|
| Voir logo (terminal) | `python main.py` | ASCII + Menu |
| Voir logo (navigateur) | Double-clique `logo.html` | Beau, animé |
| Éditer logo (couleurs) | Ouvre `logo.html` dans VS Code | Personnalisé |
| Utiliser logo (web) | Copie `logo.svg` | Intégrable partout |

---

**Enjoy ton logo défensif! 🛡️⚔️**

*Outils 101 v3.0 - Logo Défense Réseau*
