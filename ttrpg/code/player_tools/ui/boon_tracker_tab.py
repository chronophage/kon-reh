# player_tools/ui/boon_tracker_tab.py
import tkinter as tk
from tkinter import ttk

class PlayerBoonTrackerTab:
    def __init__(self, parent):
        self.parent = parent
        self.boons = 0  # 0-5
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Boon Tracker", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Boon Count
        count_frame = ttk.Frame(self.parent)
        count_frame.pack(pady=20)
        
        ttk.Label(count_frame, text="Your Boons:", font=("Arial", 14, "bold")).pack()
        self.boon_count_label = ttk.Label(count_frame, text=f"{self.boons}/5", 
                                        font=("Arial", 20, "bold"),
                                        foreground="gold")
        self.boon_count_label.pack(pady=10)
        
        # Visual Boon Indicators
        visual_frame = ttk.Frame(self.parent)
        visual_frame.pack(pady=20)
        
        self.boon_canvas = tk.Canvas(visual_frame, width=300, height=60)
        self.boon_canvas.pack()
        self.draw_boon_visual()
        
        # Boon Controls
        control_frame = ttk.Frame(self.parent)
        control_frame.pack(pady=20)
        
        ttk.Button(control_frame, text="Earn Boon", 
                  command=self.earn_boon).pack(side="left", padx=10)
        ttk.Button(control_frame, text="Spend Boon", 
                  command=self.spend_boon).pack(side="left", padx=10)
        ttk.Button(control_frame, text="Reset Boons", 
                  command=self.reset_boons).pack(side="left", padx=10)
        
        # Boon Actions
        actions_frame = ttk.LabelFrame(self.parent, text="Boon Actions", padding="15")
        actions_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(actions_frame, text="Spend for Re-roll", 
                  command=self.spend_for_reroll).pack(pady=5)
        ttk.Button(actions_frame, text="Spend for Asset Activation", 
                  command=self.spend_for_asset).pack(pady=5)
        ttk.Button(actions_frame, text="Convert to XP (2 → 1)", 
                  command=self.convert_to_xp).pack(pady=5)
        
        # Boon Info
        info_frame = ttk.LabelFrame(self.parent, text="Boon Information", padding="10")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
Boon System:
• Maximum 5 boons at any time
• Earn boons from meaningful failure and complications
• Spend boons for:
  - Re-rolling a single die (1 boon)
  - Activating Off-Screen Assets (1 boon preferred)
  - Converting to XP (2 boons = 1 XP)

Overflow Management:
• When you would earn a 6th boon, convert 2 boons to 1 XP
• This happens automatically in full implementation

Design Philosophy:
• Boons ensure failure still rewards play
• They turn setbacks into fuel for later triumphs
• Every boon represents a lesson paid for with genuine dramatic weight
        """.strip()
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack()
        
    def draw_boon_visual(self):
        self.boon_canvas.delete("all")
        
        # Draw boon indicators
        for i in range(5):
            x = 30 + i * 55
            y = 30
            
            # Fill color based on whether boon is available
            if i < self.boons:
                color = "gold"  # Available boons
                outline = "black"
            else:
                color = "lightgray"  # Empty slots
                outline = "gray"
                
            # Draw boon as a circle
            self.boon_canvas.create_oval(x-15, y-15, x+15, y+15, 
                                       fill=color, outline=outline, width=2)
            
            # Add star symbol for boons
            if i < self.boons:
                self.boon_canvas.create_text(x, y, text="★", font=("Arial", 16, "bold"))
                
    def earn_boon(self):
        if self.boons < 5:
            self.boons += 1
            self.update_boon_display()
        # In full implementation, handle overflow (6th boon converts 2→1 XP)
            
    def spend_boon(self):
        if self.boons > 0:
            self.boons -= 1
            self.update_boon_display()
            
    def reset_boons(self):
        self.boons = 0
        self.update_boon_display()
        
    def spend_for_reroll(self):
        if self.boons > 0:
            self.boons -= 1
            self.update_boon_display()
            print("Boon spent for re-roll")
            
    def spend_for_asset(self):
        if self.boons > 0:
            self.boons -= 1
            self.update_boon_display()
            print("Boon spent for asset activation")
            
    def convert_to_xp(self):
        if self.boons >= 2:
            self.boons -= 2
            self.update_boon_display()
            print("2 boons converted to 1 XP")
            
    def update_boon_display(self):
        self.boon_count_label.config(text=f"{self.boons}/5", 
                                   foreground="gold" if self.boons > 0 else "gray")
        self.draw_boon_visual()

