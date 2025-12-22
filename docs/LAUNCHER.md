# Instructions pour lancer Taskly depuis le bureau

## Méthode 1 : Application macOS (Recommandé)

1. Double-cliquez sur `Taskly.app` dans le dossier Taskly
2. L'application se lance automatiquement
3. Si macOS demande la permission, allez dans :
   - Préférences Système > Sécurité et confidentialité
   - Cliquez sur "Ouvrir quand même"

## Méthode 2 : Script de lancement

1. Localisez le fichier `scripts/launch_taskly.command` dans le dossier Taskly
2. Double-cliquez dessus
3. Si macOS demande la permission, suivez les mêmes étapes que ci-dessus

## Méthode 3 : Créer un alias sur le bureau

```bash
# Dans le terminal (remplacez <chemin> par votre chemin vers Taskly)
ln -s <chemin>/Taskly/scripts/launch_taskly.command ~/Desktop/Taskly-Launcher
```

Ensuite, double-cliquez sur l'alias sur votre bureau.

## Méthode 4 : Alias terminal

Ajoutez cette ligne à votre `~/.zshrc` (remplacez <chemin> par votre chemin) :

```bash
alias taskly="cd <chemin>/Taskly && source env/bin/activate && python src/main.py"
```

Puis dans le terminal, tapez simplement :
```bash
taskly
```

## Dépannage

### "Permission refusée"
```bash
chmod +x <chemin>/Taskly/scripts/launch_taskly.command
```

### Le terminal se ferme immédiatement
Vérifiez que l'environnement virtuel existe :
```bash
ls <chemin>/Taskly/env
```

Si absent, réinstallez :
```bash
cd <chemin>/Taskly
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### L'application Taskly.app ne se lance pas

Consultez les logs :
```bash
cat /tmp/taskly_launch.log
```

Vérifiez que l'environnement virtuel est créé :
```bash
ls <chemin>/Taskly/env/bin/python
```

## Notes

- **Taskly.app** : Ne s'affiche pas dans le Dock, seule la fenêtre Flet apparaît
- **Logs** : Tous les lancements via Taskly.app sont enregistrés dans `/tmp/taskly_launch.log`
- **Portabilité** : Tous les chemins sont relatifs, l'application fonctionne quel que soit son emplacement
