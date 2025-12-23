# Taskly v1.0.0 - Release Notes

## 🎉 Première Version Publique

Taskly est un moniteur système moderne créé pour remplacer le Moniteur d'activité d'Apple, qui est peu intuitif et visuellement désuet.

![Screenshot Taskly](assets/screenshot_taskly.png)

---

## ✨ Fonctionnalités Principales

### Surveillance Système Complète
- **CPU** : Utilisation, nombre de cœurs, fréquence
- **RAM** : Mémoire utilisée/totale avec pourcentage
- **Réseau** : Vitesses upload/download en temps réel
- **Disque** : Espace utilisé/total
- **Batterie** : Niveau, état de charge, temps restant

### Interface Moderne
- 🎨 Design Apple-style avec thème sombre élégant
- 📊 3 graphiques historiques en temps réel (30 secondes)
- 🎯 Cartes métriques colorées (CPU bleu, RAM violet, Réseau vert)
- 📋 Liste des 7 processus les plus gourmands
- ⚡ Animations fluides et micro-interactions

### Fonctionnalités Avancées
- 🔔 **Alertes configurables** : CPU > 90%, RAM > 85%
- 💾 **Export de données** : JSON et CSV
- 📱 **Application macOS native** : Taskly.app avec icône
- ⚙️ **Optimisations** : Cache intelligent, mises à jour conditionnelles

---

## 📦 Installation

### Méthode 1 : Clone et Installation

```bash
git clone https://github.com/axel-g-dev/Taskly.git
cd Taskly
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python src/main.py
```

### Méthode 2 : Application macOS

1. Télécharger le dépôt
2. Double-cliquer sur `Taskly.app`

---

## 🚀 Lancement Rapide

**3 façons de lancer Taskly** :

1. **Application macOS** : Double-clic sur `Taskly.app`
2. **Script** : Double-clic sur `scripts/launch_taskly.command`
3. **Terminal** : `python src/main.py`

---

## 📊 Statistiques

- **Langage** : Python 3.8+
- **Framework** : Flet 0.28+
- **Lignes de code** : ~2000
- **Fichiers source** : 12
- **Documentation** : 5 guides complets
- **Plateforme** : macOS, Linux, Windows

---

## 🎯 Pourquoi Taskly ?

Le Moniteur d'activité d'Apple souffre de plusieurs limitations :
- Interface peu intuitive avec informations dispersées
- Design vieillissant
- Absence de visualisations modernes
- Pas d'alertes configurables
- Aucune option d'export

**Taskly résout tous ces problèmes** avec une interface moderne, des graphiques en temps réel, des alertes intelligentes et l'export de données.

---

## 📚 Documentation

- [README](README.md) - Vue d'ensemble
- [INSTALL.md](docs/INSTALL.md) - Guide d'installation
- [DOCUMENTATION.md](docs/DOCUMENTATION.md) - Documentation technique
- [CONTRIBUTING.md](docs/CONTRIBUTING.md) - Guide de contribution
- [CHANGELOG.md](CHANGELOG.md) - Historique des versions

---

## 🙏 Remerciements

- **Flet** : Framework UI moderne pour Python
- **psutil** : Bibliothèque de monitoring système
- **Apple** : Inspiration pour le design

---

## 📝 Licence

MIT License - Voir [LICENSE](LICENSE)

---

## 🔗 Liens

- **GitHub** : https://github.com/axel-g-dev/Taskly
- **Issues** : https://github.com/axel-g-dev/Taskly/issues
- **Discussions** : https://github.com/axel-g-dev/Taskly/discussions

---

**Fait avec ❤️ et Python**
