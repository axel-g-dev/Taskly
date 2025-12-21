import psutil
import time
import os

def nettoyer_ecran():
    # Commande pour effacer l'écran (fonctionne sur Windows et Linux/Mac)
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_moniteur():
    print("=" * 40)
    print("      MONITEUR D'ACTIVITÉ SIMPLIFIÉ      ")
    print("=" * 40)
    print("Appuie sur Ctrl+C pour arrêter")
    print("-" * 40)

    try:
        while True:
            # 1. Récupérer l'utilisation CPU
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # 2. Récupérer l'utilisation de la RAM
            ram = psutil.virtual_memory()
            ram_usage = ram.percent
            ram_dispo = round(ram.available / (1024 ** 3), 2) # Convertir en Go
            
            # 3. Barres de chargement visuelles
            barre_cpu = "█" * int(cpu_usage / 5) + "-" * (20 - int(cpu_usage / 5))
            barre_ram = "█" * int(ram_usage / 5) + "-" * (20 - int(ram_usage / 5))

            # 4. Affichage
            nettoyer_ecran()
            print("=" * 40)
            print("      MONITEUR EN TEMPS RÉEL      ")
            print("=" * 40)
            
            print(f"CPU Utilisation : {cpu_usage}%")
            print(f"[{barre_cpu}]")
            print("-" * 40)
            
            print(f"RAM Utilisation : {ram_usage}%")
            print(f"[{barre_ram}]")
            print(f"   Libre : {ram_dispo} Go")
            print("-" * 40)
            
            # Pause de 0.5 seconde avant la prochaine mise à jour (l'intervalle cpu fait déjà 1s)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n Moniteur arrêté.")

if __name__ == "__main__":
    afficher_moniteur()
