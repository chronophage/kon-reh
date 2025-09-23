import tkinter as tk
from tkinter import ttk
from data.database import Database
import sqlite3

class ClocksTab:
    def __init__(self, parent):
        self.parent = parent
        self.db = Database()
        self.clocks_data = []
        self.create_ui()
        
    def import_adventure_clock(self):
        # This would import from AdventureTab - simplified for now
        pass
        
    def update_clock_checkboxes(self, clock_data):
        try:
            segment_count = int(clock_data['segment_var'].get())
        except ValueError:
            segment_count = 4
            
        # Clear existing checkboxes
        for widget, _ in clock_data['checkboxes']:
            widget.destroy()
        clock_data['checkboxes'].clear()
        clock_data['vars'].clear()
        
        # Show checkboxes frame
        clock_data['checkboxes_frame'].pack(fill="x", pady=10)
        
        # Create new checkboxes horizontally with simple number labels
        for i in range(segment_count):
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(clock_data['checkboxes_frame'], 
                                      text=str(i+1), 
                                      variable=var,
                                      style="Large.TCheckbutton")
            checkbox.pack(side=tk.LEFT, padx=5)
            clock_data['checkboxes'].append((checkbox, var))
            clock_data['vars'].append(var)
            
    def auto_set_clock_segments(self, clock_data):
        selected_name = clock_data['name_var'].get()
        if not selected_name:
            return
            
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT segments FROM clock_reference WHERE name = ?", (selected_name,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                clock_data['segment_var'].set(str(result[0]))
                self.update_clock_checkboxes(clock_data)
        except Exception as e:
            print(f"Error auto-setting clock segments: {e}")
            
    def reset_all_clocks(self):
        for clock_data in self.clocks_data:
            clock_data['name_var'].set("")
            clock_data['segment_var'].set("4")
            # Clear checkboxes
            for widget, _ in clock_data['checkboxes']:
                widget.destroy()
            clock_data['checkboxes'].clear()
            clock_data['vars'].clear()
            # Hide checkboxes frame
            clock_data['checkboxes_frame'].pack_forget()
            
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Clocks Manager", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Create scrollable frame for clocks
        self.clocks_canvas = tk.Canvas(self.parent)
        self.clocks_scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=self.clocks_canvas.yview)
        self.clocks_scrollable_frame = ttk.Frame(self.clocks_canvas)
        
        self.clocks_canvas.configure(yscrollcommand=self.clocks_scrollbar.set)
        
        # Pack scrollbar and canvas
        self.clocks_canvas.pack(side="left", fill="both", expand=True)
        self.clocks_scrollbar.pack(side="right", fill="y")
        
        # Create window in canvas
        self.clocks_canvas_window = self.clocks_canvas.create_window((0, 0), window=self.clocks_scrollable_frame, anchor="nw")
        
        # Configure scrolling
        self.clocks_scrollable_frame.bind("<Configure>", lambda e: self.clocks_canvas.configure(scrollregion=self.clocks_canvas.bbox("all")))
        self.clocks_canvas.bind("<Configure>", lambda e: self.clocks_canvas.itemconfig(self.clocks_canvas_window, width=e.width))
        
        # Import button
        import_btn = ttk.Button(self.clocks_scrollable_frame, text="Import from Adventure Generator", 
                               command=self.import_adventure_clock, style="Large.TButton")
        import_btn.pack(pady=10)
        
        # Instructions
        instructions = ttk.Label(self.clocks_scrollable_frame, 
                                text="Create up to 4 customizable clocks for your scenes.\n" +
                                     "Select the number of segments and add descriptive labels.",
                                font=("Arial", 14), wraplength=800)
        instructions.pack(pady=10)
        
        # Create 4 clock sections
        for i in range(4):
            clock_frame = ttk.LabelFrame(self.clocks_scrollable_frame, text=f"Clock {i+1}", padding=10)
            clock_frame.pack(pady=15, padx=20, fill="x")
            
            # Clock name entry
            name_frame = ttk.Frame(clock_frame)
            name_frame.pack(fill="x", pady=5)
            ttk.Label(name_frame, text="Name:", font=("Arial", 12)).pack(side=tk.LEFT)
            # Create combobox for clock names with autocomplete
            name_var = tk.StringVar()
            name_entry = ttk.Combobox(name_frame, textvariable=name_var, font=("Arial", 12), width=30)
            name_entry.pack(side=tk.LEFT, padx=10)
            
            # Populate with clock reference data
            try:
                conn = sqlite3.connect(self.db.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM clock_reference ORDER BY name")
                clock_names = [row[0] for row in cursor.fetchall()]
                conn.close()
                name_entry['values'] = clock_names
            except Exception as e:
                print(f"Error loading clock names: {e}")
                name_entry['values'] = []
            
            # Segment count dropdown
            segment_frame = ttk.Frame(clock_frame)
            segment_frame.pack(fill="x", pady=5)
            ttk.Label(segment_frame, text="Segments:", font=("Arial", 12)).pack(side=tk.LEFT)
            segment_var = tk.StringVar(value="4")
            segment_combo = ttk.Combobox(segment_frame, textvariable=segment_var, 
                                        values=["4", "6", "8", "10", "12"], state="readonly", 
                                        font=("Arial", 12), width=10)
            segment_combo.pack(side=tk.LEFT, padx=10)
            
            # Checkboxes frame (initially hidden)
            checkboxes_frame = ttk.Frame(clock_frame)
            checkboxes_frame.pack(fill="x", pady=10)
            checkboxes_frame.pack_forget()  # Hide initially
            
            # Store clock data
            clock_data = {
                'frame': clock_frame,
                'name_var': name_var,
                'name_entry': name_entry,
                'segment_var': segment_var,
                'segment_combo': segment_combo,
                'checkboxes_frame': checkboxes_frame,
                'checkboxes': [],  # Will store (widget, var) tuples
                'vars': []
            }
            
            self.clocks_data.append(clock_data)
            
            # Bind name selection to auto-set segments
            name_var.trace('w', lambda *args, cd=clock_data: self.auto_set_clock_segments(cd))
            
            # Bind segment selection to update checkboxes
            segment_var.trace('w', lambda *args, cd=clock_data: self.update_clock_checkboxes(cd))
            
        # Reset clocks button
        reset_btn = ttk.Button(self.clocks_scrollable_frame, text="Reset All Clocks", 
                              command=self.reset_all_clocks, style="Large.TButton")
        reset_btn.pack(pady=20)
