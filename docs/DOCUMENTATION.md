# Taskly - Moniteur Système

Un moniteur système moderne avec une interface inspirée d'Apple, développé en Python avec Flet.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/Flet-0.28+-5C2D91?style=flat-square&logo=flutter&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

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

### Aperçu de l'Interface

![Screenshot Taskly](../assets/screenshot_taskly.png)


---

## Fonctionnalités

- **CPU** : Pourcentage d'utilisation, nombre de cœurs, fréquence
- **RAM** : Utilisation mémoire avec affichage utilisé/total
- **Réseau** : Vitesses de téléchargement et d'envoi en temps réel
- **Batterie** : Niveau, état de charge, temps restant
- **Disque** : Utilisation de l'espace de stockage

### Visualisations
- **3 graphiques historiques** : CPU, RAM, Réseau (historique sur 30 secondes)
- **Graphique réseau double** : Téléchargement (vert) et envoi (cyan) séparés
- **Cartes métriques** : Affichage avec barres de progression colorées
- **Liste de processus** : Top 7 des processus les plus gourmands

### Système d'alertes
- **Seuils configurables** : CPU (90%), RAM (85%)
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



```bash
# Installation via Homebrew

# Vérification
```


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
python src/main.py
```

**Important** : Ne lancez l'application qu'une seule fois. Chaque exécution de `python src/main.py` ouvre une nouvelle fenêtre.

### Interface utilisateur

**Boutons d'en-tête** :
- Export : Exporter les données (JSON + CSV)
- Alertes : Afficher/masquer le panneau d'alertes
- Info : Afficher/masquer les informations système détaillées

**Cartes métriques** :
- **CPU** (Bleu) : Utilisation processeur 0-100%
- **RAM** (Violet) : Utilisation mémoire
- **Réseau** (Vert) : Vitesse de téléchargement

**Graphiques** :
- **CPU History** : Historique CPU sur 30 secondes
- **Memory History** : Historique RAM sur 30 secondes
- **Network History** : Upload + Download sur 30 secondes

**Liste de processus** :
- Tri par CPU ou RAM
- Affiche les 7 processus les plus gourmands

---

## Structure du projet

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
│       ├── metric_card.py      # Cartes métriques
│       ├── charts.py           # Graphiques
│       ├── process_list.py     # Liste de processus
│       ├── system_info.py      # Panneau d'infos
│       └── alert_manager.py    # Système d'alertes
├── assets/                      # Logo et ressources
├── docs/                        # Documentation
├── scripts/                     # Scripts de lancement
├── Taskly.app/                  # Application macOS
├── exports/                     # Données exportées
├── env/                         # Environnement virtuel
├── requirements.txt             # Dépendances Python
├── LICENSE                      # Licence MIT
└── README.md                    # README principal
```

---

## Configuration

### Seuils d'alerte

Modifiez `config.py` pour ajuster les seuils :

```python
ALERT_THRESHOLDS = {
    'cpu': 90,      # Alerte si CPU > 90%
    'ram': 85,      # Alerte si RAM > 85%
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


- **Windows** : Support variable selon le matériel

**Configuration macOS** :
```bash
```



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

### non disponible


```bash
```

Puis redémarrez Taskly.

### Plusieurs fenêtres Flet ouvertes

1. Fermez toutes les fenêtres
2. Appuyez sur `Ctrl+C` dans tous les terminaux
3. Relancez une seule fois : `python src/main.py`

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
