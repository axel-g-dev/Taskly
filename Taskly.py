import tkinter as tk
from tkinter import ttk
import psutil
import platform
import datetime
from typing import List, Dict, Any

# --- 🎨 DESIGN SYSTEM (APPLE DARK MODE) ---
class Design:
    # Palette officielle macOS Dark Mode
    BG_WINDOW = "#1C1C1E"    # Fond global (System Gray 6)
    BG_CARD = "#2C2C2E"      # Fond des cartes (System Gray 5)
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#98989D" # Subtext (System Gray)
    
    # Couleurs d'accentuation
    ACCENT_BLUE = "#0A84FF"
    ACCENT_GREEN = "#30D158"
    ACCENT_ORANGE = "#FF9F0A"
    ACCENT_RED = "#FF453A"
    ACCENT_PURPLE = "#BF5AF2"
    
    # Polices (SF Pro simulée)
    FONT_TITLE = ("Helvetica Neue", 18, "bold")
    FONT_SUBTITLE = ("Helvetica Neue", 11, "bold")
    FONT_VALUE = ("Helvetica Neue", 24, "bold")
    FONT_NORMAL = ("Helvetica Neue", 11)
    FONT_MONO = ("Menlo", 10)

# --- 🧠 BACKEND (LOGIQUE) ---
class SystemData:
    def __init__(self):
        self.last_net = psutil.net_io_counters()
        self.cpu_history = [0.0] * 100 # Plus de points pour le grand écran

    def get_stats(self):
        # CPU & RAM
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        
        # Réseau
        net = psutil.net_io_counters()
        down = (net.bytes_recv - self.last_net.bytes_recv) / 1024
        up = (net.bytes_sent - self.last_net.bytes_sent) / 1024
        self.last_net = net
        
        # Historique
        self.cpu_history.pop(0)
        self.cpu_history.append(cpu)
        
        # Batterie
        bat = psutil.sensors_battery()
        bat_pct = bat.percent if bat else 0
        is_plugged = bat.power_plugged if bat else False

        return {
            "cpu": cpu,
            "ram_pct": ram.percent,
            "ram_used": round(ram.used / (1024**3), 1),
            "net_down": down,
            "net_up": up,
            "bat_pct": bat_pct,
            "is_plugged": is_plugged,
            "history": self.cpu_history
        }

    def get_procs(self):
        try:
            # Récupère le Top 15 pour les grands écrans
            procs = sorted(
                psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                key=lambda p: (p.info['cpu_percent'] or 0.0),
                reverse=True
            )
            return procs[:20] 
        except:
            return []

# --- 🧩 COMPOSANTS UI (WIDGETS) ---

class AppleCard(tk.Frame):
    """Une carte style 'Widget iOS' avec un titre et du contenu."""
    def __init__(self, parent, title, icon=""):
        super().__init__(parent, bg=Design.BG_CARD, padx=15, pady=15)
        self.columnconfigure(0, weight=1)
        
        # En-tête de la carte
        header = tk.Frame(self, bg=Design.BG_CARD)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        tk.Label(header, text=f"{icon}  {title}".upper(), fg=Design.TEXT_SECONDARY, 
                 bg=Design.BG_CARD, font=Design.FONT_SUBTITLE, anchor="w").pack(side="left")

    def add_value_label(self, color=Design.TEXT_PRIMARY):
        """Ajoute un gros chiffre au milieu."""
        lbl = tk.Label(self, text="--", font=Design.FONT_VALUE, bg=Design.BG_CARD, fg=color)
        lbl.grid(row=1, column=0, sticky="w")
        return lbl

    def add_sub_label(self):
        """Ajoute un petit texte en dessous."""
        lbl = tk.Label(self, text="--", font=Design.FONT_NORMAL, bg=Design.BG_CARD, fg=Design.TEXT_SECONDARY)
        lbl.grid(row=2, column=0, sticky="w")
        return lbl

