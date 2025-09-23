# dice_roller_tab.py
import tkinter as tk
from tkinter import ttk
import random
from data.database import Database

class DiceRollerTab:
    def __init__(self, parent):
        self.parent = parent
        self.db = Database()
        self.banked_cp = 0
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Dice Roller", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Dice pool input
        pool_frame = ttk.Frame(self.parent)
        pool_frame.pack(pady=10)
        
        ttk.Label(pool_frame, text="Dice Pool:", font=("Arial", 16)).pack(side=tk.LEFT)
        self.pool_entry = ttk.Entry(pool_frame, width=5, font=("Arial", 14))
        self.pool_entry.pack(side=tk.LEFT, padx=10)
        self.pool_entry.insert(0, "4")
        
        # Description level
        desc_frame = ttk.Frame(self.parent)
        desc_frame.pack(pady=10)
        
        ttk.Label(desc_frame, text="Description Level:", font=("Arial", 14)).pack(side=tk.LEFT)
        self.desc_var = tk.StringVar(value="Basic")
        desc_combo = ttk.Combobox(desc_frame, textvariable=self.desc_var, 
                                 values=["Basic", "Detailed", "Intricate"], 
                                 state="readonly", font=("Arial", 12), width=12)
        desc_combo.pack(side=tk.LEFT, padx=10)
        
        # Roll button
        roll_btn = ttk.Button(self.parent, text="Roll Dice", command=self.roll_dice, 
                             style="Huge.TButton")
        roll_btn.pack(pady=20)
        
        # Results display
        results_frame = ttk.LabelFrame(self.parent, text="Results", padding="10")
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create a text widget with scrollbar for results
        self.results_text = tk.Text(results_frame, height=15, width=60, font=("Arial", 12))
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Banked CP display
        cp_frame = ttk.Frame(self.parent)
        cp_frame.pack(pady=10)
        
        ttk.Label(cp_frame, text="Banked CP:", font=("Arial", 14)).pack(side=tk.LEFT)
        self.cp_label = ttk.Label(cp_frame, text="0", font=("Arial", 14, "bold"))
        self.cp_label.pack(side=tk.LEFT, padx=10)
        
        # CP buttons
        cp_btn_frame = ttk.Frame(self.parent)
        cp_btn_frame.pack(pady=5)
        
        ttk.Button(cp_btn_frame, text="Bank CP", command=self.bank_cp).pack(side=tk.LEFT, padx=5)
        ttk.Button(cp_btn_frame, text="Clear Banked CP", command=self.clear_banked_cp).pack(side=tk.LEFT, padx=5)
        
    def roll_dice(self):
        try:
            pool_size = int(self.pool_entry.get())
            if pool_size <= 0:
                self.display_result("Error: Dice pool must be positive!")
                return
        except ValueError:
            self.display_result("Error: Invalid dice pool value!")
            return
            
        # Roll the dice
        rolls = [random.randint(1, 10) for _ in range(pool_size)]
        successes = sum(1 for roll in rolls if roll >= 6)
        complications = sum(1 for roll in rolls if roll == 1)
        
        # Apply description level benefits
        desc_level = self.desc_var.get()
        rerolled_ones = 0
        
        if desc_level == "Detailed" and complications > 0:
            # Re-roll one 1
            rerolled_ones = 1
            complications -= 1
            # Add new roll result
            new_roll = random.randint(1, 10)
            rolls.append(f"({new_roll} reroll)")
            if new_roll >= 6:
                successes += 1
            elif new_roll == 1:
                complications += 1
                
        elif desc_level == "Intricate" and complications > 0:
            # Re-roll all 1s
            rerolled_ones = complications
            complications = 0
            for _ in range(rerolled_ones):
                new_roll = random.randint(1, 10)
                rolls.append(f"({new_roll} reroll)")
                if new_roll >= 6:
                    successes += 1
                elif new_roll == 1:
                    complications += 1
        
        # Display results
        result_text = f"Dice Pool: {pool_size}\n"
        result_text += f"Description Level: {desc_level}\n"
        result_text += f"Rolls: {', '.join(str(r) for r in rolls if isinstance(r, int))}"
        if rerolled_ones > 0:
            reroll_rolls = [r for r in rolls if isinstance(r, str)]
            result_text += f" + {', '.join(reroll_rolls)}"
        result_text += f"\nSuccesses: {successes}\n"
        result_text += f"Complications (1s): {complications}\n"
        
        # Outcome interpretation based on Fate's Edge rules
        if successes > 0 and complications == 0:
            result_text += "Outcome: Clean Success\n"
        elif successes > 0 and complications > 0:
            result_text += "Outcome: Success & Cost\n"
        elif successes == 0 and complications > 0:
            result_text += "Outcome: Miss (No progress)\n"
        else:
            result_text += "Outcome: Partial Progress\n"
            
        if rerolled_ones > 0:
            result_text += f"Rerolled {rerolled_ones} ones due to {desc_level} description.\n"
            
        result_text += "-" * 50 + "\n"
        
        self.display_result(result_text)
        
    def display_result(self, text):
        self.results_text.insert("1.0", text + "\n")
        self.results_text.see("1.0")
        
    def bank_cp(self):
        # For simplicity, we'll bank 1 CP when this button is pressed
        # In a full implementation, you'd track actual CP from rolls
        self.banked_cp += 1
        self.cp_label.config(text=str(self.banked_cp))
        
    def clear_banked_cp(self):
        self.banked_cp = 0
        self.cp_label.config(text=str(self.banked_cp))
