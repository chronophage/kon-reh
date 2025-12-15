# ui/combat_tracker_tab.py
import tkinter as tk
from tkinter import ttk

class CombatTrackerTab:
    def __init__(self, parent):
        self.parent = parent
        self.combatants = []  # List of combatant dictionaries
        self.current_round = 1
        self.active_combatant_index = 0
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Combat Tracker", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Combat Controls
        control_frame = ttk.Frame(self.parent)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(control_frame, text="New Combat", command=self.new_combat).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Next Round", command=self.next_round).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Previous Round", command=self.previous_round).pack(side="left", padx=5)
        ttk.Button(control_frame, text="End Combat", command=self.end_combat).pack(side="left", padx=5)
        
        # Round Display
        self.round_label = ttk.Label(control_frame, text=f"Round: {self.current_round}", font=("Arial", 12, "bold"))
        self.round_label.pack(side="right", padx=10)
        
        # Add Combatant Section
        add_frame = ttk.LabelFrame(self.parent, text="Add Combatant", padding="10")
        add_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5)
        self.name_entry = ttk.Entry(add_frame, width=15)
        self.name_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(add_frame, text="Initiative:").grid(row=0, column=2, sticky="w", padx=5)
        self.init_entry = ttk.Entry(add_frame, width=5)
        self.init_entry.grid(row=0, column=3, padx=5)
        
        ttk.Label(add_frame, text="Position:").grid(row=0, column=4, sticky="w", padx=5)
        self.position_var = tk.StringVar(value="Controlled")
        position_combo = ttk.Combobox(add_frame, textvariable=self.position_var, 
                                    values=["Controlled", "Controlled", "Dangerous"], width=10, state="readonly")
        position_combo.grid(row=0, column=5, padx=5)
        
        ttk.Button(add_frame, text="Add Combatant", command=self.add_combatant).grid(row=0, column=6, padx=10)
        
        # Combatants Display
        self.combatants_frame = ttk.Frame(self.parent)
        self.combatants_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Combat Info
        info_frame = ttk.LabelFrame(self.parent, text="Combat Information", padding="10")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
Position Effects:
• Controlled: +1 die on all rolls
• Controlled: Standard positioning
• Dangerous: -1 die on all rolls

