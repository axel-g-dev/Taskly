# Guide de Contribution - Taskly

Merci de vouloir contribuer à Taskly ! Ce document explique comment participer au développement du projet.

## Code de Conduite

Ce projet respecte les principes de respect et de professionnalisme. En participant, vous vous engagez à maintenir ces standards.

## Comment Contribuer

### Signaler des Bugs

Avant de créer un rapport de bug, vérifiez que le problème n'a pas déjà été signalé. Quand vous créez un rapport de bug, incluez le maximum de détails :

- **Titre clair et descriptif**
- **Étapes pour reproduire le problème**
- **Exemples concrets**
- **Comportement observé vs comportement attendu**
- **Captures d'écran si pertinent**
- **Détails de votre environnement** (OS, version Python, version Flet)

### Suggérer des Améliorations

Les suggestions d'amélioration sont suivies via les GitHub Issues. Quand vous créez une suggestion, incluez :

- **Titre clair et descriptif**
- **Description détaillée de l'amélioration suggérée**
- **Explication de pourquoi cette amélioration serait utile**
- **Liste de fonctionnalités similaires dans d'autres applications**

### Pull Requests

1. Forkez le dépôt et créez votre branche depuis `main`
2. Si vous ajoutez du code, ajoutez des tests si applicable
3. Assurez-vous que votre code suit le style existant
4. Mettez à jour la documentation si nécessaire
5. Écrivez un message de commit clair

## Configuration pour le Développement

```bash
git clone https://github.com/axel-g-dev/Taskly.git
cd Taskly
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Directives de Style

### Code Python

- Suivez les directives PEP 8
- Utilisez des noms de variables et fonctions significatifs
- Ajoutez des docstrings aux fonctions et classes
- Gardez les fonctions courtes et focalisées
- Utilisez les type hints quand c'est approprié

### Messages de Commit

- Utilisez le présent ("Ajoute fonctionnalité" et non "Ajouté fonctionnalité")
- Utilisez l'impératif ("Déplace curseur vers..." et non "Déplace le curseur vers...")
- Limitez la première ligne à 72 caractères maximum
- Référencez les issues et pull requests quand pertinent

Exemple :
```
Ajoute surveillance de température

- Création du composant TemperatureCard
- Amélioration de data_manager avec collecte température
- Ajout affichage température avec code couleur
- Ferme #123
```

## Structure du Projet

```
Taskly/
├── main.py              # Point d'entrée
├── dashboard.py         # Interface principale
├── data_manager.py      # Collecte de données
├── data_exporter.py     # Fonctionnalité d'export
├── config.py            # Configuration
├── utils.py             # Utilitaires
└── components/          # Composants UI
    ├── metric_card.py
    ├── temperature_card.py
    ├── charts.py
    ├── process_list.py
    ├── system_info.py
    └── alert_manager.py
```

## Tests

Avant de soumettre une pull request :

1. Testez vos changements de manière approfondie
2. Assurez-vous que l'application démarre sans erreurs
3. Testez sur différentes plateformes si possible (macOS, Linux, Windows)
4. Vérifiez que les fonctionnalités existantes fonctionnent toujours

## Questions

N'hésitez pas à ouvrir une issue avec votre question ou à contacter les mainteneurs.

Merci de contribuer !
