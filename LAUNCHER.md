# Instructions pour lancer Taskly depuis le bureau

## Méthode 1 : Double-clic (Recommandé)

1. Localisez le fichier `launch_taskly.command` dans le dossier Taskly
2. Double-cliquez dessus
3. Si macOS demande la permission, allez dans :
   - Préférences Système > Sécurité et confidentialité
   - Cliquez sur "Ouvrir quand même"

## Méthode 2 : Créer un alias sur le bureau

```bash
# Dans le terminal
ln -s ~/Desktop/Taskly/launch_taskly.command ~/Desktop/Taskly
```

Ensuite, double-cliquez sur l'alias sur votre bureau.

## Méthode 3 : Alias terminal

Ajoutez cette ligne à votre `~/.zshrc` :

```bash
alias taskly="cd ~/Desktop/Taskly && source env/bin/activate && python main.py"
```

Puis dans le terminal, tapez simplement :
```bash
taskly
```

## Dépannage

### "Permission refusée"
```bash
chmod +x ~/Desktop/Taskly/launch_taskly.command
```

### Le terminal se ferme immédiatement
Vérifiez que l'environnement virtuel existe :
```bash
ls ~/Desktop/Taskly/env
```

Si absent, réinstallez :
```bash
cd ~/Desktop/Taskly
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
