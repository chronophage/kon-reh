# player_tools/ui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add parent directory to path for shared imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from player_tools.ui.character_sheet_tab import CharacterSheetTab
from player_tools.ui.xp_planner_tab import XPPlannerTab
from player_tools.ui.dice_roller_tab import FateEdgeDiceRoller
from player_tools.ui.character_manager import CharacterManager
from player_tools.ui.asset_manager_tab import AssetManagerTab
from player_tools.ui.settings_tab import SettingsManager
from player_tools.ui.skill_browser_tab import SkillBrowserTab

class PlayerMainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Fate's Edge Player Tools")
        self.root.geometry("1000x700")
        
        # Initialize character data
        self.character_data = {}
        
        # Create the main UI
        self.create_ui()
        
    def create_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_tabs()
        
        # Create status bar
        self.create_status_bar()
        
    def create_tabs(self):
        # Character Sheet Tab
        self.character_sheet_frame = ttk.Frame(self.notebook)
        self.character_sheet_frame.pack(fill=tk.BOTH, expand=True)
        self.character_sheet = CharacterSheetTab(self.character_sheet_frame)
        self.character_sheet.get_frame().pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.character_sheet_frame, text="Character Sheet")
        
        # XP Planner Tab
        self.xp_planner_frame = ttk.Frame(self.notebook)
        self.xp_planner_frame.pack(fill=tk.BOTH, expand=True)
        self.xp_planner = XPPlannerTab(self.xp_planner_frame, self.character_data)
        self.xp_planner.get_frame().pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.xp_planner_frame, text="XP Planner")
        
        # Dice Roller Tab
        self.dice_roller_frame = ttk.Frame(self.notebook)
        self.dice_roller_frame.pack(fill=tk.BOTH, expand=True)
        self.dice_roller = FateEdgeDiceRoller(self.dice_roller_frame)
        self.dice_roller.get_frame().pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.dice_roller_frame, text="Dice Roller")
        
        # Skill Browser Tab
        self.skill_browser_frame = ttk.Frame(self.notebook)
        self.skill_browser_frame.pack(fill=tk.BOTH, expand=True)
        self.skill_browser = SkillBrowserTab(self.skill_browser_frame)
        self.skill_browser.get_frame().pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.skill_browser_frame, text="Skill Browser")
        
        # Character Manager Tab
        self.character_manager_frame = ttk.Frame(self.notebook)
        self.character_manager_frame.pack(fill=tk.BOTH, expand=True)
        self.character_manager = CharacterManager(self.character_manager_frame, self.character_data)
        self.character_manager.get_frame().pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.character_manager_frame, text="Characters")
       
        # Asset Tracker Tab
        self.asset_manager_frame = ttk.Frame(self.notebook)
        self.asset_manager_frame.pack(fill=tk.BOTH, expand=True)
        self.asset_manager = AssetManagerTab(self.asset_manager_frame)
        self.asset_manager.get_frame().pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.asset_manager_frame, text="Asset Manager")

        # Settings Tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.settings_frame.pack(fill=tk.BOTH, expand=True)
        self.settings_manager = SettingsManager(self.settings_frame)
        self.settings_manager.get_frame().pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.settings_frame, text="Settings")
        
    def create_status_bar(self):
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        
        self.status_label = ttk.Label(self.status_bar, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        # Version info
        version_label = ttk.Label(self.status_bar, text="Fate's Edge Player Tools v1.0")
        version_label.pack(side=tk.RIGHT)
        
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlayerMainWindow(root)
    root.mainloop()

