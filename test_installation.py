#!/usr/bin/env python3
"""
Script de test d'installation - Outils 101
Vérifie que toutes les dépendances sont correctement installées.
"""

import sys
import os
from pathlib import Path

def test_python_version():
    """Vérifie la version de Python."""
    print("🔍 Test 1 : Version Python")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} trop ancien (3.7+ requis)")
        return False

def test_imports():
    """Teste l'import des modules Outils 101."""
    print("\n🔍 Test 2 : Import des modules")
    
    modules = [
        "outils101.scanner",
        "outils101.portscan",
        "outils101.vendor",
        "outils101.storage",
        "outils101.automation",
        "outils101.dnslookup",
        "outils101.geoip",
        "outils101.ssl_audit",
        "outils101.banner",
        "outils101.vulndb",
        "outils101.wifiaudit",
        "outils101.cli",
        "outils101.report_generator",
        "outils101.traffic_monitor",
        "outils101.mac_spoofing_detector",
        "outils101.wifi_security_audit",
        "outils101.intrusion_detection",
    ]
    
    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module} - {e}")
            all_ok = False
    
    return all_ok

def test_dependencies():
    """Teste les dépendances externes."""
    print("\n🔍 Test 3 : Dépendances externes")
    
    deps = {
        "scapy": "Scan ARP",
        "requests": "Géolocalisation IP",
    }
    
    all_ok = True
    for dep, description in deps.items():
        try:
            __import__(dep)
            print(f"   ✅ {dep:<15} ({description})")
        except ImportError:
            print(f"   ❌ {dep:<15} ({description}) - NON INSTALLÉ")
            print(f"      Installe avec : pip install {dep}")
            all_ok = False
    
    return all_ok

def test_file_structure():
    """Teste la structure des fichiers."""
    print("\n🔍 Test 4 : Structure des fichiers")
    
    required_files = [
        "main.py",
        "README.md",
        "requirements.txt",
        "outils101/__init__.py",
        "outils101/cli.py",
        "outils101/scanner.py",
        "outils101/report_generator.py",
        "outils101/traffic_monitor.py",
        "outils101/mac_spoofing_detector.py",
        "outils101/wifi_security_audit.py",
        "outils101/intrusion_detection.py",
    ]
    
    all_ok = True
    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MANQUANT")
            all_ok = False
    
    return all_ok

def test_directories():
    """Teste/crée les répertoires nécessaires."""
    print("\n🔍 Test 5 : Répertoires")
    
    directories = ["logs", "reports", "exports", "threats"]
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"   ✅ {dir_name}/ (existe)")
        else:
            try:
                dir_path.mkdir(exist_ok=True)
                print(f"   ✅ {dir_name}/ (créé)")
            except Exception as e:
                print(f"   ❌ {dir_name}/ - {e}")
                return False
    
    return True

def test_permissions():
    """Teste les permissions d'écriture."""
    print("\n🔍 Test 6 : Permissions d'écriture")
    
    test_file = Path("test_write.tmp")
    try:
        test_file.write_text("test")
        test_file.unlink()
        print(f"   ✅ Écriture dans le répertoire courant OK")
        return True
    except Exception as e:
        print(f"   ❌ Problème d'écriture : {e}")
        return False

def test_cli_launch():
    """Teste le lancement du CLI."""
    print("\n🔍 Test 7 : Lancement du CLI")
    
    try:
        from outils101 import cli
        print(f"   ✅ CLI chargé avec succès")
        return True
    except Exception as e:
        print(f"   ❌ Erreur CLI : {e}")
        return False

def main():
    """Lance tous les tests."""
    print("=" * 70)
    print("🧪 TEST D'INSTALLATION - OUTILS 101")
    print("=" * 70)
    
    results = {
        "Python version": test_python_version(),
        "Imports modules": test_imports(),
        "Dépendances": test_dependencies(),
        "Structure fichiers": test_file_structure(),
        "Répertoires": test_directories(),
        "Permissions": test_permissions(),
        "CLI": test_cli_launch(),
    }
    
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    print("=" * 70)
    print(f"Résultat: {passed}/{total} tests passés")
    
    if passed == total:
        print("\n🎉 TOUT EST OK! Tu peux lancer Outils 101:")
        print("   sudo python3 main.py    (Linux/macOS)")
        print("   python main.py          (Windows en Admin)")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) échoué(s). Consulte les erreurs ci-dessus.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