class ResizableGraph(tk.Canvas):
    """Un graphique qui s'adapte à la taille de la fenêtre."""
    def __init__(self, parent):
        super().__init__(parent, bg=Design.BG_CARD, highlightthickness=0, height=150)
        self.bind("<Configure>", self.on_resize)
        self.data = []

    def on_resize(self, event):
        self.draw() # Redessiner quand la fenêtre change de taille

    def update_data(self, data):
        self.data = data
        self.draw()

    def draw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10 or not self.data: return

        # Création de la ligne
        step = w / (len(self.data) - 1)
        points = []
        
        # Fond dégradé (simulé par des lignes verticales pour la performance)
        for i, val in enumerate(self.data):
            x = i * step
            y = h - (val / 100 * h)
            points.extend([x, y])
            
            # Indicateur visuel si CPU élevé
            color = Design.ACCENT_GREEN
            if val > 50: color = Design.ACCENT_ORANGE
            if val > 80: color = Design.ACCENT_RED
            
            # Petite barre verticale style "Audio Visualizer"
            self.create_line(x, h, x, y, fill=color, width=2, stipple="gray50")

        # Ligne de courbe lissée au dessus
        if len(points) >= 4:
            self.create_line(points, fill="white", width=2, smooth=True)

class ModernProcessTable(ttk.Treeview):
    """Tableau style Finder."""
    def __init__(self, parent):
        columns = ("pid", "nom", "cpu", "ram")
        super().__init__(parent, columns=columns, show="headings", selectmode="none")
        
        # Configuration des colonnes
        self.heading("pid", text="PID")
        self.heading("nom", text="NOM")
        self.heading("cpu", text="CPU %")
        self.heading("ram", text="RAM %")
        
        self.column("pid", width=50, anchor="center")
        self.column("nom", width=150, anchor="w")
        self.column("cpu", width=70, anchor="e")
        self.column("ram", width=70, anchor="e")
        
        # Styling via ttk
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background=Design.BG_CARD, 
                        foreground=Design.TEXT_PRIMARY, 
                        fieldbackground=Design.BG_CARD,
                        font=Design.FONT_NORMAL,
                        rowheight=25,
                        borderwidth=0)
        style.configure("Treeview.Heading", 
                        background=Design.BG_WINDOW, 
                        foreground=Design.TEXT_SECONDARY, 
                        font=Design.FONT_SUBTITLE,
                        borderwidth=0)
        style.map("Treeview", background=[('selected', Design.BG_CARD)]) # Désactiver la sélection bleue moche

