# ui/campaign_clock_tab.py
import tkinter as tk
from tkinter import ttk

class CampaignClockTab:
    def __init__(self, parent):
        self.parent = parent
        self.mandate = 0  # 0-6
        self.crisis = 0   # 0-6
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Campaign Clocks", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Clock Controls
        control_frame = ttk.Frame(self.parent)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(control_frame, text="Reset All Clocks", command=self.reset_clocks).pack(side="left", padx=5)
        
        # Mandate Clock
        mandate_frame = ttk.LabelFrame(self.parent, text="Mandate Clock (0-6) - Public Legitimacy", padding="15")
        mandate_frame.pack(fill="x", padx=20, pady=10)
        
        self.mandate_label = ttk.Label(mandate_frame, text=f"Mandate: {self.mandate}/6", font=("Arial", 14, "bold"))
        self.mandate_label.pack(pady=5)
        
        self.mandate_canvas = tk.Canvas(mandate_frame, width=300, height=40)
        self.mandate_canvas.pack(pady=10)
        self.draw_mandate_clock()
        
        mandate_btn_frame = ttk.Frame(mandate_frame)
        mandate_btn_frame.pack()
        ttk.Button(mandate_btn_frame, text="+", width=3, command=self.add_mandate).pack(side="left", padx=5)
        ttk.Button(mandate_btn_frame, text="-", width=3, command=self.reduce_mandate).pack(side="left", padx=5)
        ttk.Button(mandate_btn_frame, text="Set to 6", command=lambda: self.set_mandate(6)).pack(side="left", padx=5)
        
        # Crisis Clock
        crisis_frame = ttk.LabelFrame(self.parent, text="Crisis Clock (0-6) - Opposition Engine", padding="15")
        crisis_frame.pack(fill="x", padx=20, pady=10)
        
        self.crisis_label = ttk.Label(crisis_frame, text=f"Crisis: {self.crisis}/6", font=("Arial", 14, "bold"))
        self.crisis_label.pack(pady=5)
        
        self.crisis_canvas = tk.Canvas(crisis_frame, width=300, height=40)
        self.crisis_canvas.pack(pady=10)
        self.draw_crisis_clock()
        
        crisis_btn_frame = ttk.Frame(crisis_frame)
        crisis_btn_frame.pack()
        ttk.Button(crisis_btn_frame, text="+", width=3, command=self.add_crisis).pack(side="left", padx=5)
        ttk.Button(crisis_btn_frame, text="-", width=3, command=self.reduce_crisis).pack(side="left", padx=5)
        ttk.Button(crisis_btn_frame, text="Set to 6", command=lambda: self.set_crisis(6)).pack(side="left", padx=5)
        
        # Finale Status
        finale_frame = ttk.LabelFrame(self.parent, text="Finale Status", padding="15")
        finale_frame.pack(fill="x", padx=20, pady=10)
        
        self.finale_label = ttk.Label(finale_frame, text="", font=("Arial", 12, "bold"), foreground="blue")
        self.finale_label.pack(pady=5)
        self.update_finale_status()
        
        # Campaign Info
        info_frame = ttk.LabelFrame(self.parent, text="Campaign Clock Information", padding="10")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
Mandate Clock (0-6): Tracks public legitimacy and buy-in for the Crown.
• Higher values = More favorable finale conditions
• Player-called finale: Mandate ≥ 6 and Crisis ≤ 3

Crisis Clock (0-6): Tracks opposition engine (rivals, pressure rails, attrition).
• Higher values = More hostile finale conditions
• Forced finale: Crisis ≥ 6 (regardless of Mandate)

Finale Triggers:
• Player-called: Mandate ≥ 6, Crisis ≤ 3
• Forced: Crisis ≥ 6
• Balanced: Both 4-5 (start rails at +1)
        """.strip()
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack()
        
    def draw_mandate_clock(self):
        self.mandate_canvas.delete("all")
        
        # Draw empty segments
        for i in range(6):
            x1 = 20 + i * 45
            y1 = 10
            x2 = x1 + 40
            y2 = 30
            
            # Fill color based on whether segment is filled
            if i < self.mandate:
                color = "green"  # Filled segments
            else:
                color = "lightgray"  # Empty segments
                
            self.mandate_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=1)
            
    def draw_crisis_clock(self):
        self.crisis_canvas.delete("all")
        
        # Draw empty segments
        for i in range(6):
            x1 = 20 + i * 45
            y1 = 10
            x2 = x1 + 40
            y2 = 30
            
            # Fill color based on whether segment is filled
            if i < self.crisis:
                color = "red"  # Filled segments
            else:
                color = "lightgray"  # Empty segments
                
            self.crisis_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=1)
            
    def add_mandate(self):
        if self.mandate < 6:
            self.mandate += 1
            self.update_displays()
            
    def reduce_mandate(self):
        if self.mandate > 0:
            self.mandate -= 1
            self.update_displays()
            
    def set_mandate(self, value):
        self.mandate = max(0, min(6, value))
        self.update_displays()
            
    def add_crisis(self):
        if self.crisis < 6:
            self.crisis += 1
            self.update_displays()
            
    def reduce_crisis(self):
        if self.crisis > 0:
            self.crisis -= 1
            self.update_displays()
            
    def set_crisis(self, value):
        self.crisis = max(0, min(6, value))
        self.update_displays()
            
    def reset_clocks(self):
        self.mandate = 0
        self.crisis = 0
        self.update_displays()
        
    def update_displays(self):
        self.mandate_label.config(text=f"Mandate: {self.mandate}/6")
        self.crisis_label.config(text=f"Crisis: {self.crisis}/6")
        self.draw_mandate_clock()
        self.draw_crisis_clock()
        self.update_finale_status()
        
    def update_finale_status(self):
        if self.mandate >= 6 and self.crisis <= 3:
            status = "READY FOR PLAYER-CALLED FINALE"
            color = "green"
        elif self.crisis >= 6:
            status = "CRISIS THRESHOLD REACHED - FORCED FINALE IMMINENT"
            color = "red"
        elif 4 <= self.mandate <= 5 and 4 <= self.crisis <= 5:
            status = "BALANCED CAMPAIGN - FINALE WILL START RAILS AT +1"
            color = "orange"
        else:
            status = "CAMPAIGN IN PROGRESS"
            color = "blue"
            
        self.finale_label.config(text=status, foreground=color)
