# player_tools/ui/condition_tracker_tab.py
import tkinter as tk
from tkinter import ttk

class ConditionTrackerTab:
    def __init__(self, parent):
        self.parent = parent
        self.fatigue = 0  # 0-4
        self.supply_segments = 0  # 0-4
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Condition Tracker", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Fatigue Tracker
        fatigue_frame = ttk.LabelFrame(self.parent, text="Fatigue Tracker", padding="15")
        fatigue_frame.pack(fill="x", padx=20, pady=10)
        
        # Fatigue Level
        level_frame = ttk.Frame(fatigue_frame)
        level_frame.pack(fill="x", pady=10)
        
        ttk.Label(level_frame, text="Fatigue Level:", font=("Arial", 12, "bold")).pack(side="left")
        self.fatigue_label = ttk.Label(level_frame, text=f"{self.fatigue}/4", 
                                     font=("Arial", 14, "bold"),
                                     foreground="orange" if self.fatigue > 0 else "green")
        self.fatigue_label.pack(side="left", padx=10)
        
        # Visual Fatigue Indicators
        visual_frame = ttk.Frame(fatigue_frame)
        visual_frame.pack(pady=10)
        
        self.fatigue_canvas = tk.Canvas(visual_frame, width=200, height=40)
        self.fatigue_canvas.pack()
        self.draw_fatigue_visual()
        
        # Fatigue Controls
        fatigue_control_frame = ttk.Frame(fatigue_frame)
        fatigue_control_frame.pack(pady=10)
        
        ttk.Button(fatigue_control_frame, text="Add Fatigue", 
                  command=self.add_fatigue).pack(side="left", padx=5)
        ttk.Button(fatigue_control_frame, text="Reduce Fatigue", 
                  command=self.reduce_fatigue).pack(side="left", padx=5)
        ttk.Button(fatigue_control_frame, text="Reset Fatigue", 
                  command=self.reset_fatigue).pack(side="left", padx=5)
        
        # Fatigue Effect
        self.fatigue_effect_label = ttk.Label(fatigue_frame, text=self.get_fatigue_effect(), 
                                            font=("Arial", 10, "italic"))
        self.fatigue_effect_label.pack(pady=5)
        
        # Supply Clock
        supply_frame = ttk.LabelFrame(self.parent, text="Supply Clock", padding="15")
        supply_frame.pack(fill="x", padx=20, pady=10)
        
        # Supply Level
        supply_level_frame = ttk.Frame(supply_frame)
        supply_level_frame.pack(fill="x", pady=10)
        
        ttk.Label(supply_level_frame, text="Supply Segments:", font=("Arial", 12, "bold")).pack(side="left")
        self.supply_label = ttk.Label(supply_level_frame, text=f"{self.supply_segments}/4", 
                                    font=("Arial", 14, "bold"),
                                    foreground="red" if self.supply_segments >= 3 else "orange" if self.supply_segments > 0 else "green")
        self.supply_label.pack(side="left", padx=10)
        
        # Visual Supply Clock
        supply_visual_frame = ttk.Frame(supply_frame)
        supply_visual_frame.pack(pady=10)
        
        self.supply_canvas = tk.Canvas(supply_visual_frame, width=300, height=60)
        self.supply_canvas.pack()
        self.draw_supply_visual()
        
        # Supply Controls
        supply_control_frame = ttk.Frame(supply_frame)
        supply_control_frame.pack(pady=10)
        
        ttk.Button(supply_control_frame, text="Fill Segment", 
                  command=self.fill_supply_segment).pack(side="left", padx=5)
        ttk.Button(supply_control_frame, text="Empty Segment", 
                  command=self.empty_supply_segment).pack(side="left", padx=5)
        ttk.Button(supply_control_frame, text="Reset Supply", 
                  command=self.reset_supply).pack(side="left", padx=5)
        
        # Supply Status
        self.supply_status_label = ttk.Label(supply_frame, text=self.get_supply_status(), 
                                           font=("Arial", 10, "italic"))
        self.supply_status_label.pack(pady=5)
        
        # Condition Info
        info_frame = ttk.LabelFrame(self.parent, text="Condition Information", padding="10")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
