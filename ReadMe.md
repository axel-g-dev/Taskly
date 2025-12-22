# Taskly - Moniteur Système

<div align="center">
  <img src="assets/icon.png" alt="Logo Taskly" width="128" height="128">
  <p><em>Un moniteur système moderne avec interface Apple-style</em></p>
</div>

## Pourquoi Taskly ?

Le **Moniteur d'activité** d'Apple est puissant mais peu intuitif et visuellement désuet. Taskly a été créé pour offrir une alternative moderne avec :

- **Interface intuitive** : Informations claires et accessibles d'un coup d'œil
- **Design moderne** : Interface Apple-style avec animations fluides
- **Visualisations améliorées** : Graphiques en temps réel et cartes métriques colorées
- **Fonctionnalités avancées** : Alertes configurables, export de données, surveillance de température
- **Expérience optimisée** : Mise à jour en temps réel sans ralentissement

Taskly transforme la surveillance système en une expérience agréable et efficace.

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
│   ├── temperature_sensor.py   # Capteurs de température
│   ├── config.py               # Configuration et thème
│   ├── utils.py                # Fonctions utilitaires
│   └── components/             # Composants UI
│       ├── __init__.py
│       ├── metric_card.py      # Cartes métriques
│       ├── temperature_card.py # Carte température
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

# (macOS) Installer le support température
brew install osx-cpu-temp

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

- [README complet](docs/README.md) - Documentation complète
- [Guide d'installation](docs/INSTALL.md) - Instructions détaillées
- [Guide du lanceur](docs/LAUNCHER.md) - Options de lancement
- [Guide de contribution](docs/CONTRIBUTING.md) - Comment contribuer

## Fonctionnalités

- Surveillance CPU, RAM, Température, Réseau, Disque, Batterie
- Graphiques historiques en temps réel (30 secondes)
- Système d'alertes configurables
- Export de données (JSON/CSV)
- Interface moderne et optimisée
- Application macOS native avec icône

## Licence

MIT License - Voir [LICENSE](LICENSE)
