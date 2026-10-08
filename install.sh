#!/bin/bash
# Script d'installation automatique pour Outils 101 (Linux/macOS)

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🛡️  OUTILS 101 - Script d'Installation Automatique        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Vérifier si on est root
if [ "$EUID" -ne 0 ]; then 
  echo -e "${RED}✗ Ce script doit être lancé avec sudo${NC}"
  echo "  Utilise : sudo bash install.sh"
  exit 1
fi

echo -e "${BLUE}Étape 1/5 : Vérification du système...${NC}"

# Vérifier le système d'exploitation
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  OS="linux"
  echo -e "${GREEN}✓ Système détecté : Linux${NC}"
elif [[ "$OSTYPE" == "darwin"* ]]; then
  OS="macos"
  echo -e "${GREEN}✓ Système détecté : macOS${NC}"
else
  echo -e "${RED}✗ Système non supporté : $OSTYPE${NC}"
  echo "  Outils 101 supporte : Linux, macOS, Windows"
  exit 1
fi

# Vérifier Python
echo ""
echo -e "${BLUE}Étape 2/5 : Vérification Python...${NC}"

if ! command -v python3 &> /dev/null; then
  echo -e "${RED}✗ Python 3 n'est pas installé${NC}"
  if [ "$OS" = "linux" ]; then
    echo "  Installe avec : sudo apt install python3 python3-pip"
  elif [ "$OS" = "macos" ]; then
    echo "  Installe avec : brew install python3"
  fi
  exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}' | cut -d. -f1,2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION trouvé${NC}"

# Vérifier pip
if ! command -v pip3 &> /dev/null; then
  echo -e "${RED}✗ pip3 n'est pas installé${NC}"
  if [ "$OS" = "linux" ]; then
    echo "  Installe avec : sudo apt install python3-pip"
  elif [ "$OS" = "macos" ]; then
    echo "  Installe avec : brew install pip3"
  fi
  exit 1
fi

echo -e "${GREEN}✓ pip3 trouvé${NC}"

# Installer les dépendances
echo ""
echo -e "${BLUE}Étape 3/5 : Installation des dépendances...${NC}"

if [ -f "requirements.txt" ]; then
  echo "  Installations scapy et requests..."
  pip3 install -q -r requirements.txt
  echo -e "${GREEN}✓ Dépendances installées${NC}"
else
  echo -e "${YELLOW}⚠ requirements.txt non trouvé${NC}"
fi

# Créer les répertoires
echo ""
echo -e "${BLUE}Étape 4/5 : Création des répertoires...${NC}"

mkdir -p logs reports exports threats
echo -e "${GREEN}✓ Répertoires créés${NC}"

# Lancer les tests
echo ""
echo -e "${BLUE}Étape 5/5 : Test d'installation...${NC}"

if [ -f "test_installation.py" ]; then
  echo ""
  python3 test_installation.py
  echo ""
else
  echo -e "${YELLOW}⚠ test_installation.py non trouvé${NC}"
fi

# Résumé final
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo -e "║  ${GREEN}✓ Installation terminée avec succès!${NC}                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo -e "${GREEN}Prochaines étapes:${NC}"
echo ""
echo "  1. Lance l'outil:"
echo -e "     ${YELLOW}sudo python3 main.py${NC}"
echo ""
echo "  2. Voir l'aide rapide:"
echo -e "     ${YELLOW}cat HELP.txt${NC}"
echo ""
echo "  3. Guide de démarrage rapide:"
echo -e "     ${YELLOW}cat QUICKSTART.md${NC}"
echo ""
echo "  4. Documentation complète:"
echo -e "     ${YELLOW}cat README.md${NC}"
echo ""

echo -e "${BLUE}Première utilisation recommandée:${NC}"
echo "  1. Choix : 1 (Scanner le réseau)"
echo "  2. Choix : 3 (Renommer tes appareils)"
echo "  3. Choix : 16 (Audit WiFi)"
echo "  4. Choix : 13 (Générer rapport HTML)"
echo ""

echo -e "${YELLOW}⚠️  Rappel important:${NC}"
echo "  Cet outil est à usage DÉFENSIF UNIQUEMENT"
echo "  À utiliser UNIQUEMENT sur TON propre réseau"
echo ""

echo -e "${GREEN}🐧🌀 Happy scanning!${NC}"
