# gm_tools/ui/cp_spend_menu_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.database.skill_db import SkillDatabase

class CPSpendMenuTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.cp_pool = 0
        self.banked_cp = 0
        self.create_ui()
        
    def create_ui(self):
        # CP Pool Display
        pool_frame = ttk.LabelFrame(self.frame, text="Complication Points", padding="10")
        pool_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Current CP display
        cp_display_frame = ttk.Frame(pool_frame)
        cp_display_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(cp_display_frame, text="Available CP:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        self.cp_label = ttk.Label(cp_display_frame, text="0", font=("Arial", 12, "bold"), foreground="red")
        self.cp_label.pack(side=tk.LEFT, padx=(5, 20))
        
        ttk.Label(cp_display_frame, text="Banked CP:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        self.banked_label = ttk.Label(cp_display_frame, text="0", font=("Arial", 12, "bold"), foreground="orange")
        self.banked_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # CP Controls
        control_frame = ttk.Frame(pool_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(control_frame, text="Add CP:").pack(side=tk.LEFT)
        self.add_cp_var = tk.StringVar(value="1")
        cp_spinbox = ttk.Spinbox(control_frame, from_=1, to=10, textvariable=self.add_cp_var, width=5)
        cp_spinbox.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Button(control_frame, text="Add to Pool", command=self.add_cp).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="Bank All CP", command=self.bank_cp).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="Clear All", command=self.clear_cp).pack(side=tk.LEFT)
        
        # Spend Options by Suit
        suits_frame = ttk.Frame(self.frame)
        suits_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Hearts - Social/Emotional
        hearts_frame = ttk.LabelFrame(suits_frame, text="♥ Hearts (Social/Emotional)", padding="10")
        hearts_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_spend_options(hearts_frame, [
            ("1 CP", "Rumor cost or faux pas (future –1d with this character)"),
            ("2 CP", "A concession is now required (gift, favor)"),
            ("3 CP", "Someone interjects with leverage"),
            ("4 CP", "Patron turns, audience turns, or oath invoked")
        ], "hearts")
        
        # Swords - Harm/Danger
        swords_frame = ttk.LabelFrame(suits_frame, text="⚔ Swords (Harm/Danger)", padding="10")
        swords_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_spend_options(swords_frame, [
            ("1 CP", "Lose footing (next defense –1d)"),
            ("2 CP", "Weapon or gear becomes Compromised"),
            ("3 CP", "Pinned, disarmed, or separated"),
            ("4+ CP", "Battlefield shifts (fireline, cave-in, cavalry arrives)")
        ], "swords")
        
        # Pentacles - Resources/Material
        pentacles_frame = ttk.LabelFrame(suits_frame, text="♦ Pentacles (Resources/Material)", padding="10")
        pentacles_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_spend_options(pentacles_frame, [
            ("1 CP", "Noise, tell, or trace left; +1 segment on Supply clock"),
            ("2 CP", "Alarmed attention (not full alarm); lose position/cover"),
            ("3 CP", "Reinforcements en route; Out of Supply"),
            ("4+ CP", "Major turn: trap springs, rival claims prize first")
        ], "pentacles")
        
        # Spades - Position/Surveillance
        spades_frame = ttk.LabelFrame(suits_frame, text="♠ Spades (Position/Surveillance)", padding="10")
        spades_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_spend_options(spades_frame, [
            ("1 CP", "Footstep/squeak; shadow seen"),
            ("2 CP", "Patrol path changes; lock resists (extra test)"),
            ("3 CP", "Partial alarm initiated"),
            ("4+ CP", "Full alarm and lockdown protocol")
        ], "spades")
        
        # Universal Options
        universal_frame = ttk.LabelFrame(self.frame, text="Universal CP Options", padding="10")
        universal_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.create_spend_options(universal_frame, [
            ("3 CP", "Key gear breaks now; split party's options"),
            ("4+ CP", "Convert saved CP into scene-defining twist")
        ], "universal")
        
        # Spend History
        history_frame = ttk.LabelFrame(self.frame, text="Recent Spends", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.history_text = tk.Text(history_frame, height=6, wrap=tk.WORD)
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_text.grid(row=0, column=0, sticky="nsew")
        history_scrollbar.grid(row=0, column=1, sticky="ns")
        
        history_frame.grid_rowconfigure(0, weight=1)
        history_frame.grid_columnconfigure(0, weight=1)
        
    def create_spend_options(self, parent, options, category):
        for cost, description in options:
            option_frame = ttk.Frame(parent)
            option_frame.pack(fill=tk.X, pady=2)
            
            # Cost button
            cost_button = ttk.Button(
                option_frame, 
                text=cost, 
                width=8,
                command=lambda c=cost, d=description: self.spend_cp(c, d, category)
            )
            cost_button.pack(side=tk.LEFT, padx=(0, 10))
            
            # Description
            desc_label = ttk.Label(option_frame, text=description, wraplength=600)
            desc_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
    def add_cp(self):
        try:
            amount = int(self.add_cp_var.get())
            self.cp_pool += amount
            self.update_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid CP amount")
            
    def bank_cp(self):
        self.banked_cp += self.cp_pool
        self.cp_pool = 0
        self.update_display()
        
    def clear_cp(self):
        self.cp_pool = 0
        self.banked_cp = 0
        self.update_display()
        
    def spend_cp(self, cost_str, description, category):
        # Parse cost (handle "4+" as 4)
        cost = int(cost_str.split("+")[0])
        
        if self.cp_pool >= cost:
            self.cp_pool -= cost
            self.add_to_history(f"Spent {cost} CP: {description} ({category.title()})")
            self.update_display()
        else:
            # Try to use banked CP
            total_available = self.cp_pool + self.banked_cp
            if total_available >= cost:
                if messagebox.askyesno("Use Banked CP", f"Not enough available CP. Use {cost - self.cp_pool} banked CP?"):
                    needed_from_bank = cost - self.cp_pool
                    self.cp_pool = 0
                    self.banked_cp -= needed_from_bank
                    self.add_to_history(f"Spent {cost} CP (including {needed_from_bank} banked): {description} ({category.title()})")
                    self.update_display()
            else:
                messagebox.showwarning("Insufficient CP", f"Need {cost} CP but only have {total_available} available")
                
    def add_to_history(self, entry):
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.history_text.insert(tk.END, f"[{timestamp}] {entry}\n")
        self.history_text.see(tk.END)
        
    def update_display(self):
        self.cp_label.config(text=str(self.cp_pool))
        self.banked_label.config(text=str(self.banked_cp))
        
    def get_frame(self):
        return self.frame
