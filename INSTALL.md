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

**macOS/Linux**:
```bash
source env/bin/activate
```

**Windows**:
```bash
env\Scripts\activate
```

### 4. Installer les dépendances
```bash
pip install -r requirements.txt
```

---

## Configuration Spécifique par Plateforme

### macOS - Surveillance de la Température

Pour activer la surveillance de la température CPU sur macOS, installez `osx-cpu-temp`:

```bash
# Installation via Homebrew
brew install osx-cpu-temp

# Vérification
osx-cpu-temp
# Devrait afficher quelque chose comme: 48.2°C
```

**Pourquoi est-ce nécessaire ?**
- macOS n'expose pas les capteurs de température via les API standard
- `psutil` ne peut pas accéder aux données de température sur macOS
- `osx-cpu-temp` lit directement depuis le SMC (System Management Controller)

**Que se passe-t-il si je ne l'installe pas ?**
- Taskly fonctionnera parfaitement
- La carte de température ne sera simplement pas affichée
- Toutes les autres fonctionnalités restent opérationnelles

### Linux - Surveillance de la Température

La surveillance de température fonctionne nativement sur la plupart des systèmes Linux:

**Capteurs supportés**:
- `coretemp` (CPU Intel)
- `k10temp` (CPU AMD)
- `cpu_thermal` (ARM/Raspberry Pi)

**Vérifier les capteurs**:
```bash
# Vérifier les capteurs disponibles
sensors

# Ou avec Python
python3 -c "import psutil; print(psutil.sensors_temperatures())"
```

### Windows - Surveillance de la Température

Le support de température sur Windows varie:
- Certains systèmes le supportent nativement via `psutil`
- D'autres peuvent nécessiter des pilotes tiers
- Taskly détecte automatiquement et s'adapte

---

## Lancement de Taskly

Une fois installé, lancez Taskly avec:

```bash
# Assurez-vous que l'environnement virtuel est activé
source env/bin/activate  # macOS/Linux
# ou
env\Scripts\activate  # Windows

# Lancer l'application
python main.py
```

---

## Dépannage

### "ModuleNotFoundError: No module named 'flet'"

**Solution**: Activez d'abord l'environnement virtuel
```bash
source env/bin/activate
pip install -r requirements.txt
```

### La température ne s'affiche pas sur macOS

**Solution**: Installez `osx-cpu-temp`
```bash
brew install osx-cpu-temp
```

Puis redémarrez Taskly.

### Homebrew n'est pas installé (macOS)

**Solution**: Installez d'abord Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Plusieurs fenêtres Flet s'ouvrent

**Cause**: Exécution multiple de `python main.py`

**Solution**: 
1. Fermez toutes les fenêtres Flet
2. Appuyez sur `Ctrl+C` dans tous les terminaux
3. Exécutez `python main.py` une seule fois

---

## Mise à jour de Taskly

Pour mettre à jour vers la dernière version:

```bash
cd Taskly
git pull origin main
source env/bin/activate
pip install -r requirements.txt --upgrade
```

---

## Désinstallation

Pour supprimer complètement Taskly:

```bash
# Supprimer le répertoire
cd ..
rm -rf Taskly

# (Optionnel) Désinstaller osx-cpu-temp sur macOS
brew uninstall osx-cpu-temp
```

---

## Prochaines Étapes

- Lisez le [README](README.md) pour un aperçu des fonctionnalités
- Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour contribuer
- Signalez les problèmes sur [GitHub](https://github.com/axel-g-dev/Taskly/issues)

---

**Besoin d'aide ?** Ouvrez une issue sur GitHub.
