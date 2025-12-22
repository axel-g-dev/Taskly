#!/bin/bash

# Taskly Launcher
# Double-cliquez sur ce fichier pour lancer Taskly

# Obtenir le répertoire du script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Aller dans le répertoire Taskly
cd "$DIR"

# Activer l'environnement virtuel
source env/bin/activate

# Lancer Taskly
python main.py