Rail Tracking:
• Hunt/Escort: Pursuit or protection scenarios
• Escape/Containment: Getting away or holding ground
• Hazard/Sanctity: Environmental threats or sacred spaces
• Curfew/Assembly: Time pressure or crowd dynamics
• Crowd/Solitude: Social pressure or isolation
        """.strip()
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack()
        
        self.refresh_display()
        
    def new_combat(self):
        self.combatants = []
        self.current_round = 1
        self.active_combatant_index = 0
        self.round_label.config(text=f"Round: {self.current_round}")
        self.refresh_display()
        
    def next_round(self):
        self.current_round += 1
        self.active_combatant_index = 0
        self.round_label.config(text=f"Round: {self.current_round}")
        self.refresh_display()
        
    def previous_round(self):
        if self.current_round > 1:
            self.current_round -= 1
            self.active_combatant_index = 0
            self.round_label.config(text=f"Round: {self.current_round}")
            self.refresh_display()
            
    def end_combat(self):
        self.new_combat()
        
    def add_combatant(self):
        name = self.name_entry.get().strip()
        init_str = self.init_entry.get().strip()
        
        if name and init_str:
            try:
                initiative = int(init_str)
                combatant = {
                    "name": name,
                    "initiative": initiative,
                    "position": self.position_var.get(),
                    "fatigue": 0,
                    "cp": 0,  # Story Beats
                    "active": True
                }
                self.combatants.append(combatant)
                self.combatants.sort(key=lambda x: x["initiative"], reverse=True)
                self.name_entry.delete(0, tk.END)
                self.init_entry.delete(0, tk.END)
                self.refresh_display()
            except ValueError:
                pass  # Invalid initiative value
                
    def refresh_display(self):
        # Clear existing widgets
        for widget in self.combatants_frame.winfo_children():
            widget.destroy()
            
        if not self.combatants:
            ttk.Label(self.combatants_frame, text="No combatants added").pack(pady=20)
            return
            
        # Create combatant controls
        for i, combatant in enumerate(self.combatants):
            is_active = (i == self.active_combatant_index and self.combatants)
            bg_color = "lightblue" if is_active else "white"
            
            combatant_frame = ttk.Frame(self.combatants_frame, relief="solid", borderwidth=1)
            combatant_frame.pack(fill="x", pady=2, padx=5)
            combatant_frame.configure(style="Card.TFrame")
            
            # Name and Initiative
            name_label = ttk.Label(combatant_frame, text=f"{combatant['name']} (Init: {combatant['initiative']})", 
                                 font=("Arial", 10, "bold"))
            name_label.pack(side="left", padx=10, pady=5)
            
            # Position
            position_label = ttk.Label(combatant_frame, 
                                     text=f"Position: {combatant['position']}", 
                                     foreground=self.get_position_color(combatant['position']))
            position_label.pack(side="left", padx=10)
            
            # Fatigue and (SB)
            status_frame = ttk.Frame(combatant_frame)
            status_frame.pack(side="left", padx=10)
            
            ttk.Label(status_frame, text=f"Fatigue: {combatant['fatigue']}").pack(side="left")
            ttk.Label(status_frame, text=f" | (SB): {combatant['cp']}").pack(side="left", padx=(5,0))
            
            # Controls
            btn_frame = ttk.Frame(combatant_frame)
            btn_frame.pack(side="right", padx=10)
            
            # Position controls
            pos_frame = ttk.Frame(btn_frame)
            pos_frame.pack(side="left", padx=5)
            ttk.Button(pos_frame, text="▲", width=2, command=lambda idx=i: self.change_position(idx, 1)).pack()
            ttk.Button(pos_frame, text="▼", width=2, command=lambda idx=i: self.change_position(idx, -1)).pack()
            
            # Fatigue controls
            fatigue_frame = ttk.Frame(btn_frame)
            fatigue_frame.pack(side="left", padx=5)
            ttk.Button(fatigue_frame, text="F+", width=3, command=lambda idx=i: self.add_fatigue(idx)).pack(side="left")
            ttk.Button(fatigue_frame, text="F-", width=3, command=lambda idx=i: self.reduce_fatigue(idx)).pack(side="left")
            
            # (SB) controls
            cp_frame = ttk.Frame(btn_frame)
            cp_frame.pack(side="left", padx=5)
            ttk.Button(cp_frame, text="(SB)+", width=4, command=lambda idx=i: self.add_cp(idx)).pack(side="left")
            ttk.Button(cp_frame, text="(SB)-", width=4, command=lambda idx=i: self.reduce_cp(idx)).pack(side="left")
            
            # Remove button
            ttk.Button(btn_frame, text="Remove", command=lambda idx=i: self.remove_combatant(idx)).pack(side="left", padx=5)
            
            # Active indicator
            if is_active:
                ttk.Label(btn_frame, text="ACTIVE", foreground="red", font=("Arial", 8, "bold")).pack(side="left", padx=5)
                
    def get_position_color(self, position):
        colors = {
            "Controlled": "green",
            "Controlled": "orange",
            "Dangerous": "red"
        }
        return colors.get(position, "black")
        
    def change_position(self, index, direction):
        if 0 <= index < len(self.combatants):
            positions = ["Controlled", "Controlled", "Dangerous"]
            current_pos = self.combatants[index]["position"]
            current_idx = positions.index(current_pos)
            new_idx = max(0, min(len(positions)-1, current_idx + direction))
            self.combatants[index]["position"] = positions[new_idx]
            self.refresh_display()
            
    def add_fatigue(self, index):
        if 0 <= index < len(self.combatants) and self.combatants[index]["fatigue"] < 4:
            self.combatants[index]["fatigue"] += 1
            self.refresh_display()
            
    def reduce_fatigue(self, index):
        if 0 <= index < len(self.combatants) and self.combatants[index]["fatigue"] > 0:
            self.combatants[index]["fatigue"] -= 1
            self.refresh_display()
            
    def add_cp(self, index):
        if 0 <= index < len(self.combatants):
            self.combatants[index]["cp"] += 1
            self.refresh_display()
            
    def reduce_cp(self, index):
        if 0 <= index < len(self.combatants) and self.combatants[index]["cp"] > 0:
            self.combatants[index]["cp"] -= 1
            self.refresh_display()
            
    def remove_combatant(self, index):
        if 0 <= index < len(self.combatants):
            del self.combatants[index]
            if self.active_combatant_index >= len(self.combatants) and self.combatants:
                self.active_combatant_index = max(0, len(self.combatants) - 1)
            self.refresh_display()
