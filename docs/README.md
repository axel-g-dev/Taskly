# Taskly - Moniteur Système

Un moniteur système moderne avec une interface inspirée d'Apple, développé en Python avec Flet.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/Flet-0.28+-5C2D91?style=flat-square&logo=flutter&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## Fonctionnalités

### Surveillance en temps réel
- **CPU** : Pourcentage d'utilisation, nombre de cœurs, fréquence
- **RAM** : Utilisation mémoire avec affichage utilisé/total
- **Température** : Température CPU avec code couleur (vert/orange/rouge)
- **Réseau** : Vitesses de téléchargement et d'envoi en temps réel
- **Batterie** : Niveau, état de charge, temps restant
- **Disque** : Utilisation de l'espace de stockage

### Visualisations
- **3 graphiques historiques** : CPU, RAM, Réseau (historique sur 30 secondes)
- **Graphique réseau double** : Téléchargement (vert) et envoi (cyan) séparés
- **Cartes métriques** : Affichage avec barres de progression colorées
- **Liste de processus** : Top 7 des processus les plus gourmands

### Système d'alertes
- **Seuils configurables** : CPU (90%), RAM (85%), Température (80°C)
- **Niveaux d'alerte** : Warning et Critical
- **Cooldown intelligent** : 30 secondes entre alertes similaires
- **Panneau visuel** : Affichage avec icônes et horodatage

### Export de données
- **Format JSON** : Données structurées complètes avec historiques
- **Format CSV** : Tableaux lisibles pour Excel/Google Sheets
- **Sauvegarde automatique** : Fichiers dans le dossier `./exports/`
- **Horodatage** : Noms de fichiers automatiques avec date et heure

### Optimisations
- **Cache intelligent** : Disque et batterie mis à jour toutes les 5s
- **Historique optimisé** : 30 points au lieu de 60 (économie de 50% de mémoire)
- **Mises à jour conditionnelles** : Interface mise à jour uniquement si changement > 0.5%
- **Architecture modulaire** : Code organisé en composants réutilisables

### Interface utilisateur
- **Animations optimisées** : Transitions fluides et effets de survol
- **Design moderne** : Interface Apple-style avec thème sombre
- **Lanceur bureau** : Script de lancement rapide pour macOS
- **Responsive** : Interface adaptative et fluide

---

## Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation rapide

```bash
# Cloner le dépôt
git clone https://github.com/axel-g-dev/Taskly.git
cd Taskly

# Créer un environnement virtuel
python3 -m venv env

# Activer l'environnement virtuel
source env/bin/activate  # macOS/Linux
# ou
env\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Surveillance de température sur macOS (optionnel)

Pour activer la surveillance de température CPU sur macOS :

```bash
# Installation via Homebrew
brew install osx-cpu-temp

# Vérification
osx-cpu-temp
```

**Note** : La surveillance de température fonctionne nativement sur Linux. Sur macOS, elle nécessite `osx-cpu-temp`. Sur Windows, le support varie selon le matériel.

### Lanceur bureau (macOS)

Pour lancer Taskly facilement depuis le bureau :

1. Localisez le fichier `launch_taskly.command` dans le dossier Taskly
2. Double-cliquez dessus pour lancer l'application
3. (Optionnel) Créez un alias sur votre bureau :
   ```bash
   ln -s <chemin>/Taskly/scripts/launch_taskly.command ~/Desktop/Taskly-Launcher
   ```

Voir [LAUNCHER.md](LAUNCHER.md) pour plus d'options de lancement.

---

## Utilisation

### Lancement de l'application

```bash
# Activer l'environnement virtuel
source env/bin/activate