Fatigue Effects:
• 1 Fatigue: Re-roll one success on next roll
• 2 Fatigue: Re-roll one success on each roll
• 3 Fatigue: Re-roll two successes on each roll
• 4 Fatigue: Collapse/KO - Out of scene until treated

Supply Status Effects:
• 0 filled: Full Supply - Well-equipped, no penalties
• 1-2 filled: Low Supply - Minor narrative complications
• 3 filled: Dangerously Low - Each character gains Fatigue
• 4 filled: Out of Supply - Severe penalties, starvation risk

Clearing Conditions:
• Safe rest with adequate Supply removes 1 Fatigue
• Reaching civilization resets Supply to Full
        """.strip()
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack()
        
    def draw_fatigue_visual(self):
        self.fatigue_canvas.delete("all")
        
        # Draw fatigue segments
        for i in range(4):
            x1 = 20 + i * 45
            y1 = 10
            x2 = x1 + 40
            y2 = 30
            
            # Fill color based on whether segment is filled
            if i < self.fatigue:
                color = "orange"  # Filled segments
            else:
                color = "lightgray"  # Empty segments
                
            self.fatigue_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=1)
            
        # Add labels
        self.fatigue_canvas.create_text(10, 20, text="F", anchor="w")
        
    def draw_supply_visual(self):
        self.supply_canvas.delete("all")
        
        # Draw supply segments
        for i in range(4):
            x1 = 50 + i * 50
            y1 = 20
            x2 = x1 + 40
            y2 = 50
            
            # Fill color based on whether segment is filled
            if i < self.supply_segments:
                color = "red"  # Filled segments
            else:
                color = "lightgray"  # Empty segments
                
            self.supply_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=2)
            
        # Add labels
        self.supply_canvas.create_text(25, 35, text="Supply", anchor="e")
        
    def add_fatigue(self):
        if self.fatigue < 4:
            self.fatigue += 1
            self.update_fatigue_display()
            
    def reduce_fatigue(self):
        if self.fatigue > 0:
            self.fatigue -= 1
            self.update_fatigue_display()
            
    def reset_fatigue(self):
        self.fatigue = 0
        self.update_fatigue_display()
        
    def fill_supply_segment(self):
        if self.supply_segments < 4:
            self.supply_segments += 1
            self.update_supply_display()
            
    def empty_supply_segment(self):
        if self.supply_segments > 0:
            self.supply_segments -= 1
            self.update_supply_display()
            
    def reset_supply(self):
        self.supply_segments = 0
        self.update_supply_display()
        
    def update_fatigue_display(self):
        self.fatigue_label.config(text=f"{self.fatigue}/4", 
                                foreground="red" if self.fatigue >= 3 else "orange" if self.fatigue > 0 else "green")
        self.draw_fatigue_visual()
        self.fatigue_effect_label.config(text=self.get_fatigue_effect())
        
    def update_supply_display(self):
        self.supply_label.config(text=f"{self.supply_segments}/4",
                               foreground="red" if self.supply_segments >= 3 else "orange" if self.supply_segments > 0 else "green")
        self.draw_supply_visual()
        self.supply_status_label.config(text=self.get_supply_status())
        
    def get_fatigue_effect(self):
        effects = {
            0: "No penalty",
            1: "Re-roll 1 success next roll",
            2: "Re-roll 1 success each roll",
            3: "Re-roll 2 successes each roll",
            4: "KO - Out of scene until treated"
        }
        return effects.get(self.fatigue, "Invalid fatigue level")
        
    def get_supply_status(self):
        statuses = {
            0: "Full Supply - Well-equipped, no penalties",
            1: "Low Supply - Minor narrative complications",
            2: "Low Supply - Minor narrative complications",
            3: "Dangerously Low - Each character gains Fatigue",
            4: "Out of Supply - Severe penalties, starvation risk"
        }
        return statuses.get(self.supply_segments, "Invalid supply level")
