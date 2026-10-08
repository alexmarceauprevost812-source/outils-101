# 🤝 Contribution Guide - Outils 101

Merci de vouloir contribuer à Outils 101! Ce projet est un outil open source pour la surveillance et l'audit de réseaux WiFi locaux.

## 📋 Avant de Commencer

- **Lis** le README.md pour comprendre le projet
- **Vérifie** que tu utilises Python 3.7+
- **Teste** ton code avant de proposer une pull request
- **Suis** les conventions de code du projet

---

## 🎯 Types de Contributions Bienvenues

### 🐛 Signaler un bug
1. Va dans "Issues" sur GitHub
2. Clique "New Issue"
3. Titre clair : `[BUG] Nom du problème`
4. Description détaillée :
   - Version Python
   - Système d'exploitation
   - Étapes pour reproduire
   - Message d'erreur exact

Exemple :
```
[BUG] Scanner ne fonctionne pas sur Windows 11

- Python : 3.10.5
- OS : Windows 11 Pro
- Étapes :
  1. Ouvre main.py
  2. Choix : 1
  3. Valide le réseau proposé

Erreur :
```
Traceback (most recent call last):
  File "scapy_error.py", line 12, in <module>
    scapy.all import ARP
```

### ✨ Proposer une nouvelle fonctionnalité
1. "New Issue" → `[FEATURE] Nom de la fonctionnalité`
2. Explique clairement le besoin :
   - Quel problème ça résout
   - Cas d'usage
   - Exemple d'utilisation
   - Impact sur les perfs

Exemple :
```
[FEATURE] Exporter en CSV

Actuellement, seuls HTML/JSON sont supportés.
CSV serait utile pour :
- Importation dans Excel
- Analyses statistiques
- Rapports mensuels

Cas d'usage :
  Choix : 13 → CSV
  Exporte : devices.csv, alerts.csv, etc.
```

### 📖 Améliorer la documentation
- Corrige les typos/erreurs dans README.md
- Améliore les explications
- Ajoute des exemples
- Propose des guides nouveaux

### 🧪 Améliorer les tests
- Propose des tests unitaires
- Améliore `test_installation.py`
- Ajoute des tests d'intégration

---

## 📝 Code Style & Conventions

### Nommage
```python
# ✅ BON
def scan_wifi_networks():
class MACSpoofer:
DANGEROUS_PORTS = {23: "Telnet", ...}
max_history_entries = 1000

# ❌ MAUVAIS
def scanWifi():
class macspoofer:
dangerous_ports = {23: "Telnet"}
max-history-entries = 1000
```

### Docstrings
```python
# ✅ BON
def generate_report(devices, alerts):
    """
    Génère un rapport HTML complet.
    
    Args:
        devices (list): Liste des appareils détectés
        alerts (list): Alertes générées
    
    Returns:
        str: Chemin du fichier HTML généré
    """
    pass

# ❌ MAUVAIS
def generate_report(devices, alerts):
    pass
```

### Logging
```python
# ✅ BON
print("✅ Scan terminé")
print(f"🔴 Alerte : {issue['risk']}")
print("\n📊 Résumé :")

# ❌ MAUVAIS
print("ok")
print("error: " + str(issue))
print("")
```

### Format de code
```python
# ✅ BON
if len(devices) > 10:
    for device in devices:
        process_device(device)

issues = [i for i in all_issues if "CRITICAL" in i.get("risk", "")]

# ❌ MAUVAIS
if len(devices)>10:
    for d in devices:process_device(d)

issues=[i for i in all_issues if "CRITICAL" in i.get("risk","")]
```

---

## 🔀 Comment Faire une Pull Request

### Étape 1 : Fork le projet
1. Va sur GitHub
2. Clique "Fork" en haut à droite
3. Choisis ton compte

### Étape 2 : Clone ton fork
```bash
git clone https://github.com/TON_USERNAME/outils101.git
cd outils101
```

### Étape 3 : Crée une branche
```bash
git checkout -b feature/nom-de-la-fonctionnalite
# Ou pour un bug :
git checkout -b bugfix/nom-du-bug
```

### Étape 4 : Fais tes changements
```bash
# Modifie les fichiers
nano outils101/cli.py
# etc.
```

### Étape 5 : Teste
```bash
# Lance les tests
python3 test_installation.py

