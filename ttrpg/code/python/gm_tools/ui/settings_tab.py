import tkinter as tk
from tkinter import ttk, messagebox
from data.database import Database

class SettingsTab:
    def __init__(self, parent):
        self.parent = parent
        self.db = Database()
        self.debug_mode = False
        self.create_ui()
        
    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        status = "enabled" if self.debug_mode else "disabled"
        print(f"Debug mode {status}")
        messagebox.showinfo("Debug Mode", f"Debug mode {status}")
        
    def reload_database(self):
        try:
            self.db.init_database()
            messagebox.showinfo("Success", "Database reloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error reloading database: {e}")
            
    def clear_log(self):
        try:
            with open(self.db.log_path, 'w') as log_file:
                log_file.write("")
            messagebox.showinfo("Success", "Debug log cleared!")
        except Exception as e:
            messagebox.showerror("Error", f"Error clearing log: {e}")
            
    def test_database(self):
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM consequence_descriptors")
            cons_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM npc_descriptors")
            npc_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM adventure_descriptors")
            adv_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM clock_reference")
            clock_count = cursor.fetchone()[0]
            
            conn.close()
            
            message = f"Database Statistics:\n\n"
            message += f"Consequence Descriptors: {cons_count}\n"
            message += f"NPC Descriptors: {npc_count}\n"
            message += f"Adventure Descriptors: {adv_count}\n"
            message += f"Clock References: {clock_count}\n"
            
            messagebox.showinfo("Database Test", message)
        except Exception as e:
            messagebox.showerror("Database Test Error", f"Database test error: {e}")
            
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Settings", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Debug mode toggle
        debug_frame = ttk.Frame(self.parent)
        debug_frame.pack(pady=20)
        
        debug_check = ttk.Checkbutton(debug_frame, text="Enable Debug Logging", 
                                     variable=tk.BooleanVar(value=self.debug_mode),
                                     command=self.toggle_debug_mode, style="Large.TCheckbutton")
        debug_check.pack()
        
        # Debug info
        debug_info = ttk.Label(self.parent, 
                              text=f"Debug Log File: {self.db.log_path}\n" +
                                   "Enable debug mode to log database queries and errors",
                              font=("Arial", 14), wraplength=800)
        debug_info.pack(pady=20)
        
        # Database info
        db_info = ttk.Label(self.parent, 
                           text=f"Database File: {self.db.db_path}\n" +
                                f"SQL File: {self.db.sql_path if hasattr(self.db, 'sql_path') and self.db.sql_path else 'Not found'}\n" +
                                f"Clocks SQL File: {self.db.clocks_sql_path if hasattr(self.db, 'clocks_sql_path') and self.db.clocks_sql_path else 'Not found'}",
                           font=("Arial", 14), wraplength=800)
        db_info.pack(pady=20)
        
        # Reload database button
        reload_btn = ttk.Button(self.parent, text="Reload Database", 
                               command=self.reload_database, style="Large.TButton")
        reload_btn.pack(pady=20)
        
        # Clear log button
        clear_log_btn = ttk.Button(self.parent, text="Clear Debug Log", 
                                  command=self.clear_log, style="Large.TButton")
        clear_log_btn.pack(pady=10)
        
        # Test database button
        test_db_btn = ttk.Button(self.parent, text="Test Database Connection", 
                                command=self.test_database, style="Large.TButton")
        test_db_btn.pack(pady=10)
