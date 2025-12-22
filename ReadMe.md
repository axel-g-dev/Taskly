# Taskly - Moniteur Système

<div align="center">
  <img src="assets/icon.png" alt="Logo Taskly" width="128" height="128">
  <p><em>Un moniteur système moderne avec interface Apple-style</em></p>
</div>

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
