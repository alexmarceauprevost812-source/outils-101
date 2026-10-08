@echo off
REM ============================================
REM Outils 101 - Lancer l'outil
REM ============================================
REM Lance ce fichier EN ADMINISTRATEUR
REM ============================================

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   OUTILS 101 - Démarrage                                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Vérifie si lancé en admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERREUR] Ce script doit être lancé EN ADMINISTRATEUR !
    echo.
    echo Solution :
    echo 1. Fais un clic droit sur ce fichier (run.bat)
    echo 2. Clique "Exécuter en tant qu'administrateur"
    echo.
    pause
    exit /b 1
)

echo [OK] Lancé en tant qu'administrateur
echo.

REM Vérifie Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERREUR] Python n'est pas installé
    echo Télécharge Python : https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Vérifie si dans le bon dossier
if not exist "main.py" (
    echo [ERREUR] main.py introuvable
    echo Assure-toi d'être dans le dossier "source"
    pause
    exit /b 1
)

echo [DÉMARRAGE] Outils 101...
echo.
python main.py

if %errorLevel% neq 0 (
    echo.
    echo [ERREUR] L'outil s'est arrêté avec une erreur
    pause
    exit /b 1
)
