# ui/fatigue_tracker_tab.py
import tkinter as tk
from tkinter import ttk

class FatigueTrackerTab:
    def __init__(self, parent):
        self.parent = parent
        self.players = {}  # {name: fatigue_level}
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Fatigue Tracker", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Add Player Section
        add_frame = ttk.LabelFrame(self.parent, text="Add Player", padding="10")
        add_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(add_frame, text="Player Name:").pack(side="left")
        self.player_entry = ttk.Entry(add_frame, width=20)
        self.player_entry.pack(side="left", padx=5)
        ttk.Button(add_frame, text="Add Player", command=self.add_player).pack(side="left", padx=5)
        
        # Players Display
        self.players_frame = ttk.Frame(self.parent)
        self.players_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Fatigue Info
        info_frame = ttk.LabelFrame(self.parent, text="Fatigue Effects", padding="10")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
Fatigue Effects:
• 1 Fatigue: Re-roll one success on next roll
• 2 Fatigue: Re-roll one success on each roll
• 3 Fatigue: Re-roll two successes on each roll
• 4 Fatigue: Collapse/KO - Out of scene until treated

Clearing Fatigue:
• Safe rest with adequate Supply removes 1 level
• Cannot clear Fatigue if party Supply is Dangerously Low or Empty

Sources of Fatigue:
• (SB) spends by GM
• Exhaustion from travel or exertion
• Harsh conditions or lack of rest
• Magical or supernatural effects
        """.strip()
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack()
        
        self.refresh_display()
        
    def add_player(self):
        name = self.player_entry.get().strip()
        if name and name not in self.players:
            self.players[name] = 0
            self.player_entry.delete(0, tk.END)
            self.refresh_display()
            
    def refresh_display(self):
        # Clear existing widgets
        for widget in self.players_frame.winfo_children():
            widget.destroy()
            
        # Create player controls
        for name, fatigue in self.players.items():
            player_frame = ttk.LabelFrame(self.players_frame, text=name, padding="10")
            player_frame.pack(fill="x", pady=5)
            
            # Fatigue display
            fatigue_frame = ttk.Frame(player_frame)
            fatigue_frame.pack(side="left")
            
            fatigue_label = ttk.Label(fatigue_frame, text=f"Fatigue Level: {fatigue}", font=("Arial", 12, "bold"))
            fatigue_label.pack()
            
            # Visual fatigue indicators
            visual_frame = ttk.Frame(fatigue_frame)
            visual_frame.pack(pady=5)
            
            for i in range(4):
                color = "orange" if i < fatigue else "lightgray"
                canvas = tk.Canvas(visual_frame, width=25, height=25)
                canvas.pack(side="left", padx=2)
                canvas.create_oval(5, 5, 20, 20, fill=color, outline="black")
                
            # Effect description
            effect_text = self.get_fatigue_effect(fatigue)
            effect_label = ttk.Label(fatigue_frame, text=effect_text, foreground="red" if fatigue > 0 else "green")
            effect_label.pack(pady=(5,0))
            
            # Control buttons
            btn_frame = ttk.Frame(player_frame)
            btn_frame.pack(side="right")
            
            ttk.Button(btn_frame, text="+", width=3, command=lambda n=name: self.add_fatigue(n)).pack(side="left", padx=2)
            ttk.Button(btn_frame, text="-", width=3, command=lambda n=name: self.reduce_fatigue(n)).pack(side="left", padx=2)
            ttk.Button(btn_frame, text="Reset", command=lambda n=name: self.reset_fatigue(n)).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="Remove", command=lambda n=name: self.remove_player(n)).pack(side="left", padx=5)
            
        if not self.players:
            ttk.Label(self.players_frame, text="No players added").pack(pady=20)
            
    def get_fatigue_effect(self, level):
        effects = {
            0: "No penalty",
            1: "Re-roll 1 success next roll",
            2: "Re-roll 1 success each roll",
            3: "Re-roll 2 successes each roll",
            4: "KO - Out of scene until treated"
        }
        return effects.get(level, "Invalid fatigue level")
        
    def add_fatigue(self, name):
        if name in self.players and self.players[name] < 4:
            self.players[name] += 1
            self.refresh_display()
            
    def reduce_fatigue(self, name):
        if name in self.players and self.players[name] > 0:
            self.players[name] -= 1
            self.refresh_display()
            
    def reset_fatigue(self, name):
        if name in self.players:
            self.players[name] = 0
            self.refresh_display()
            
    def remove_player(self, name):
        if name in self.players:
            del self.players[name]
            self.refresh_display()