# Lance l'outil
sudo python3 main.py
# Test tes changements manuellement
```

### Étape 6 : Commit
```bash
git add .
git commit -m "[FEATURE] Ajoute export CSV pour les rapports"
# Ou
git commit -m "[BUG FIX] Corrige crash scanner sur Windows 11"
```

### Étape 7 : Push
```bash
git push origin feature/nom-de-la-fonctionnalite
```

### Étape 8 : Pull Request
1. Va sur ton fork GitHub
2. Clique "New Pull Request"
3. Remplis le template :

```markdown
## Description
Ajoute l'export CSV pour les rapports HTML.

## Motivation
Les utilisateurs demandaient l'export en CSV pour
les analyses statistiques.

## Changements
- Ajoute fonction `export_to_csv()` dans report_generator.py
- Ajoute option 13b au menu CLI
- Crée dossier exports/ pour les CSV

## Vérification
- ✅ Code testéé sur Linux
- ✅ Pas de dépendances nouvelles
- ✅ Documentation mise à jour

Fixes: #123
```

---

## 🎨 Types de Fichiers

### Outils Principaux (`outils101/*.py`)
- Chaque outil = 1 fichier
- Classe avec méthodes publiques + privées
- Docstrings complètes
- Gestion d'erreurs robuste

### CLI (`outils101/cli.py`)
- Menu principal
- Fonctions `action_*()` pour chaque option
- Importation des outils nécessaires
- Gestion utilisateur interactive

### Documentation
- `README.md` : Guide complet
- `QUICKSTART.md` : Premiers pas
- `INSTALLATION.md` : Installation détaillée
- `CHANGELOG.md` : Historique des versions
- `CONTRIBUTING.md` : Ce fichier

### Config
- `requirements.txt` : Dépendances
- `config_example.json` : Configuration exemple
- `.gitignore` : Fichiers à ignorer

---

## ✅ Checklist Avant de Soumettre

- [ ] Mon code suit les conventions du projet
- [ ] J'ai testé manuellement
- [ ] `test_installation.py` passe
- [ ] Pas d'erreur console
- [ ] Pas de dépendances supplémentaires
- [ ] J'ai mis à jour la documentation
- [ ] Mon commit message est clair
- [ ] Je n'ai modifié que les fichiers nécessaires

---

## 🚀 Petites Contributions Rapides

### Corriger une typo
```bash
git checkout -b typo/correction-readme
# Modifie README.md
git add README.md
git commit -m "[DOC] Corrige typo dans README"
git push origin typo/correction-readme
# → Pull Request
```

### Ajouter un exemple
```bash
git checkout -b docs/exemple-csv-export
# Modifie README.md ou QUICKSTART.md
# Ajoute un exemple d'export CSV
git commit -m "[DOC] Ajoute exemple export CSV"
# → Pull Request
```

### Améliorer les logs
```bash
git checkout -b enhancement/meilleurs-logs
# Améliore les messages print()
git commit -m "[ENHANCEMENT] Améliore readabilité des logs"
# → Pull Request
```

---

## 🧪 Testing

### Lancer les tests
```bash
python3 test_installation.py
```

### Ajouter un test
```python
# Dans test_installation.py
def test_my_feature():
    """Teste la nouvelle fonctionnalité."""
    print("🔍 Test X : Description")
    
    try:
        # Ton test ici
        result = my_function()
        assert result is not None
        print("   ✅ OK")
        return True
    except Exception as e:
        print(f"   ❌ {e}")
        return False
```

### Test manuel
```bash
sudo python3 main.py
# Choix : teste ta nouvelle fonctionnalité
# Vérifie que ça marche et pas d'erreurs
```

---

## 📚 Ressources Utiles

- **Scapy docs** : https://scapy.readthedocs.io/
- **Requests docs** : https://requests.readthedocs.io/
- **Python PEP 8** : https://pep8.org/
- **Markdown guide** : https://www.markdownguide.org/

---

## 🎓 Qu'on Cherche

### Contributeurs Bienvenues Pour
- ✅ Améliorer les perfs
- ✅ Support macOS/ARM64
- ✅ GUI graphique (tkinter/Qt)
- ✅ Web interface (Flask/Django)
- ✅ Plugins système
- ✅ Base de données vulnérabilités
- ✅ Notifications en temps réel
- ✅ Tests unitaires

---

## ⚖️ Licence

En contribuant, tu acceptes que ton code soit sous licence open source comme le reste du projet.

---

## 🤖 Aide de la Communauté

- **Slack/Discord** : (À ajouter)
- **Issues** : Pour signaler des bugs
- **Discussions** : Pour des questions
- **Wikis** : Pour de la documentation

---

## 🙏 Merci!

Merci de contribuer à Outils 101! Chaque contribution compte, même les petites corrections.

**Happy coding! 🐧🌀**
