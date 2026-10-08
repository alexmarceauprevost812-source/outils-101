# ============================================
# Outils 101 - Installation PowerShell Windows 11
# ============================================
# Lance ce script EN ADMINISTRATEUR
# ============================================

# Couleurs
$Green = [System.ConsoleColor]::Green
$Red = [System.ConsoleColor]::Red
$Yellow = [System.ConsoleColor]::Yellow

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   OUTILS 101 - Installation Windows 11 (PowerShell)        ║" -ForegroundColor Cyan
Write-Host "║   Lance ce script EN ADMINISTRATEUR                        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Vérifie si lancé en admin
$IsAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $IsAdmin) {
    Write-Host "[ERREUR] Ce script doit être lancé EN ADMINISTRATEUR !" -ForegroundColor $Red
    Write-Host ""
    Write-Host "Solution :"
    Write-Host "1. Ouvre PowerShell EN ADMINISTRATEUR"
    Write-Host "2. Lance : Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
    Write-Host "3. Puis relance ce script"
    Write-Host ""
    Read-Host "Appuie sur Entrée pour quitter"
    exit 1
}

Write-Host "[OK] Lancé en tant qu'administrateur" -ForegroundColor $Green
Write-Host ""

# ÉTAPE 1 : Vérifier Python
Write-Host "[ÉTAPE 1/5] Vérification de Python..." -ForegroundColor Cyan
$PythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERREUR] Python n'est pas installé ou pas dans PATH" -ForegroundColor $Red
    Write-Host ""
    Write-Host "Télécharge Python : https://www.python.org/downloads/" -ForegroundColor $Yellow
    Write-Host "✅ Pendant l'installation, COCHE 'Add Python to PATH'" -ForegroundColor $Yellow
    Write-Host ""
    Read-Host "Appuie sur Entrée pour quitter"
    exit 1
}
Write-Host "[OK] $PythonVersion trouvé" -ForegroundColor $Green

# ÉTAPE 2 : Vérifier Npcap
Write-Host ""
Write-Host "[ÉTAPE 2/5] Vérification de Npcap..." -ForegroundColor Cyan
$Npcap = Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Where {$_.DisplayName -like "*Npcap*"}

if (-not $Npcap) {
    Write-Host "[ATTENTION] Npcap n'est pas installé" -ForegroundColor $Yellow
    Write-Host ""
    Write-Host "Npcap est OBLIGATOIRE pour scanner le réseau !" -ForegroundColor $Yellow
    Write-Host "Télécharge-le : https://npcap.com/download/" -ForegroundColor $Yellow
    Write-Host ""
    Write-Host "✅ Pendant l'installation :" -ForegroundColor $Yellow
    Write-Host "   - Coche 'Install Npcap in WinPcap API-compatible Mode'" -ForegroundColor $Yellow
    Write-Host "   - Redémarre ton PC après" -ForegroundColor $Yellow
    Write-Host ""
    
    $Confirm = Read-Host "Continuer sans Npcap ? (O/N)"
    if ($Confirm -eq "N") { exit 1 }
} else {
    Write-Host "[OK] Npcap trouvé" -ForegroundColor $Green
}

# ÉTAPE 3 : Cloner le repo
Write-Host ""
Write-Host "[ÉTAPE 3/5] Clonage du repository..." -ForegroundColor Cyan

$GitVersion = git --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERREUR] Git n'est pas installé" -ForegroundColor $Red
    Write-Host "Télécharge Git : https://git-scm.com/download/win" -ForegroundColor $Yellow
    Read-Host "Appuie sur Entrée pour quitter"
    exit 1
}

if (Test-Path "source") {
    Write-Host "[OK] Dossier 'source' existe déjà" -ForegroundColor $Green
} else {
    Write-Host "Clonage en cours..." -ForegroundColor Cyan
    git clone https://github.com/Alexmarceauprevost812/source.git
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERREUR] Impossible de cloner le repo" -ForegroundColor $Red
        Read-Host "Appuie sur Entrée pour quitter"
        exit 1
    }
    Write-Host "[OK] Repository cloné" -ForegroundColor $Green
}

Set-Location source
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERREUR] Impossible d'entrer dans le dossier" -ForegroundColor $Red
    Read-Host "Appuie sur Entrée pour quitter"
    exit 1
}

# ÉTAPE 4 : Installer les dépendances
Write-Host ""
Write-Host "[ÉTAPE 4/5] Installation des dépendances Python..." -ForegroundColor Cyan
Write-Host "Cette étape peut prendre 1-2 minutes..." -ForegroundColor Yellow
Write-Host ""

pip install --upgrade pip | Out-Null
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERREUR] Erreur lors de l'installation des dépendances" -ForegroundColor $Red
    Write-Host "Essaie manuellement : pip install scapy requests" -ForegroundColor $Yellow
    Read-Host "Appuie sur Entrée pour quitter"
    exit 1
}
Write-Host "[OK] Dépendances installées" -ForegroundColor $Green

# ÉTAPE 5 : Tester
Write-Host ""
Write-Host "[ÉTAPE 5/5] Test de l'installation..." -ForegroundColor Cyan
python -c "import scapy; import requests; print('[OK] Tous les modules chargés')" 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Test réussi !" -ForegroundColor $Green
} else {
    Write-Host "[ATTENTION] Certains modules pourraient ne pas être chargés" -ForegroundColor $Yellow
}

# FIN
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   INSTALLATION TERMINÉE ! ✅                               ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pour lancer Outils 101, tape :" -ForegroundColor Cyan
Write-Host ""
Write-Host "    python main.py" -ForegroundColor $Yellow
Write-Host ""
Write-Host "⚠️  IMPORTANT : Lance toujours en ADMINISTRATEUR" -ForegroundColor $Yellow
Write-Host ""
Read-Host "Appuie sur Entrée pour quitter"
