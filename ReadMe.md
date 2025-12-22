# Taskly - System Monitor 🖥️

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flet](https://img.shields.io/badge/Flet-0.28+-purple.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Un moniteur système moderne et élégant avec interface Apple-style, développé en Python avec Flet.

[Fonctionnalités](#-fonctionnalités) • [Installation](#-installation) • [Utilisation](#-utilisation) • [Architecture](#-architecture) • [Configuration](#-configuration)

</div>

---

## ✨ Fonctionnalités

### 📊 Monitoring en Temps Réel
- **CPU** : Utilisation normalisée (0-100%), nombre de cœurs, fréquence
- **RAM** : Pourcentage d'utilisation, mémoire utilisée/totale
- **Température** : Monitoring CPU avec code couleur (vert/orange/rouge)
- **Réseau** : Vitesses upload/download en temps réel
- **Batterie** : Niveau, état de charge, temps restant
- **Disque** : Utilisation de l'espace disque

### 📈 Visualisations
- **3 graphiques historiques** : CPU, RAM, Réseau (30 secondes)
- **Graphique réseau dual** : Upload (cyan) + Download (vert)
- **Cartes métriques** : Affichage coloré avec barres de progression
- **Liste de processus** : Top 7 processus par CPU ou RAM

### 🔔 Système d'Alertes
- **Seuils configurables** : CPU (90%), RAM (85%), Température (80°C)
- **Niveaux d'alerte** : Warning et Critical
- **Cooldown intelligent** : 30 secondes entre alertes similaires
- **Panneau visuel** : Affichage avec icônes et timestamps

### 💾 Export de Données
- **Format JSON** : Structure complète avec historiques
- **Format CSV** : Tableau lisible pour Excel/Google Sheets
- **Export automatique** : Sauvegarde dans `./exports/`
- **Timestamps** : Nommage automatique des fichiers

### ⚡ Optimisations
- **Cache intelligent** : Disque et batterie mis à jour toutes les 5s
- **Historique optimisé** : 30 points au lieu de 60 (-50% mémoire)
- **Updates conditionnels** : UI mise à jour uniquement si changement > 0.5%
- **Code modulaire** : Architecture en composants réutilisables

---

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation rapide

```bash
# Cloner le projet
cd /Users/axel/Desktop/Taskly

# Créer un environnement virtuel
python3 -m venv env

# Activer l'environnement virtuel
source env/bin/activate  # macOS/Linux
# ou
env\Scripts\activate  # Windows

# Installer les dépendances
pip install flet psutil
```

---

## 🎮 Utilisation

### Lancement de l'application

```bash
# Activer l'environnement virtuel
source env/bin/activate

# Lancer Taskly
python main.py
```

### Interface Utilisateur

**Boutons d'en-tête** :
- 🕐 **Horloge** : Heure actuelle en temps réel
- 📥 **Export** : Exporter les données (JSON + CSV)
- 🔔 **Alertes** : Afficher/masquer le panneau d'alertes
- ℹ️ **Info** : Afficher/masquer les informations système détaillées

**Cartes métriques** :
- **CPU** : Bleu - Utilisation processeur normalisée
- **RAM** : Violet - Utilisation mémoire
- **Température** : Orange - Température CPU (si disponible)
- **Réseau** : Vert - Vitesse de téléchargement

**Graphiques** :
- **CPU History** : Historique d'utilisation CPU (30s)
- **Memory History** : Historique d'utilisation RAM (30s)
- **Network History** : Upload + Download (30s)

**Liste de processus** :
- Tri par CPU ou RAM
- Top 7 processus les plus gourmands
- Mise à jour en temps réel

---

## 🏗️ Architecture

### Structure du Projet

```
Taskly/
├── main.py                      # Point d'entrée
├── dashboard.py                 # Interface principale
├── data_manager.py              # Collecte des métriques
├── data_exporter.py             # Export JSON/CSV
├── config.py                    # Configuration et thème
├── utils.py                     # Fonctions utilitaires
├── components/                  # Composants UI
│   ├── __init__.py
│   ├── metric_card.py          # Cartes métriques
│   ├── temperature_card.py     # Carte température
│   ├── charts.py               # Graphiques (CPU/RAM/Net)
│   ├── process_list.py         # Liste de processus
│   ├── system_info.py          # Panneau d'infos
│   └── alert_manager.py        # Système d'alertes
├── exports/                     # Données exportées (gitignored)
├── env/                         # Environnement virtuel (gitignored)
└── README.md                    # Documentation
```

### Composants Principaux

**DashboardUI** (`dashboard.py`)
- Gère l'interface principale
- Coordonne les mises à jour
- Thread de monitoring en arrière-plan

**SystemDataManager** (`data_manager.py`)
- Collecte les métriques système via `psutil`
- Cache intelligent pour optimiser les performances
- Historique des données (30 points par métrique)

**DataExporter** (`data_exporter.py`)
- Export JSON structuré
- Export CSV tabulaire
- Gestion du répertoire d'export

**AlertManager** (`components/alert_manager.py`)
- Surveillance des seuils critiques
- Gestion des alertes avec cooldown
- Panneau d'affichage visuel

---

## ⚙️ Configuration

### Seuils d'Alerte

Modifiez `config.py` pour ajuster les seuils :

```python
ALERT_THRESHOLDS = {
    'cpu': 90,      # Alerte si CPU > 90%
    'ram': 85,      # Alerte si RAM > 85%
    'temp': 80,     # Alerte si Temp > 80°C
}
```

### Paramètres de Performance

```python
UPDATE_INTERVAL = 1.0       # Intervalle de mise à jour (secondes)
HISTORY_SIZE = 30           # Nombre de points d'historique
CACHE_INTERVAL = 5          # Intervalle de cache disque/batterie (secondes)
```

### Thème

Le thème Apple-style est défini dans `config.py` :

```python
class AppleTheme:
    # Couleurs système
    BG_COLOR = "#1C1C1E"
    CARD_COLOR = "#2C2C2E"
    
    # Accents
    BLUE = "#0A84FF"
    GREEN = "#30D158"
    ORANGE = "#FF9F0A"
    RED = "#FF453A"
    PURPLE = "#BF5AF2"
    # ...
```

---

## 🔧 Détails Techniques

### Normalisation CPU

Le CPU est normalisé pour afficher 0-100% même sur systèmes multi-cœurs :

```python
# psutil peut retourner > 100% sur multi-core
cpu_pct_raw = psutil.cpu_percent()
cpu_pct = min(cpu_pct_raw / cpu_count_logical * 100, 100)
```

**Pourquoi ?** Sur un système 4-cœurs, un processus utilisant 100% d'un cœur apparaîtrait comme 25% dans psutil. La normalisation permet une lecture plus intuitive.

### Optimisations Mémoire

- **Historique réduit** : 30 points au lieu de 60 (-50% mémoire)
- **Cache disque/batterie** : Mis à jour toutes les 5s au lieu de 1s
- **Updates conditionnels** : UI mise à jour uniquement si Δ > 0.5%

### Compatibilité Température

La température CPU n'est pas disponible sur tous les systèmes :
- ✅ **Linux** : Généralement supporté (coretemp, k10temp)
- ⚠️ **macOS** : Non supporté par psutil
- ✅ **Windows** : Support variable selon le matériel

L'application gère gracieusement l'absence de capteurs.

---

## 📊 Export de Données

### Format JSON

```json
{
  "timestamp": "2025-12-22T15:03:44",
  "metrics": {
    "cpu": {
      "percent": 75.8,
      "count": 2,
      "freq_mhz": 2400,
      "temp_celsius": null,
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
75.8,2,2400,N/A

Memory Metrics
Usage %,Used GB,Total GB,Available GB
74.0,4.4,8.0,3.6
...
```

---

## 🐛 Dépannage

### L'application ne démarre pas

```bash
# Vérifier que l'environnement virtuel est activé
source env/bin/activate

# Réinstaller les dépendances
pip install --upgrade flet psutil
```

### Température non disponible

C'est normal sur macOS. La carte affichera "--" au lieu d'une température.

### CPU > 100%

Si vous voyez encore des valeurs > 100%, vérifiez que vous utilisez la dernière version du code avec la normalisation CPU.

---

## 📝 Logs et Debug

### Activer les logs détaillés

Dans `config.py` :

```python
DEBUG = True    # Logs de debug
VERBOSE = True  # Logs très détaillés
```

Les logs apparaissent dans la console :

```
[15:03:44.353] [INFO] TASKLY - SYSTEM MONITOR STARTING
[15:03:44.353] [VERBOSE] Fetching system metrics...
[15:03:44.353] [VERBOSE] CPU: 75.8% (raw: 151.6%)
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 🙏 Remerciements

- **Flet** : Framework UI moderne pour Python
- **psutil** : Bibliothèque de monitoring système
- **Apple** : Inspiration pour le design

---

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation dans `/docs`
- Vérifiez les logs avec `DEBUG=True`

---

<div align="center">

**Fait avec ❤️ et Python**

[⬆ Retour en haut](#taskly---system-monitor-)

</div>