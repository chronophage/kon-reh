# player_tools/ui/settings_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class SettingsManager:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
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
        
        self.backup_btn = ttk.Button(self.data_frame, text="Backup Characters", command=self.backup_characters)
        self.backup_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.restore_btn = ttk.Button(self.data_frame, text="Restore Characters", command=self.restore_characters)
        self.restore_btn.grid(row=0, column=1, padx=(0, 5))
        
        # Save Button
        self.save_btn = ttk.Button(self.frame, text="Save Settings", command=self.save_settings)
        self.save_btn.grid(row=3, column=0, pady=10)
        
    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
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
        
        try:
            with open("settings.json", "w") as f:
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
            
    def backup_characters(self):
        try:
            import shutil
            if os.path.exists("characters"):
                shutil.make_archive("characters_backup", "zip", "characters")
                messagebox.showinfo("Success", "Characters backed up successfully!")
            else:
                messagebox.showwarning("No Data", "No character data to backup")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {str(e)}")
            
    def restore_characters(self):
        try:
            import shutil
            if os.path.exists("characters_backup.zip"):
                if os.path.exists("characters"):
                    shutil.rmtree("characters")
                shutil.unpack_archive("characters_backup.zip", "characters")
                messagebox.showinfo("Success", "Characters restored successfully!")
            else:
                messagebox.showwarning("No Backup", "No backup file found")
        except Exception as e:
            messagebox.showerror("Error", f"Restore failed: {str(e)}")
            
    def get_frame(self):
        return self.frame

