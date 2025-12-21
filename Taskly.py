import tkinter as tk
from tkinter import ttk  # Pour des jolis widgets (barres de progression)
import psutil

# --- Configuration ---
COULEUR_FOND = "#ECECEC"  # Gris clair typique Mac
COULEUR_TEXTE = "#333333"

def mettre_a_jour():
    # 1. Récupérer les infos (interval=None pour ne pas bloquer la fenêtre)
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    batterie = psutil.sensors_battery()
    
    # 2. Mettre à jour les textes
    label_cpu_val.config(text=f"{cpu}%")
    label_ram_val.config(text=f"{ram}%")
    
    # 3. Mettre à jour les barres de progression
    barre_cpu['value'] = cpu
    barre_ram['value'] = ram
    
    # 4. Gestion de la batterie
    icon = "⚡" if batterie.power_plugged else "🔋"
    label_bat_val.config(text=f"{icon} {batterie.percent}%")
    
    # Changer la couleur de la barre batterie si faible (<20%)
    if not batterie.power_plugged and batterie.percent < 20:
        style.configure("red.Horizontal.TProgressbar", background='red')
        barre_bat.config(style="red.Horizontal.TProgressbar")
    else:
        barre_bat.config(style="green.Horizontal.TProgressbar")
        
    barre_bat['value'] = batterie.percent

    # 5. On relance cette fonction dans 1000ms (1 seconde)
    root.after(1000, mettre_a_jour)

# --- Création de la Fenêtre ---
root = tk.Tk()
root.title("Moniteur Mac")
root.geometry("300x250") # Taille de la fenêtre (Largeur x Hauteur)
root.resizable(False, False) # Empêcher de redimensionner
root.configure(bg=COULEUR_FOND)

# Style pour les barres (Vert par défaut)
style = ttk.Style()
style.theme_use('clam') # Un thème plus moderne que celui par défaut
style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
style.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

# --- SECTION CPU ---
tk.Label(root, text="Processeur (CPU)", bg=COULEUR_FOND, fg=COULEUR_TEXTE, font=("Arial", 12, "bold")).pack(pady=(15, 5))
label_cpu_val = tk.Label(root, text="0%", bg=COULEUR_FOND, fg=COULEUR_TEXTE)
label_cpu_val.pack()
barre_cpu = ttk.Progressbar(root, length=250, mode='determinate', style="green.Horizontal.TProgressbar")
barre_cpu.pack(pady=5)

# --- SECTION RAM ---
tk.Label(root, text="Mémoire (RAM)", bg=COULEUR_FOND, fg=COULEUR_TEXTE, font=("Arial", 12, "bold")).pack(pady=(15, 5))
label_ram_val = tk.Label(root, text="0%", bg=COULEUR_FOND, fg=COULEUR_TEXTE)
label_ram_val.pack()
barre_ram = ttk.Progressbar(root, length=250, mode='determinate', style="green.Horizontal.TProgressbar")
barre_ram.pack(pady=5)

# --- SECTION BATTERIE ---
tk.Label(root, text="Batterie", bg=COULEUR_FOND, fg=COULEUR_TEXTE, font=("Arial", 12, "bold")).pack(pady=(15, 5))
label_bat_val = tk.Label(root, text="--%", bg=COULEUR_FOND, fg=COULEUR_TEXTE)
label_bat_val.pack()
barre_bat = ttk.Progressbar(root, length=250, mode='determinate', style="green.Horizontal.TProgressbar")
barre_bat.pack(pady=5)

# Lancer la première mise à jour
mettre_a_jour()

# Boucle principale (maintient la fenêtre ouverte)
root.mainloop()