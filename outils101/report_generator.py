"""
Générateur de rapports HTML/PDF complets pour l'audit réseau.
Combine tous les outils en un seul rapport professionnel.
"""

import json
import os
from datetime import datetime
from pathlib import Path


def generate_html_report(devices, alerts, history):
    """Génère un rapport HTML complet du réseau scanné."""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    
    filename = report_dir / f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    # Compter les stats
    total_devices = len(devices)
    new_devices = len([a for a in alerts if "NEW_DEVICE" in a.get("alert_type", "")])
    disconnected = len([a for a in alerts if "DISCONNECTED" in a.get("alert_type", "")])
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Audit Réseau - Outils 101</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            .header p {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                padding: 30px;
                background: #f8f9fa;
            }}
            .stat-card {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
                border-left: 4px solid #667eea;
            }}
            .stat-card h3 {{
                font-size: 2em;
                color: #667eea;
                margin-bottom: 5px;
            }}
            .stat-card p {{
                color: #666;
                font-size: 0.9em;
            }}
            .section {{
                padding: 30px;
                border-bottom: 1px solid #eee;
            }}
            .section h2 {{
                color: #667eea;
                margin-bottom: 20px;
                font-size: 1.8em;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}
            table th {{
                background: #f8f9fa;
                color: #333;
                padding: 12px;
                text-align: left;
                font-weight: 600;
                border-bottom: 2px solid #667eea;
            }}
            table td {{
                padding: 12px;
                border-bottom: 1px solid #eee;
            }}
            table tr:hover {{
                background: #f8f9fa;
            }}
            .badge {{
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: 600;
            }}
            .badge-new {{
                background: #d4edda;
                color: #155724;
            }}
            .badge-alert {{
                background: #f8d7da;
                color: #721c24;
            }}
            .badge-safe {{
                background: #d1ecf1;
                color: #0c5460;
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }}
            .alert-item {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 10px 0;
                border-radius: 4px;
            }}
            .device-item {{
                background: #f8f9fa;
                padding: 15px;
                margin: 10px 0;
                border-radius: 4px;
                border-left: 4px solid #667eea;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛡️ Audit Réseau Outils 101</h1>
                <p>Rapport généré le {timestamp}</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>{total_devices}</h3>
                    <p>Appareils détectés</p>
                </div>
                <div class="stat-card">
                    <h3>{new_devices}</h3>
                    <p>Nouveaux appareils</p>
                </div>
                <div class="stat-card">
                    <h3>{disconnected}</h3>
                    <p>Déconnexions</p>
                </div>
                <div class="stat-card">
                    <h3>{len(alerts)}</h3>
                    <p>Alertes totales</p>
                </div>
            </div>
            
            <div class="section">
                <h2>📱 Appareils Connectés</h2>
                <table>
                    <tr>
                        <th>IP</th>
                        <th>MAC</th>
                        <th>Fabricant</th>
                        <th>Nom</th>
                        <th>Statut</th>
                    </tr>
    """
    
    for device in devices:
        status_badge = f"<span class='badge badge-safe'>Actif</span>"
        html_content += f"""
                    <tr>
                        <td>{device.get('ip', 'N/A')}</td>
                        <td><code>{device.get('mac', 'N/A')}</code></td>
                        <td>{device.get('vendor', 'Inconnu')}</td>
                        <td>{device.get('name', 'Sans nom')}</td>
                        <td>{status_badge}</td>
                    </tr>
        """
    
    html_content += """
                </table>
            </div>
            
            <div class="section">
                <h2>⚠️ Alertes Récentes</h2>
    """
    
    if alerts:
        for alert in alerts[-10:]:  # Dernières 10 alertes
            alert_type = alert.get("alert_type", "UNKNOWN")
            badge_class = "badge-new" if "NEW" in alert_type else "badge-alert"
            html_content += f"""
                <div class="alert-item">
                    <strong>{alert.get('timestamp', 'N/A')}</strong> - 
                    <span class="badge {badge_class}">{alert_type}</span>
                    <p>{alert.get('message', 'N/A')}</p>
                </div>
            """
    else:
        html_content += "<p>Aucune alerte pour le moment.</p>"
    
    html_content += """
            </div>
            
            <div class="section">
                <h2>📊 Historique</h2>
                <p>Nombre d'entrées d'historique : <strong>""" + str(len(history)) + """</strong></p>
                <p><em>Voir le fichier <code>logs/devices_history.json</code> pour l'historique complet.</em></p>
            </div>
            
            <div class="footer">
                <p>🐧🌀 Outils 101 - Audit Réseau Local | Open Source</p>
                <p>Généré automatiquement | À usage défensif uniquement</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Rapport HTML généré : {filename}")
    return str(filename)


def export_to_json(devices, alerts, history):
    """Exporte tous les données en JSON structuré."""
    export_dir = Path("exports")
    export_dir.mkdir(exist_ok=True)
    
    filename = export_dir / f"audit_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_devices": len(devices),
            "total_alerts": len(alerts),
            "history_entries": len(history)
        },
        "devices": devices,
        "alerts": alerts,
        "history": history
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Données exportées en JSON : {filename}")
    return str(filename)
