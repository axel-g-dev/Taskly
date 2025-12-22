# Taskly - Moniteur Système

![Logo Taskly](assets/icon.png)

Un moniteur système moderne avec interface Apple-style, développé en Python avec Flet.

## Lancement Rapide

```bash
# Méthode 1 : Script de lancement
./scripts/launch_taskly.command

# Méthode 2 : Ligne de commande
cd Taskly
source env/bin/activate
python src/main.py
```

## Documentation

- [README complet](docs/README.md) - Documentation complète
- [Guide d'installation](docs/INSTALL.md) - Instructions d'installation détaillées
- [Guide du lanceur](docs/LAUNCHER.md) - Options de lancement
- [Guide de contribution](docs/CONTRIBUTING.md) - Comment contribuer

## Fonctionnalités Principales

- Surveillance CPU, RAM, Température, Réseau, Disque, Batterie
- Graphiques historiques en temps réel
- Système d'alertes configurables
- Export de données (JSON/CSV)
- Interface moderne et optimisée

## Installation

```bash
git clone https://github.com/axel-g-dev/Taskly.git
cd Taskly
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Sur macOS, pour la surveillance de température :
```bash
brew install osx-cpu-temp
```

## Licence

MIT License - Voir [LICENSE](LICENSE)

## Structure du Projet

```
Taskly/
├── src/           # Code source
├── assets/        # Logo et ressources
├── docs/          # Documentation
├── scripts/       # Scripts utilitaires
└── env/           # Environnement virtuel
```

Pour plus de détails, consultez la [documentation complète](docs/README.md).
