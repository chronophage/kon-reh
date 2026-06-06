# supply_timer_tab.py
import tkinter as tk
from tkinter import ttk

class SupplyClockTab:
    def __init__(self, parent):
        self.parent = parent
        self.segments = 0  # 0-4 segments
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Supply Clock", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Clock Visualization
        timer_frame = ttk.LabelFrame(self.parent, text="Supply Status", padding="20")
        timer_frame.pack(fill="x", padx=20, pady=10)
        
        self.timer_canvas = tk.Canvas(timer_frame, width=300, height=100)
        self.timer_canvas.pack(pady=10)
        self.draw_timer()
        
        # Status Label
        self.status_label = ttk.Label(timer_frame, text="", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=10)
        self.update_status()
        
        # Control Buttons
        control_frame = ttk.Frame(self.parent)
        control_frame.pack(pady=20)
        
        ttk.Button(control_frame, text="Fill Segment", command=self.fill_segment).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Empty Segment", command=self.empty_segment).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Reset Clock", command=self.reset_timer).pack(side="left", padx=5)
        
        # Supply Status Information
        info_frame = ttk.LabelFrame(self.parent, text="Supply Status Effects", padding="10")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
Full Supply (0 filled): The party is well-equipped. No penalties.
Low Supply (1-2 filled): Minor narrative complications: bland food, damaged arrows, thinning waterskins.
Dangerously Low (3 filled): Each character gains Fatigue.
Out of Supply (4 filled): Severe penalties; starvation, dehydration, failing gear.
        """.strip()
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack()
        
    def draw_timer(self):
        self.timer_canvas.delete("all")
        
        # Draw empty segments
        for i in range(4):
            x1 = 50 + i * 50
            y1 = 30
            x2 = x1 + 40
            y2 = 70
            
            # Fill color based on whether segment is filled
            if i < self.segments:
                color = "red"  # Filled segments
            else:
                color = "lightgray"  # Empty segments
                
            self.timer_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=2)
            
        # Add labels
        self.timer_canvas.create_text(25, 50, text="Supply", anchor="e")
        
    def update_status(self):
        status_texts = {
            0: "Full Supply - Well-equipped, no penalties",
            1: "Low Supply - Minor complications",
            2: "Low Supply - Minor complications", 
            3: "Dangerously Low - Characters gain Fatigue",
            4: "Out of Supply - Severe penalties, starvation risk"
        }
        
        self.status_label.config(text=status_texts[self.segments])
        
    def fill_segment(self):
        if self.segments < 4:
            self.segments += 1
            self.draw_timer()
            self.update_status()
            
    def empty_segment(self):
        if self.segments > 0:
            self.segments -= 1
            self.draw_timer()
            self.update_status()
            
    def reset_timer(self):
        self.segments = 0
        self.draw_timer()
        self.update_status()

# Example usage (if running this file directly)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Fate's Edge GM Tools - Supply Clock")
    root.geometry("400x400")
    
    supply_tab = SupplyClockTab(root)
    root.mainloop()
