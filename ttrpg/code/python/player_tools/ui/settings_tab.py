# player_tools/ui/settings_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import shutil

class SettingsManager:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        # Use shared/data/ directory
        self.shared_data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'shared', 'data')
        os.makedirs(self.shared_data_dir, exist_ok=True)
        
        # Load existing settings
        self.settings = self.load_settings()
        
        # Appearance Settings
        self.appearance_frame = ttk.LabelFrame(self.frame, text="Appearance", padding="10")
        self.appearance_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(self.appearance_frame, text="Theme:").grid(row=0, column=0, sticky=tk.W)
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "default"))
        self.theme_combo = ttk.Combobox(self.appearance_frame, textvariable=self.theme_var,
                                       values=["default", "clam", "alt", "classic"], width=15)
        self.theme_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Dice Settings
        self.dice_frame = ttk.LabelFrame(self.frame, text="Dice Settings", padding="10")
        self.dice_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(self.dice_frame, text="Default Dice Pool:").grid(row=0, column=0, sticky=tk.W)
        self.default_pool_var = tk.StringVar(value=str(self.settings.get("default_pool", 4)))
        self.default_pool_spin = ttk.Spinbox(self.dice_frame, from_=1, to=20, 
                                            textvariable=self.default_pool_var, width=5)
        self.default_pool_spin.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(self.dice_frame, text="Default Difficulty:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.default_difficulty_var = tk.StringVar(value=str(self.settings.get("default_difficulty", 1)))
        self.default_difficulty_spin = ttk.Spinbox(self.dice_frame, from_=1, to=10,
                                                  textvariable=self.default_difficulty_var, width=5)
        self.default_difficulty_spin.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        # Data Settings
        self.data_frame = ttk.LabelFrame(self.frame, text="Data Management", padding="10")
        self.data_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.backup_btn = ttk.Button(self.data_frame, text="Backup All Data", command=self.backup_all_data)
        self.backup_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.restore_btn = ttk.Button(self.data_frame, text="Restore Data", command=self.restore_data)
        self.restore_btn.grid(row=0, column=1, padx=(0, 5))
        
        # Save Button
        self.save_btn = ttk.Button(self.frame, text="Save Settings", command=self.save_settings)
        self.save_btn.grid(row=3, column=0, pady=10)
        
    def load_settings(self):
        settings_file = os.path.join(self.shared_data_dir, "settings.json")
        try:
            if os.path.exists(settings_file):
                with open(settings_file, "r") as f:
                    return json.load(f)
            else:
                # Return default settings
                return {
                    "theme": "default",
                    "default_pool": 4,
                    "default_difficulty": 1
                }
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {str(e)}")
            return {
                "theme": "default",
                "default_pool": 4,
                "default_difficulty": 1
            }
            
    def save_settings(self):
        self.settings = {
            "theme": self.theme_var.get(),
            "default_pool": int(self.default_pool_var.get()),
            "default_difficulty": int(self.default_difficulty_var.get())
        }
        
        settings_file = os.path.join(self.shared_data_dir, "settings.json")
        try:
            with open(settings_file, "w") as f:
                json.dump(self.settings, f, indent=2)
            messagebox.showinfo("Success", "Settings saved successfully!")
            
            # Apply theme
            self.apply_theme()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            
    def apply_theme(self):
        theme = self.theme_var.get()
        try:
            self.parent.tk.call("ttk::setTheme", theme)
        except Exception as e:
            messagebox.showwarning("Theme Error", f"Could not apply theme: {str(e)}")
            
    def backup_all_data(self):
        try:
            backup_file = os.path.join(self.shared_data_dir, "data_backup.zip")
            shutil.make_archive(
                os.path.join(self.shared_data_dir, "data_backup"), 
                "zip", 
                self.shared_data_dir
            )
            messagebox.showinfo("Success", f"All data backed up successfully to:\n{backup_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {str(e)}")
            
    def restore_data(self):
        messagebox.showinfo("Info", "To restore data, simply extract your backup ZIP file to the shared/data/ directory")
            
    def get_frame(self):
        return self.frame