# Lancer Taskly
python main.py
```

**Important** : Ne lancez l'application qu'une seule fois. Chaque exécution de `python main.py` ouvre une nouvelle fenêtre.

### Interface utilisateur

**Boutons d'en-tête** :
- Horloge : Heure actuelle en temps réel
- Export : Exporter les données (JSON + CSV)
- Alertes : Afficher/masquer le panneau d'alertes
- Info : Afficher/masquer les informations système détaillées

**Cartes métriques** :
- **CPU** (Bleu) : Utilisation processeur 0-100%
- **RAM** (Violet) : Utilisation mémoire
- **Température** (Orange) : Température CPU (si disponible)
- **Réseau** (Vert) : Vitesse de téléchargement

**Graphiques** :
- **CPU History** : Historique CPU sur 30 secondes
- **Memory History** : Historique RAM sur 30 secondes
- **Network History** : Upload + Download sur 30 secondes

**Liste de processus** :
- Tri par CPU ou RAM
- Affiche les 7 processus les plus gourmands
- Mise à jour en temps réel

---

## Structure du projet

```
Taskly/
├── main.py                      # Point d'entrée
├── dashboard.py                 # Interface principale
├── data_manager.py              # Collecte des métriques
├── data_exporter.py             # Export JSON/CSV
├── temperature_sensor.py        # Capteurs de température
├── config.py                    # Configuration et thème
├── utils.py                     # Fonctions utilitaires
├── components/                  # Composants UI
│   ├── metric_card.py          # Cartes métriques
│   ├── temperature_card.py     # Carte température
│   ├── charts.py               # Graphiques
│   ├── process_list.py         # Liste de processus
│   ├── system_info.py          # Panneau d'infos
│   └── alert_manager.py        # Système d'alertes
├── exports/                     # Données exportées
├── env/                         # Environnement virtuel
└── README.md                    # Ce fichier
```

---

## Configuration

### Seuils d'alerte

Modifiez `config.py` pour ajuster les seuils :

```python
ALERT_THRESHOLDS = {
    'cpu': 90,      # Alerte si CPU > 90%
    'ram': 85,      # Alerte si RAM > 85%
    'temp': 80,     # Alerte si Temp > 80°C
}
```

### Paramètres de performance

```python
UPDATE_INTERVAL = 1.0       # Intervalle de mise à jour (secondes)
HISTORY_SIZE = 30           # Nombre de points d'historique
CACHE_INTERVAL = 5          # Intervalle de cache disque/batterie (secondes)
```

### Paramètres d'animation

```python
ENABLE_ANIMATIONS = True    # Activer/désactiver les animations
ANIMATION_DURATION = 200    # Durée des animations (ms)
HOVER_SCALE = 1.02          # Échelle au survol
SHADOW_BLUR = 15            # Flou de l'ombre
```

### Logs de débogage

```python
DEBUG = True     # Logs de debug
VERBOSE = False  # Logs très détaillés (recommandé: False en production)
```

---

## Détails techniques

### Normalisation CPU

Le CPU est affiché de 0 à 100% pour une lecture intuitive :

```python
# psutil retourne déjà une valeur 0-100%
cpu_pct = psutil.cpu_percent()  # Déjà normalisé
```

### Optimisations mémoire

- **Historique réduit** : 30 points au lieu de 60 (économie de 50%)
- **Cache disque/batterie** : Mis à jour toutes les 5s au lieu de 1s
- **Mises à jour conditionnelles** : UI mise à jour uniquement si changement > 0.5%

### Compatibilité température

La surveillance de température varie selon la plateforme :
- **Linux** : Support complet (coretemp, k10temp, cpu_thermal)
- **macOS** : Support via `osx-cpu-temp` (installation requise)
- **Windows** : Support variable selon le matériel

**Configuration macOS** :
```bash
brew install osx-cpu-temp
```

L'application détecte automatiquement les capteurs disponibles et adapte l'interface. Si aucun capteur n'est disponible, la carte température est masquée.

**Note sur les températures** : `osx-cpu-temp` lit la température du package CPU (capteur TC0P), qui est plus stable que les températures individuelles des cœurs. Cette valeur représente mieux la charge globale du système.

---

## Export de données

### Format JSON

```json
{
  "timestamp": "2025-12-22T15:03:44",
  "metrics": {
    "cpu": {
      "percent": 75.8,
      "count": 2,
      "freq_mhz": 2400,
      "temp_celsius": 48.2,
      "history": [...]
    },
    "memory": {...},
    "network": {...}
  }
}
```

### Format CSV

```csv
Timestamp,2025-12-22T15:03:44

CPU Metrics
Usage %,Cores,Frequency MHz,Temperature °C
75.8,2,2400,48.2

Memory Metrics
Usage %,Used GB,Total GB,Available GB
74.0,4.4,8.0,3.6
...
```

---

## Dépannage

### L'application ne démarre pas

```bash
# Vérifier que l'environnement virtuel est activé
source env/bin/activate

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Température non disponible

C'est normal sur macOS sans `osx-cpu-temp`. Pour l'activer :

```bash
brew install osx-cpu-temp
```

Puis redémarrez Taskly.

### Plusieurs fenêtres Flet ouvertes

1. Fermez toutes les fenêtres
2. Appuyez sur `Ctrl+C` dans tous les terminaux
3. Relancez une seule fois : `python main.py`

---

## Contribution

Les contributions sont les bienvenues. Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/NouvelleFonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout NouvelleFonctionnalite'`)
4. Pushez vers la branche (`git push origin feature/NouvelleFonctionnalite`)
5. Ouvrez une Pull Request

---

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## Remerciements

- **Flet** : Framework UI moderne pour Python
- **psutil** : Bibliothèque de monitoring système
- **Apple** : Inspiration pour le design

---

## Support

Pour toute question ou problème :
- Ouvrez une issue sur [GitHub](https://github.com/axel-g-dev/Taskly/issues)
- Consultez la documentation dans le dossier `/docs`
- Vérifiez les logs avec `DEBUG=True` dans `config.py`

---

Fait avec Python
