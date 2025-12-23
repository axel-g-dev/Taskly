# Taskly v1.1.0 - Internationalisation et Optimisations

## 🌐 Nouvelle Fonctionnalité Majeure : Support Multilingue

Taskly supporte maintenant **deux langues** : Français et Anglais !

### Comment changer de langue ?

Cliquez simplement sur le bouton 🌐 dans l'en-tête de l'application. Votre préférence est automatiquement sauvegardée et restaurée au prochain lancement.

![Language Toggle](assets/screenshot_taskly.png)

---

## ✨ Nouveautés

### Internationalisation
- ✅ **Support Français/Anglais complet**
- ✅ **Bouton de langue** (🌐) dans l'en-tête
- ✅ **Persistance** de la préférence utilisateur
- ✅ **100% des textes traduits** (interface complète)
- ✅ **Changement instantané** sans redémarrage

### Architecture Améliorée
- 📁 **Nouveau fichier `constants.py`** - Toutes les constantes centralisées
- 🔧 **Configuration unifiée** - Intervalles, seuils, dimensions UI
- 📦 **Code mieux organisé** - Plus facile à maintenir et étendre

---

## 🐛 Corrections de Bugs

### Bug CPU >100% Corrigé ✅

**Problème** : Certains processus affichaient >100% CPU dans "Top Processes"

**Cause** : Sur les systèmes multi-cœurs, `psutil` retourne le pourcentage CPU total (ex: 2 cœurs à 100% = 200%)

**Solution** : Normalisation par nombre de cœurs pour afficher 0-100%

**Avant** :
```
Chrome    200% CPU  ❌
Python    150% CPU  ❌
```

**Après** :
```
Chrome    100% CPU  ✅
Python     75% CPU  ✅
```

---

## ♻️ Refactorisation du Code

### `data_manager.py` - Refonte Complète

Le fichier a été refactorisé en **méthodes modulaires** :

```python
class SystemDataManager:
    def _get_cpu_metrics(self)      # Collecte CPU
    def _get_memory_metrics(self)   # Collecte RAM
    def _get_disk_metrics(self)     # Collecte Disque (avec cache)
    def _get_network_metrics(self)  # Collecte Réseau
    def _get_battery_metrics(self)  # Collecte Batterie (avec cache)
    def _get_system_metrics(self)   # Uptime, etc.
```

**Avantages** :
- ✅ Code plus lisible et maintenable
- ✅ Gestion d'erreurs individualisée
- ✅ Facile d'ajouter de nouvelles métriques
- ✅ Tests unitaires simplifiés

### Composants UI Améliorés

Tous les composants supportent maintenant les **mises à jour dynamiques** :

- `metric_card.py` → `update_title()`
- `process_list.py` → `update_labels()`
- `system_info.py` → `update_labels()`
- `charts.py` → `update_title()`

---

## 📊 Statistiques de la Release

- **Fichiers créés** : 2
  - `src/i18n.py` - Système de traduction
  - `src/constants.py` - Configuration centralisée
- **Fichiers modifiés** : 11
- **Lignes ajoutées** : 624
- **Lignes supprimées** : 149
- **Langues supportées** : 2 (FR, EN)

---

## 📦 Installation

### Mise à jour depuis v1.0.0

```bash
cd Taskly
git pull origin main
source env/bin/activate
python src/main.py
```

### Nouvelle installation

```bash
git clone https://github.com/axel-g-dev/Taskly.git
cd Taskly
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python src/main.py
```

---

## 🚀 Utilisation

### Changer de Langue

1. Cliquez sur le bouton 🌐 dans l'en-tête
2. L'interface bascule instantanément
3. Votre choix est sauvegardé automatiquement

### Langues Disponibles

- 🇫🇷 **Français** (par défaut)
- 🇬🇧 **English**

---

## 🔧 Détails Techniques

### Système de Traduction

Le système utilise un dictionnaire de traductions avec persistance :

```python
from i18n import TranslationManager

i18n = TranslationManager(default_language="fr")
title = i18n.t("cpu_usage")  # "Utilisation CPU" ou "CPU Usage"
```

### Configuration Centralisée

Toutes les constantes sont maintenant dans `constants.py` :

```python
# Performance
UPDATE_INTERVAL = 1.0
HISTORY_SIZE = 30

# Process Monitoring
NORMALIZE_CPU_BY_CORES = True

# UI
WINDOW_WIDTH = 1200
DEFAULT_LANGUAGE = "fr"
```

---

## 🙏 Remerciements

Merci à tous ceux qui ont testé et fourni des retours sur la v1.0.0 !

---

## 📝 Changelog Complet

Voir [CHANGELOG.md](CHANGELOG.md) pour tous les détails.

---

## 🔗 Liens

- **GitHub** : https://github.com/axel-g-dev/Taskly
- **Issues** : https://github.com/axel-g-dev/Taskly/issues
- **Discussions** : https://github.com/axel-g-dev/Taskly/discussions

---

**Fait avec ❤️ et Python**
