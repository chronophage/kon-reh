import tkinter as tk
from tkinter import ttk
from data.database import Database
import sqlite3

class ClocksTab:
    def __init__(self, parent):
        self.parent = parent
        self.db = Database()
        self.timers_data = []
        self.create_ui()
        
    def import_adventure_timer(self):
        # This would import from AdventureTab - simplified for now
        pass
        
    def update_timer_checkboxes(self, timer_data):
        try:
            segment_count = int(timer_data['segment_var'].get())
        except ValueError:
            segment_count = 4
            
        # Clear existing checkboxes
        for widget, _ in timer_data['checkboxes']:
            widget.destroy()
        timer_data['checkboxes'].clear()
        timer_data['vars'].clear()
        
        # Show checkboxes frame
        timer_data['checkboxes_frame'].pack(fill="x", pady=10)
        
        # Create new checkboxes horizontally with simple number labels
        for i in range(segment_count):
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(timer_data['checkboxes_frame'], 
                                      text=str(i+1), 
                                      variable=var,
                                      style="Large.TCheckbutton")
            checkbox.pack(side=tk.LEFT, padx=5)
            timer_data['checkboxes'].append((checkbox, var))
            timer_data['vars'].append(var)
            
    def auto_set_timer_segments(self, timer_data):
        selected_name = timer_data['name_var'].get()
        if not selected_name:
            return
            
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT segments FROM timer_reference WHERE name = ?", (selected_name,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                timer_data['segment_var'].set(str(result[0]))
                self.update_timer_checkboxes(timer_data)
        except Exception as e:
            print(f"Error auto-setting timer segments: {e}")
            
    def reset_all_timers(self):
        for timer_data in self.timers_data:
            timer_data['name_var'].set("")
            timer_data['segment_var'].set("4")
            # Clear checkboxes
            for widget, _ in timer_data['checkboxes']:
                widget.destroy()
            timer_data['checkboxes'].clear()
            timer_data['vars'].clear()
            # Hide checkboxes frame
            timer_data['checkboxes_frame'].pack_forget()
            
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Clocks Manager", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Create scrollable frame for timers
        self.timers_canvas = tk.Canvas(self.parent)
        self.timers_scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=self.timers_canvas.yview)
        self.timers_scrollable_frame = ttk.Frame(self.timers_canvas)
        
        self.timers_canvas.configure(yscrollcommand=self.timers_scrollbar.set)
        
        # Pack scrollbar and canvas
        self.timers_canvas.pack(side="left", fill="both", expand=True)
        self.timers_scrollbar.pack(side="right", fill="y")
        
        # Create window in canvas
        self.timers_canvas_window = self.timers_canvas.create_window((0, 0), window=self.timers_scrollable_frame, anchor="nw")
        
        # Configure scrolling
        self.timers_scrollable_frame.bind("<Configure>", lambda e: self.timers_canvas.configure(scrollregion=self.timers_canvas.bbox("all")))
        self.timers_canvas.bind("<Configure>", lambda e: self.timers_canvas.itemconfig(self.timers_canvas_window, width=e.width))
        
        # Import button
        import_btn = ttk.Button(self.timers_scrollable_frame, text="Import from Adventure Generator", 
                               command=self.import_adventure_timer, style="Large.TButton")
        import_btn.pack(pady=10)
        
        # Instructions
        instructions = ttk.Label(self.timers_scrollable_frame, 
                                text="Create up to 4 customizable timers for your scenes.\n" +
                                     "Select the number of segments and add descriptive labels.",
                                font=("Arial", 14), wraplength=800)
        instructions.pack(pady=10)
        
        # Create 4 timer sections
        for i in range(4):
            timer_frame = ttk.LabelFrame(self.timers_scrollable_frame, text=f"Clock {i+1}", padding=10)
            timer_frame.pack(pady=15, padx=20, fill="x")
            
            # Clock name entry
            name_frame = ttk.Frame(timer_frame)
            name_frame.pack(fill="x", pady=5)
            ttk.Label(name_frame, text="Name:", font=("Arial", 12)).pack(side=tk.LEFT)
            # Create combobox for timer names with autocomplete
            name_var = tk.StringVar()
            name_entry = ttk.Combobox(name_frame, textvariable=name_var, font=("Arial", 12), width=30)
            name_entry.pack(side=tk.LEFT, padx=10)
            
            # Populate with timer reference data
            try:
                conn = sqlite3.connect(self.db.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM timer_reference ORDER BY name")
                timer_names = [row[0] for row in cursor.fetchall()]
                conn.close()
                name_entry['values'] = timer_names
            except Exception as e:
                print(f"Error loading timer names: {e}")
                name_entry['values'] = []
            
            # Segment count dropdown
            segment_frame = ttk.Frame(timer_frame)
            segment_frame.pack(fill="x", pady=5)
            ttk.Label(segment_frame, text="Segments:", font=("Arial", 12)).pack(side=tk.LEFT)
            segment_var = tk.StringVar(value="4")
            segment_combo = ttk.Combobox(segment_frame, textvariable=segment_var, 
                                        values=["4", "6", "8", "10", "12"], state="readonly", 
                                        font=("Arial", 12), width=10)
            segment_combo.pack(side=tk.LEFT, padx=10)
            
            # Checkboxes frame (initially hidden)
            checkboxes_frame = ttk.Frame(timer_frame)
            checkboxes_frame.pack(fill="x", pady=10)
            checkboxes_frame.pack_forget()  # Hide initially
            
            # Store timer data
            timer_data = {
                'frame': timer_frame,
                'name_var': name_var,
                'name_entry': name_entry,
                'segment_var': segment_var,
                'segment_combo': segment_combo,
                'checkboxes_frame': checkboxes_frame,
                'checkboxes': [],  # Will store (widget, var) tuples
                'vars': []
            }
            
            self.timers_data.append(timer_data)
            
            # Bind name selection to auto-set segments
            name_var.trace('w', lambda *args, cd=timer_data: self.auto_set_timer_segments(cd))
            
            # Bind segment selection to update checkboxes
            segment_var.trace('w', lambda *args, cd=timer_data: self.update_timer_checkboxes(cd))
            
        # Reset timers button
        reset_btn = ttk.Button(self.timers_scrollable_frame, text="Reset All Clocks", 
                              command=self.reset_all_timers, style="Large.TButton")
        reset_btn.pack(pady=20)
