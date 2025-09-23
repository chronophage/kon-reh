# ui/main_window.py
import tkinter as tk
from tkinter import ttk

# Import all your tab modules
from ui.supply_clock_tab import SupplyClockTab
from ui.fatigue_tracker_tab import FatigueTrackerTab
from ui.boon_tracker_tab import BoonTrackerTab
from ui.xp_tracker_tab import XPTrackerTab
from ui.combat_tracker_tab import CombatTrackerTab
from ui.scene_builder_tab import SceneBuilderTab
from ui.cp_spend_tab import CPSpendTab
from ui.consequence_tab import ConsequenceTab
from ui.campaign_clock_tab import CampaignClockTab
from ui.evidence_tracker_tab import EvidenceTrackerTab
from ui.follower_tracker_tab import FollowerTrackerTab
from ui.dice_roller_tab import DiceRollerTab
from ui.npc_tab import NPCTab
from ui.clocks_tab import ClocksTab
from ui.adventure_tab import AdventureTab
from ui.settings_tab import SettingsTab

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Fate's Edge GM Tools")
        self.root.geometry("1200x800")
        
        self.create_menu()
        self.create_notebook()
        self.create_status_bar()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Campaign", command=self.new_campaign)
        file_menu.add_command(label="Open Campaign", command=self.open_campaign)
        file_menu.add_command(label="Save Campaign", command=self.save_campaign)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Export Data", command=self.export_data)
        tools_menu.add_command(label="Import Data", command=self.import_data)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Quick Reference", command=self.show_help)
        
    def create_notebook(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create all tabs
        self.create_all_tabs()
        
    def create_all_tabs(self):
        # Core Resource Trackers
        supply_frame = ttk.Frame(self.notebook)
        self.notebook.add(supply_frame, text="Supply Clock")
        self.supply_clock = SupplyClockTab(supply_frame)
        
        fatigue_frame = ttk.Frame(self.notebook)
        self.notebook.add(fatigue_frame, text="Fatigue")
        self.fatigue_tracker = FatigueTrackerTab(fatigue_frame)
        
        boon_frame = ttk.Frame(self.notebook)
        self.notebook.add(boon_frame, text="Boons")
        self.boon_tracker = BoonTrackerTab(boon_frame)
        
        xp_frame = ttk.Frame(self.notebook)
        self.notebook.add(xp_frame, text="XP Tracker")
        self.xp_tracker = XPTrackerTab(xp_frame)
        
        # Combat & Scene Management
        combat_frame = ttk.Frame(self.notebook)
        self.notebook.add(combat_frame, text="Combat Tracker")
        self.combat_tracker = CombatTrackerTab(combat_frame)
        
        scene_frame = ttk.Frame(self.notebook)
        self.notebook.add(scene_frame, text="Scene Builder")
        self.scene_builder = SceneBuilderTab(scene_frame)
        
        # Consequence Management
        cp_frame = ttk.Frame(self.notebook)
        self.notebook.add(cp_frame, text="CP Tracker")
        self.cp_tracker = CPSpendTab(cp_frame)
        
        consequence_frame = ttk.Frame(self.notebook)
        self.notebook.add(consequence_frame, text="Consequences")
        self.consequence_tracker = ConsequenceTab(consequence_frame)
        
        # Campaign Management
        campaign_frame = ttk.Frame(self.notebook)
        self.notebook.add(campaign_frame, text="Campaign Clocks")
        self.campaign_clock = CampaignClockTab(campaign_frame)
        
        evidence_frame = ttk.Frame(self.notebook)
        self.notebook.add(evidence_frame, text="Evidence")
        self.evidence_tracker = EvidenceTrackerTab(evidence_frame)
        
        # Resource Management
        follower_frame = ttk.Frame(self.notebook)
        self.notebook.add(follower_frame, text="Followers & Assets")
        self.follower_tracker = FollowerTrackerTab(follower_frame)
        
        # Utility Tools
        dice_frame = ttk.Frame(self.notebook)
        self.notebook.add(dice_frame, text="Dice Roller")
        self.dice_roller = DiceRollerTab(dice_frame)
        
        npc_frame = ttk.Frame(self.notebook)
        self.notebook.add(npc_frame, text="NPC Generator")
        self.npc_generator = NPCTab(npc_frame)
        
        clocks_frame = ttk.Frame(self.notebook)
        self.notebook.add(clocks_frame, text="Custom Clocks")
        self.clocks_tracker = ClocksTab(clocks_frame)
        
        adventure_frame = ttk.Frame(self.notebook)
        self.notebook.add(adventure_frame, text="Adventure Tools")
        self.adventure_tools = AdventureTab(adventure_frame)
        
        # Settings
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        self.settings = SettingsTab(settings_frame)
        
    def create_status_bar(self):
        self.status_bar = ttk.Label(self.root, text="Fate's Edge GM Tools Ready", 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def update_status(self, message):
        self.status_bar.config(text=message)
        
    # Menu command methods
    def new_campaign(self):
        self.update_status("New campaign started")
        
    def open_campaign(self):
        self.update_status("Campaign loaded")
        
    def save_campaign(self):
        self.update_status("Campaign saved")
        
    def export_data(self):
        self.update_status("Data exported")
        
    def import_data(self):
        self.update_status("Data imported")
        
    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("300x200")
        about_window.transient(self.root)
        about_window.grab_set()
        
        ttk.Label(about_window, text="Fate's Edge GM Tools", 
                 font=("Arial", 16, "bold")).pack(pady=20)
        ttk.Label(about_window, text="Version 1.0").pack()
        ttk.Label(about_window, text="A comprehensive toolkit for Fate's Edge RPG").pack(pady=10)
        ttk.Button(about_window, text="Close", command=about_window.destroy).pack(pady=20)
        
    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Quick Reference")
        help_window.geometry("500x400")
        help_window.transient(self.root)
        help_window.grab_set()
        
        help_text = """
Quick Reference for Fate's Edge GM Tools:

Core Tabs:
• Supply Clock: Track party resources (0-4 segments)
• Fatigue: Manage character exhaustion levels
• Boons: Track player rewards from complications
• XP Tracker: Manage character advancement currency

Combat & Scenes:
• Combat Tracker: Initiative, positioning, and combat management
• Scene Builder: Prepare scenes with stakes and rails
• CP Tracker: Manage complication points spending
• Consequences: Handle deck draws and complications

Campaign Management:
• Campaign Clocks: Track Mandate and Crisis for finale
• Evidence: Manage Immaculate vs Scorched evidence
• Followers & Assets: Resource condition tracking

Utilities:
• Dice Roller: Roll d10 pools with success counting
• NPC Generator: Create NPCs with motivations
• Custom Clocks: Track any custom timers
• Adventure Tools: Generate content and locations

Navigation:
• Click tabs to switch between tools
• Most tools have built-in help information
• Data persists between sessions
        """.strip()
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.insert("1.0", help_text)
        text_widget.config(state=tk.DISABLED)
        
        scrollbar = ttk.Scrollbar(help_window, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(help_window, text="Close", command=help_window.destroy).pack(pady=10)

# Make sure this is at the end of the file
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
