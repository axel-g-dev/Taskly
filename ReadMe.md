# Taskly - Moniteur Système

<div align="center">
  <img src="assets/icon.png" alt="Logo Taskly" width="128" height="128">
  <p><em>Un moniteur système moderne avec interface Apple-style</em></p>
  
  ![Version](https://img.shields.io/badge/version-1.0.0-blue)
  ![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
  ![Flet](https://img.shields.io/badge/Flet-0.28+-5C2D91?logo=flutter&logoColor=white)
  ![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)
  ![License](https://img.shields.io/badge/License-MIT-green)
  ![GitHub stars](https://img.shields.io/github/stars/axel-g-dev/Taskly?style=social)
</div>

## Pourquoi Taskly ?

Le **Moniteur d'activité** d'Apple, bien que fonctionnel, souffre de plusieurs limitations :
- Interface peu intuitive avec trop d'informations dispersées
- Design vieillissant qui n'a pas évolué depuis des années
- Absence de visualisations modernes (graphiques limités)
- Pas d'alertes configurables
- Aucune option d'export de données

**Taskly a été créé pour résoudre ces problèmes** en offrant :

### Une Interface Moderne et Intuitive
- **Cartes métriques colorées** : CPU (bleu), RAM (violet) (orange), Réseau (vert)
- **Design Apple-style** : Interface sombre élégante avec animations fluides
- **Informations d'un coup d'œil** : Tout ce dont vous avez besoin sur un seul écran

### Des Fonctionnalités Avancées
- **Système d'alertes** : Soyez notifié quand CPU > 90%, RAM > 85%, ou > 80°C
- **Export de données** : Sauvegardez vos métriques en JSON ou CSV pour analyse
- **Optimisations intelligentes** : Cache et mises à jour conditionnelles pour des performances optimales

### Une Expérience Utilisateur Supérieure
- **Lancement rapide** : Application macOS native ou script de lancement
- **Architecture modulaire** : Code propre et facilement extensible
- **Open Source** : Licence MIT, personnalisable à souhait

**Taskly transforme la surveillance système en une expérience agréable, moderne et efficace.**

### Aperçu

![Screenshot Taskly](assets/screenshot_taskly.png)

---

## Structure du Projet

```
Taskly/
├── src/                         # Code source
│   ├── main.py                 # Point d'entrée
│   ├── dashboard.py            # Interface principale
│   ├── data_manager.py         # Collecte des métriques
│   ├── data_exporter.py        # Export JSON/CSV
│   ├── config.py               # Configuration et thème
│   ├── utils.py                # Fonctions utilitaires
│   └── components/             # Composants UI
│       ├── __init__.py
│       ├── metric_card.py      # Cartes métriques
│       ├── charts.py           # Graphiques
│       ├── process_list.py     # Liste de processus
│       ├── system_info.py      # Panneau d'infos
│       └── alert_manager.py    # Système d'alertes
├── assets/                      # Ressources
│   ├── icon.png                # Logo de l'application
│   └── screenshot_taskly.png   # Capture d'écran
├── docs/                        # Documentation
│   ├── README.md               # Documentation complète
│   ├── INSTALL.md              # Guide d'installation
│   ├── CONTRIBUTING.md         # Guide de contribution
│   └── LAUNCHER.md             # Options de lancement
├── scripts/                     # Scripts utilitaires
│   └── launch_taskly.command   # Lanceur macOS
├── Taskly.app/                  # Application macOS
│   └── Contents/
│       ├── Info.plist          # Métadonnées
│       ├── MacOS/Taskly        # Script exécutable
│       └── Resources/icon.png  # Icône
├── exports/                     # Données exportées (gitignored)
├── env/                         # Environnement virtuel (gitignored)
├── requirements.txt             # Dépendances Python
├── LICENSE                      # Licence MIT
└── README.md                    # Ce fichier
```

---

## Lancement Rapide

```bash
# Méthode 1 : Application macOS (double-clic)
open Taskly.app

# Méthode 2 : Script de lancement
./scripts/launch_taskly.command

# Méthode 3 : Ligne de commande
cd Taskly
source env/bin/activate
python src/main.py
```

## Installation depuis GitHub

```bash
# Cloner le dépôt
git clone https://github.com/axel-g-dev/Taskly.git
cd Taskly

# Créer l'environnement virtuel
python3 -m venv env
source env/bin/activate

# Installer les dépendances
pip install -r requirements.txt


# Lancer l'application
python src/main.py
# ou double-clic sur Taskly.app
```

## Déploiement

L'application est **prête à l'emploi** après clonage :
- Tous les fichiers nécessaires sont inclus
- L'application Taskly.app est fonctionnelle
- Aucune compilation requise
- Compatible macOS, Linux, Windows

**Note** : L'environnement virtuel doit être créé sur chaque machine.

## Documentation

- [📖 Documentation complète](docs/DOCUMENTATION.md) - Guide détaillé
- [⚙️ Guide d'installation](docs/INSTALL.md) - Instructions détaillées
- [🚀 Guide du lanceur](docs/LAUNCHER.md) - Options de lancement
- [🤝 Guide de contribution](docs/CONTRIBUTING.md) - Comment contribuer

## Fonctionnalités

- Surveillance CPU, RAM, Réseau, Disque, Batterie
- Système d'alertes configurables
- Export de données (JSON/CSV)
- Interface moderne et optimisée
- Application macOS native avec icône

## Licence

MIT License - Voir [LICENSE](LICENSE)
