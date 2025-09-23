# player_tools/ui/dice_roller_tab.py
import tkinter as tk
from tkinter import ttk
import random

class FateEdgeDiceRoller:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        # Roll Configuration
        self.config_frame = ttk.LabelFrame(self.frame, text="Roll Configuration", padding="10")
        self.config_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        ttk.Label(self.config_frame, text="Dice Pool:").grid(row=0, column=0, sticky=tk.W)
        self.pool_var = tk.StringVar(value="4")
        self.pool_spin = ttk.Spinbox(self.config_frame, from_=1, to=20, textvariable=self.pool_var, width=5)
        self.pool_spin.grid(row=0, column=1, padx=(5, 0))
        
        ttk.Label(self.config_frame, text="Difficulty (Successes Needed):").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.difficulty_var = tk.StringVar(value="1")
        self.difficulty_spin = ttk.Spinbox(self.config_frame, from_=1, to=10, textvariable=self.difficulty_var, width=5)
        self.difficulty_spin.grid(row=1, column=1, padx=(5, 0), pady=(5, 0))
        
        # Description Ladder
        ttk.Label(self.config_frame, text="Description Quality:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.description_var = tk.StringVar(value="Basic")
        self.description_combo = ttk.Combobox(self.config_frame, textvariable=self.description_var,
                                             values=["Basic", "Detailed", "Intricate"], width=10)
        self.description_combo.grid(row=2, column=1, padx=(5, 0), pady=(5, 0))
        
        # Roll Button
        self.roll_btn = ttk.Button(self.config_frame, text="Roll Dice", command=self.roll_dice)
        self.roll_btn.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        # Results Display
        self.results_frame = ttk.LabelFrame(self.frame, text="Results", padding="10")
        self.results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Dice Results
        ttk.Label(self.results_frame, text="Dice Rolled:").grid(row=0, column=0, sticky=tk.W)
        self.dice_results = tk.Text(self.results_frame, height=3, width=50)
        self.dice_results.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Successes and Complications
        ttk.Label(self.results_frame, text="Successes:").grid(row=2, column=0, sticky=tk.W)
        self.successes_var = tk.StringVar(value="0")
        self.successes_entry = ttk.Entry(self.results_frame, textvariable=self.successes_var, width=10, state="readonly")
        self.successes_entry.grid(row=2, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(self.results_frame, text="Complications (1s):").grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
        self.complications_var = tk.StringVar(value="0")
        self.complications_entry = ttk.Entry(self.results_frame, textvariable=self.complications_var, width=10, state="readonly")
        self.complications_entry.grid(row=3, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        # Outcome
        ttk.Label(self.results_frame, text="Outcome:").grid(row=4, column=0, sticky=tk.W, pady=(5, 0))
        self.outcome_var = tk.StringVar(value="Pending")
        self.outcome_entry = ttk.Entry(self.results_frame, textvariable=self.outcome_var, width=20, state="readonly")
        self.outcome_entry.grid(row=4, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        # Reroll Information
        ttk.Label(self.results_frame, text="Reroll Info:").grid(row=5, column=0, sticky=tk.W, pady=(5, 0))
        self.reroll_text = tk.Text(self.results_frame, height=2, width=50)
        self.reroll_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # History
        self.history_frame = ttk.LabelFrame(self.frame, text="Roll History", padding="10")
        self.history_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.history_text = tk.Text(self.history_frame, height=6, width=60)
        self.history_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(self.history_frame, orient=tk.VERTICAL, command=self.history_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.history_text.configure(yscrollcommand=scrollbar.set)
        
    def roll_dice(self):
        try:
            pool = int(self.pool_var.get())
            difficulty = int(self.difficulty_var.get())
            description = self.description_var.get()
        except ValueError:
            self.outcome_var.set("Invalid Input")
            return
            
        # Roll the dice
        dice = [random.randint(1, 10) for _ in range(pool)]
        
        # Count successes (6 or higher)
        successes = sum(1 for die in dice if die >= 6)
        
        # Count complications (1s)
        complications = dice.count(1)
        
        # Handle rerolls based on description quality
        reroll_info = ""
        if description == "Detailed" and complications > 0:
            # Reroll one 1
            if 1 in dice:
                index = dice.index(1)
                new_roll = random.randint(1, 10)
                dice[index] = new_roll
                reroll_info = f"Rerolled one 1 → {new_roll}\n"
                # Recalculate after reroll
                successes = sum(1 for die in dice if die >= 6)
                complications = dice.count(1)
                
        elif description == "Intricate" and complications > 0:
            # Reroll all 1s
            rerolled = []
            for i, die in enumerate(dice):
                if die == 1:
                    new_roll = random.randint(1, 10)
                    dice[i] = new_roll
                    rerolled.append(new_roll)
            if rerolled:
                reroll_info = f"Rerolled all 1s → {', '.join(map(str, rerolled))}\n"
                # Recalculate after reroll
                successes = sum(1 for die in dice if die >= 6)
                complications = dice.count(1)
                
        # Determine outcome
        if successes >= difficulty and complications == 0:
            outcome = "Clean Success"
        elif successes >= difficulty and complications > 0:
            outcome = "Success with Cost"
        elif 0 < successes < difficulty:
            outcome = "Partial Success"
        elif successes == 0:
            outcome = "Miss"
        else:
            outcome = "Unknown"
            
        # Update UI
        self.dice_results.delete(1.0, tk.END)
        self.dice_results.insert(1.0, ", ".join(map(str, dice)))
        
        self.successes_var.set(str(successes))
        self.complications_var.set(str(complications))
        self.outcome_var.set(outcome)
        
        self.reroll_text.delete(1.0, tk.END)
        self.reroll_text.insert(1.0, reroll_info)
        
        # Add to history
        history_entry = f"Pool: {pool}, DV: {difficulty}, Desc: {description}\n"
        history_entry += f"Dice: {', '.join(map(str, dice))} | Successes: {successes} | Complications: {complications}\n"
        history_entry += f"Outcome: {outcome}\n"
        if reroll_info:
            history_entry += reroll_info
        history_entry += "-" * 50 + "\n"
        
        self.history_text.insert(tk.END, history_entry)
        self.history_text.see(tk.END)
        
    def get_frame(self):
        return self.frame

