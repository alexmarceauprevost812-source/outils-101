@echo off
REM ============================================
REM Outils 101 - Installation Windows 11
REM ============================================
REM Lance ce fichier EN ADMINISTRATEUR
REM ============================================

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   OUTILS 101 - Installation Windows 11                     ║
echo ║   Lance ce fichier EN ADMINISTRATEUR                       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Vérifie si lancé en admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERREUR] Ce script doit être lancé EN ADMINISTRATEUR !
    echo.
    echo Refais un clic droit sur ce fichier ^> Exécuter en tant qu'administrateur
    pause
    exit /b 1
)

echo [OK] Lancé en tant qu'administrateur
echo.

REM ============ ÉTAPE 1 : Vérifier Python ============
echo [ÉTAPE 1/5] Vérification de Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERREUR] Python n'est pas installé ou pas dans PATH
    echo.
    echo Télécharge Python : https://www.python.org/downloads/
    echo ✅ Pendant l'installation, COCHE "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION% trouvé

REM ============ ÉTAPE 2 : Vérifier Npcap ============
echo.
echo [ÉTAPE 2/5] Vérification de Npcap (pour scan réseau)...
wmic product list brief | find /i "npcap" >nul 2>&1
if %errorLevel% neq 0 (
    echo [ATTENTION] Npcap n'est pas installé
    echo.
    echo Npcap est OBLIGATOIRE pour scanner le réseau !
    echo Télécharge-le : https://npcap.com/download/
    echo.
    echo ✅ Pendant l'installation :
    echo    - Coche "Install Npcap in WinPcap API-compatible Mode"
    echo    - Redémarre ton PC après
    echo.
    choice /C YN /M "Continuer sans Npcap (certaines fonctions ne marcheront pas) ? (O/N)"
    if errorLevel 2 exit /b 1
) else (
    echo [OK] Npcap trouvé
)

REM ============ ÉTAPE 3 : Cloner le repo ============
echo.
echo [ÉTAPE 3/5] Clonage du repository...
git --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERREUR] Git n'est pas installé
    echo Télécharge Git : https://git-scm.com/download/win
    pause
    exit /b 1
)

if exist "source" (
    echo [OK] Dossier 'source' existe déjà
) else (
    echo Clonage en cours...
    git clone https://github.com/Alexmarceauprevost812/source.git
    if %errorLevel% neq 0 (
        echo [ERREUR] Impossible de cloner le repo
        echo Vérifie ta connexion internet et l'URL
        pause
        exit /b 1
    )
    echo [OK] Repository cloné
)

cd source
if %errorLevel% neq 0 (
    echo [ERREUR] Impossible d'entrer dans le dossier
    pause
    exit /b 1
)

REM ============ ÉTAPE 4 : Installer les dépendances ============
echo.
echo [ÉTAPE 4/5] Installation des dépendances Python...
echo Cette étape peut prendre 1-2 minutes...
echo.

pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt

if %errorLevel% neq 0 (
    echo [ERREUR] Erreur lors de l'installation des dépendances
    echo Essaie manuellement : pip install scapy requests
    pause
    exit /b 1
)
echo [OK] Dépendances installées

REM ============ ÉTAPE 5 : Tester l'installation ============
echo.
echo [ÉTAPE 5/5] Test de l'installation...
python -c "import scapy; import requests; print('[OK] Tous les modules chargés')" >nul 2>&1
if %errorLevel% neq 0 (
    echo [ATTENTION] Certains modules pourraient ne pas être chargés
    echo Essaie de relancer : pip install scapy requests
)

REM ============ FIN ============
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   INSTALLATION TERMINÉE ! ✅                               ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Pour lancer Outils 101, tape :
echo.
echo    python main.py
echo.
echo ⚠️  IMPORTANT : Lance toujours en ADMINISTRATEUR
echo.
pause