# --- 🚀 APPLICATION PRINCIPALE ---
class TasklyApp:
    def __init__(self, root):
        self.root = root
        self.data_manager = SystemData()
        self.setup_window()
        self.build_ui()
        self.update_loop()

    def setup_window(self):
        self.root.title("Taskly Pro")
        self.root.geometry("1000x700") # Taille de départ large
        self.root.minsize(800, 600)
        self.root.configure(bg=Design.BG_WINDOW)
        
        # Configuration de la grille responsive
        # Colonne 0 = 1/3, Colonne 1 = 1/3, Colonne 2 = 1/3
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        # Ligne 1 (stats) fix, Ligne 2 (graph/table) prend le reste
        self.root.rowconfigure(1, weight=1) 

    def build_ui(self):
        # 1. Header
        header = tk.Frame(self.root, bg=Design.BG_WINDOW)
        header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=20, pady=20)
        
        tk.Label(header, text=f"{platform.node().split('.')[0]}", 
                 font=Design.FONT_TITLE, fg=Design.TEXT_PRIMARY, bg=Design.BG_WINDOW).pack(side="left")
        
        self.lbl_clock = tk.Label(header, text="--:--", font=Design.FONT_TITLE, 
                                  fg=Design.TEXT_SECONDARY, bg=Design.BG_WINDOW)
        self.lbl_clock.pack(side="right")

        # 2. Cartes de Stats (Ligne 1)
        # CPU Card
        self.card_cpu = AppleCard(self.root, "Processeur", "🧠")
        self.card_cpu.grid(row=1, column=0, sticky="ew", padx=(20, 10), pady=10)
        self.lbl_cpu_val = self.card_cpu.add_value_label(Design.ACCENT_BLUE)
        self.lbl_cpu_sub = self.card_cpu.add_sub_label()

        # RAM Card
        self.card_ram = AppleCard(self.root, "Mémoire", "💾")
        self.card_ram.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        self.lbl_ram_val = self.card_ram.add_value_label(Design.ACCENT_PURPLE)
        self.lbl_ram_sub = self.card_ram.add_sub_label()

        # Battery/Net Card
        self.card_misc = AppleCard(self.root, "Système", "⚡")
        self.card_misc.grid(row=1, column=2, sticky="ew", padx=(10, 20), pady=10)
        self.lbl_misc_val = self.card_misc.add_value_label(Design.ACCENT_GREEN)
        self.lbl_misc_sub = self.card_misc.add_sub_label()

        # 3. Zone Contenu Principal (Ligne 2 - Expandable)
        # On divise le bas en deux colonnes principales
        
        # Container Graphique (Gauche, prend 2/3 de la largeur si possible)
        graph_container = tk.Frame(self.root, bg=Design.BG_CARD)
        graph_container.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=(20, 10), pady=(10, 20))
        
        tk.Label(graph_container, text="HISTORIQUE D'ACTIVITÉ", font=Design.FONT_SUBTITLE, 
                 bg=Design.BG_CARD, fg=Design.TEXT_SECONDARY).pack(anchor="w", padx=15, pady=15)
        
        self.graph = ResizableGraph(graph_container)
        self.graph.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Container Processus (Droite, prend 1/3)
        list_container = tk.Frame(self.root, bg=Design.BG_CARD)
        list_container.grid(row=2, column=2, sticky="nsew", padx=(10, 20), pady=(10, 20))
        
        tk.Label(list_container, text="APPS GOURMANDES", font=Design.FONT_SUBTITLE, 
                 bg=Design.BG_CARD, fg=Design.TEXT_SECONDARY).pack(anchor="w", padx=15, pady=15)
        
        self.proc_table = ModernProcessTable(list_container)
        self.proc_table.pack(fill="both", expand=True, padx=5, pady=5)

    def update_loop(self):
        # Récupération données
        data = self.data_manager.get_stats()
        procs = self.data_manager.get_procs()
        
        # Mise à jour Clock
        self.lbl_clock.config(text=datetime.datetime.now().strftime("%H:%M:%S"))

        # Mise à jour Cartes
        self.lbl_cpu_val.config(text=f"{data['cpu']}%")
        self.lbl_cpu_sub.config(text="Utilisation Totale")

        self.lbl_ram_val.config(text=f"{data['ram_pct']}%")
        self.lbl_ram_sub.config(text=f"{data['ram_used']} GB utilisés")
        
        plugged_icon = "⚡" if data['is_plugged'] else "🔋"
        self.lbl_misc_val.config(text=f"{data['bat_pct']}%")
        self.lbl_misc_sub.config(text=f"{plugged_icon} Batterie | ⬇ {data['net_down']:.1f} KB/s")

        # Mise à jour Graphique
        self.graph.update_data(data['history'])

        # Mise à jour Table (On efface et on réécrit, méthode simple)
        for item in self.proc_table.get_children():
            self.proc_table.delete(item)
            
        for p in procs:
            try:
                self.proc_table.insert("", "end", values=(
                    p.info['pid'],
                    p.info['name'],
                    f"{p.info['cpu_percent'] or 0.0:.1f}%",
                    f"{p.info['memory_percent'] or 0.0:.1f}%"
                ))
            except: pass

        # Rappel 1000ms
        self.root.after(1000, self.update_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = TasklyApp(root)
    root.mainloop()