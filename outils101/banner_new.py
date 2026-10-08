#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Banner Amélioré - Logos et bannières visuelles pour Outils 101
"""

def print_logo_ascii():
    """Affiche le logo ASCII art principal avec épées et bouclier"""
    logo = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║            ⚔️   OUTILS 101 CYBERSÉCURITÉ   ⚔️            ║
    ║                                                            ║
    ║                      Épée Gauche                           ║
    ║                           ⚔️                              ║
    ║                            |                              ║
    ║                        _____|____                          ║
    ║                       /   🛡️    \\                       ║
    ║                      |  DÉFENSE  |                        ║
    ║                       \\   101   /                        ║
    ║                        \\       /                          ║
    ║                         ╰─────╯                           ║
    ║                            |                              ║
    ║                            ⚔️                              ║
    ║                      Épée Droite                           ║
    ║                                                            ║
    ║                   ⚔️ LINUX • WINDOWS • macOS ⚔️          ║
    ║                                                            ║
    ║              Surveillance • Audit • Détection             ║
    ║                    d'Intrusions Réseau                    ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(logo)


def print_welcome_banner():
    """Bannière de bienvenue avec explications"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║  ⚔️  BIENVENUE DANS OUTILS 101 - ÉDITION DÉFENSIVE  ⚔️       ║
    ║                                                               ║
    ║  🛡️ BOUCLIER = Protection de ton réseau WiFi               ║
    ║  ⚔️ ÉPÉE GAUCHE = Détection d'intrusions (IDS)             ║
    ║  ⚔️ ÉPÉE DROITE = Forensics & Honeypot                     ║
    ║                                                               ║
    ║  Outils 100% LÉGAUX • Défensifs • Éthiques                  ║
    ║  À utiliser sur TON PROPRE RÉSEAU                           ║
    ║                                                               ║
    ║  Choisis une option ci-dessous pour commencer →              ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu_header():
    """En-tête du menu principal"""
    header = """
    ┌───────────────────────────────────────────────────────┐
    │  🛡️ MENU PRINCIPAL - OUTILS 101 v3.0 DÉFENSIF         │
    │                                                       │
    │  ⚔️ ÉPÉE GAUCHE  │  🛡️ BOUCLIER  │  ⚔️ ÉPÉE DROITE  │
    │  Intrusions    │  Réseau WiFi  │  Forensics      │
    │                                                       │
    └───────────────────────────────────────────────────────┘
    """
    print(header)


def print_section_header(title):
    """En-tête de section avec décoration"""
    header = f"""
    ╭─────────────────────────────────────────────╮
    │  🛡️ {title.upper().center(39)} 🛡️
    ╰─────────────────────────────────────────────╯
    """
    print(header)


def print_tool_info(name, description, icon="🛡️"):
    """Affiche les infos d'un outil"""
    info = f"""
    {icon} {name}
    └─ {description}
    """
    print(info)


def print_success(message):
    """Affiche un message de succès"""
    print(f"    ✅ {message}")


def print_warning(message):
    """Affiche un avertissement"""
    print(f"    ⚠️  {message}")


def print_error(message):
    """Affiche une erreur"""
    print(f"    ❌ {message}")


def print_info(message):
    """Affiche une info"""
    print(f"    ℹ️  {message}")
