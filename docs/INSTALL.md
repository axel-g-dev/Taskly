# Guide d'Installation - Taskly

## Installation Rapide

### 1. Cloner le dépôt
```bash
git clone https://github.com/axel-g-dev/Taskly.git
cd Taskly
```

### 2. Créer l'environnement virtuel
```bash
python3 -m venv env
```

### 3. Activer l'environnement virtuel

**macOS/Linux** :
```bash
source env/bin/activate
```

**Windows** :
```bash
env\Scripts\activate
```

### 4. Installer les dépendances
```bash
pip install -r requirements.txt
```

---



## Lancement de Taskly

Une fois installé, lancez Taskly avec :

```bash
# Assurez-vous que l'environnement virtuel est activé
source env/bin/activate  # macOS/Linux
# ou
env\Scripts\activate  # Windows

# Lancer l'application
python src/main.py
```

**Important** : Ne lancez l'application qu'une seule fois. Chaque exécution de `python src/main.py` ouvre une nouvelle fenêtre.

---

## Dépannage

### "ModuleNotFoundError: No module named 'flet'"

**Cause** : L'environnement virtuel n'est pas activé

**Solution** :
```bash
source env/bin/activate
pip install -r requirements.txt
```



**Solution** :
```bash
```

Puis redémarrez Taskly.

### Homebrew n'est pas installé (macOS)

**Solution** : Installez d'abord Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Plusieurs fenêtres Flet s'ouvrent

**Cause** : Vous avez lancé `python main.py` plusieurs fois

**Solution** : 
1. Fermez toutes les fenêtres Flet
2. Appuyez sur `Ctrl+C` dans tous les terminaux
3. Relancez une seule fois : `python src/main.py`

### Erreur de permission sur Linux

**Cause** : Certains capteurs nécessitent des permissions spéciales

**Solution** :
```bash
# Ajouter votre utilisateur au groupe approprié
sudo usermod -a -G video $USER
# Puis redémarrez votre session
```

---

## Mise à jour de Taskly

Pour mettre à jour vers la dernière version :

```bash
cd Taskly
git pull origin main
source env/bin/activate
pip install -r requirements.txt --upgrade
```

---

## Désinstallation

Pour supprimer complètement Taskly :

```bash
# Supprimer le répertoire
cd ..
rm -rf Taskly

```

---

## Prochaines Étapes

- Lisez la [Documentation complète](DOCUMENTATION.md) pour un aperçu complet des fonctionnalités
- Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour contribuer au projet
- Signalez les problèmes sur [GitHub Issues](https://github.com/axel-g-dev/Taskly/issues)

---

**Besoin d'aide ?** N'hésitez pas à ouvrir une issue sur GitHub.
