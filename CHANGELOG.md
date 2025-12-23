# Changelog

Toutes les modifications notables de Taskly seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

---

## [1.1.0] - 2025-12-23

### ✨ Ajouté

**Internationalisation**
- Support complet Français/Anglais
- Bouton de changement de langue (🌐) dans l'en-tête
- Persistance de la préférence utilisateur dans `~/.taskly_config.json`
- 100% des textes de l'interface traduits
- Système de traduction modulaire (`i18n.py`)

**Architecture**
- Nouveau fichier `constants.py` pour centraliser toutes les constantes
- Configuration centralisée (intervalles, seuils, dimensions UI)
- Meilleure organisation du code

### 🐛 Corrigé

**Bug CPU >100%**
- Correction de l'affichage des processus dans "Top Processes"
- Normalisation du pourcentage CPU par nombre de cœurs
- Les processus affichent maintenant correctement 0-100% CPU
- Fix de la formule mathématique de normalisation

### ♻️ Refactorisé

**data_manager.py**
- Refactorisation complète en méthodes modulaires :
  - `_get_cpu_metrics()` - Collecte CPU
  - `_get_memory_metrics()` - Collecte RAM
  - `_get_disk_metrics()` - Collecte Disque (avec cache)
  - `_get_network_metrics()` - Collecte Réseau
  - `_get_battery_metrics()` - Collecte Batterie (avec cache)
  - `_get_system_metrics()` - Uptime et infos système
- Gestion d'erreurs individualisée par métrique
- Code plus lisible et maintenable

**Composants UI**
- Tous les composants supportent maintenant les mises à jour dynamiques de langue :
  - `metric_card.py` : Méthode `update_title()`
  - `process_list.py` : Méthode `update_labels()`
  - `system_info.py` : Méthode `update_labels()`
  - `charts.py` : Méthode `update_title()`

**Imports optimisés**
- `config.py` importe maintenant de `constants.py`
- `dashboard.py` utilise les constantes pour les dimensions de fenêtre
- `data_exporter.py` utilise `EXPORT_DIRECTORY`
- `alert_manager.py` utilise `ALERT_COOLDOWN`
- Élimination des duplications de code

### 📊 Statistiques

- **Fichiers créés** : 2 (`i18n.py`, `constants.py`)
- **Fichiers modifiés** : 11
- **Lignes ajoutées** : 624
- **Lignes supprimées** : 149
- **Langues supportées** : 2 (FR, EN)

---

## [1.0.0] - 2025-12-23

### 🎉 Version Initiale

Première version publique de Taskly, un moniteur système moderne pour remplacer le Moniteur d'activité d'Apple.

### ✨ Ajouté

**Surveillance Système**
- Surveillance CPU : Pourcentage d'utilisation, nombre de cœurs, fréquence
- Surveillance RAM : Utilisation mémoire avec affichage utilisé/total
- Surveillance Réseau : Vitesses de téléchargement et d'envoi en temps réel
- Surveillance Disque : Utilisation de l'espace de stockage
- Surveillance Batterie : Niveau, état de charge, temps restant
- Uptime système

**Interface Utilisateur**
- Interface moderne Apple-style avec thème sombre
- 3 cartes métriques colorées (CPU bleu, RAM violet, Réseau vert)
- 3 graphiques historiques en temps réel (30 secondes)
- Liste des 7 processus les plus gourmands (tri CPU/RAM)
- Panneau d'informations système détaillées
- Animations fluides et effets de survol

**Fonctionnalités Avancées**
- Système d'alertes configurables (CPU > 90%, RAM > 85%)
- Cooldown intelligent (30s entre alertes similaires)
- Export de données en JSON et CSV
- Sauvegarde automatique dans `./exports/`
- Horloge en temps réel dans l'en-tête

**Optimisations**
- Cache intelligent pour disque et batterie (mise à jour toutes les 5s)
- Historique optimisé (30 points au lieu de 60, économie de 50% de mémoire)
- Mises à jour conditionnelles de l'UI (seulement si changement > 0.5%)
- Architecture modulaire avec composants réutilisables

**Application macOS**
- Application native Taskly.app avec icône personnalisée
- Script de lancement `scripts/launch_taskly.command`
- Pas d'icône dans le Dock (LSUIElement)
- Logs de débogage dans `/tmp/taskly_launch.log`

**Documentation**
- README complet avec screenshot
- Guide d'installation détaillé (INSTALL.md)
- Documentation technique complète (DOCUMENTATION.md)
- Guide de contribution (CONTRIBUTING.md)
- Guide du lanceur (LAUNCHER.md)
- Licence MIT

### 🏗️ Structure du Projet

```
Taskly/
├── src/                    # Code source modulaire
├── assets/                 # Logo et screenshots
├── docs/                   # Documentation complète
├── scripts/                # Scripts de lancement
├── Taskly.app/             # Application macOS native
├── exports/                # Données exportées
└── env/                    # Environnement virtuel
```

### 🔧 Technologies

- **Framework UI** : Flet 0.28+
- **Bibliothèque Système** : psutil 5.9+
- **Langage** : Python 3.8+
- **Plateforme** : macOS, Linux, Windows

### 📊 Statistiques

- ~2000 lignes de code Python
- 12 fichiers source
- 5 fichiers de documentation
- 100% des objectifs atteints

---

## [Unreleased]

### À venir dans les prochaines versions

- Tests unitaires
- Mode économie d'énergie
- Statistiques historiques (1h, 24h, 7j)
- Notifications système natives
- Thèmes personnalisables
- Widget macOS

---

[1.0.0]: https://github.com/axel-g-dev/Taskly/releases/tag/v1.0.0
