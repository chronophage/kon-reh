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
        
        # Create category tabs
        self.create_category_tabs()
        
    def create_category_tabs(self):
        # Resources Category
        resources_frame = ttk.Frame(self.notebook)
        self.notebook.add(resources_frame, text="Resources")
        self.create_resources_tabs(resources_frame)
        
        # Combat Category
        combat_frame = ttk.Frame(self.notebook)
        self.notebook.add(combat_frame, text="Combat")
        self.create_combat_tabs(combat_frame)
        
        # Campaign Category
        campaign_frame = ttk.Frame(self.notebook)
        self.notebook.add(campaign_frame, text="Campaign")
        self.create_campaign_tabs(campaign_frame)
        
        # Tools Category
        tools_frame = ttk.Frame(self.notebook)
        self.notebook.add(tools_frame, text="Tools")
        self.create_tools_tabs(tools_frame)
        
    def create_resources_tabs(self, parent):
        resources_notebook = ttk.Notebook(parent)
        resources_notebook.pack(fill="both", expand=True)
        
        # Supply Clock
        supply_frame = ttk.Frame(resources_notebook)
        resources_notebook.add(supply_frame, text="Supply")
        self.supply_clock = SupplyClockTab(supply_frame)
        
        # Fatigue
        fatigue_frame = ttk.Frame(resources_notebook)
        resources_notebook.add(fatigue_frame, text="Fatigue")
        self.fatigue_tracker = FatigueTrackerTab(fatigue_frame)
        
        # Boons
        boon_frame = ttk.Frame(resources_notebook)
        resources_notebook.add(boon_frame, text="Boons")
        self.boon_tracker = BoonTrackerTab(boon_frame)
        
        # XP Tracker
        xp_frame = ttk.Frame(resources_notebook)
        resources_notebook.add(xp_frame, text="XP")
        self.xp_tracker = XPTrackerTab(xp_frame)
        
        # Followers & Assets
        follower_frame = ttk.Frame(resources_notebook)
        resources_notebook.add(follower_frame, text="Followers/Assets")
        self.follower_tracker = FollowerTrackerTab(follower_frame)
        
    def create_combat_tabs(self, parent):
        combat_notebook = ttk.Notebook(parent)
        combat_notebook.pack(fill="both", expand=True)
        
        # Combat Tracker
        combat_frame = ttk.Frame(combat_notebook)
        combat_notebook.add(combat_frame, text="Combat")
        self.combat_tracker = CombatTrackerTab(combat_frame)
        
        # CP Tracker
        cp_frame = ttk.Frame(combat_notebook)
        combat_notebook.add(cp_frame, text="CP")
        self.cp_tracker = CPSpendTab(cp_frame)
        
        # Consequences
        consequence_frame = ttk.Frame(combat_notebook)
        combat_notebook.add(consequence_frame, text="Consequences")
        self.consequence_tracker = ConsequenceTab(consequence_frame)
        
        # Scene Builder
        scene_frame = ttk.Frame(combat_notebook)
        combat_notebook.add(scene_frame, text="Scenes")
        self.scene_builder = SceneBuilderTab(scene_frame)
        
    def create_campaign_tabs(self, parent):
        campaign_notebook = ttk.Notebook(parent)
        campaign_notebook.pack(fill="both", expand=True)
        
        # Campaign Clocks
        campaign_frame = ttk.Frame(campaign_notebook)
        campaign_notebook.add(campaign_frame, text="Clocks")
        self.campaign_clock = CampaignClockTab(campaign_frame)
        
        # Evidence
        evidence_frame = ttk.Frame(campaign_notebook)
        campaign_notebook.add(evidence_frame, text="Evidence")
        self.evidence_tracker = EvidenceTrackerTab(evidence_frame)
        
    def create_tools_tabs(self, parent):
        tools_notebook = ttk.Notebook(parent)
        tools_notebook.pack(fill="both", expand=True)
        
        # Dice Roller
        dice_frame = ttk.Frame(tools_notebook)
        tools_notebook.add(dice_frame, text="Dice")
        self.dice_roller = DiceRollerTab(dice_frame)
        
        # NPC Generator
        npc_frame = ttk.Frame(tools_notebook)
        tools_notebook.add(npc_frame, text="NPCs")
        self.npc_generator = NPCTab(npc_frame)
        
        # Custom Clocks
        clocks_frame = ttk.Frame(tools_notebook)
        tools_notebook.add(clocks_frame, text="Clocks")
        self.clocks_tracker = ClocksTab(clocks_frame)
        
        # Adventure Tools
        adventure_frame = ttk.Frame(tools_notebook)
        tools_notebook.add(adventure_frame, text="Adventure")
        self.adventure_tools = AdventureTab(adventure_frame)
        
        # Settings
        settings_frame = ttk.Frame(tools_notebook)
        tools_notebook.add(settings_frame, text="Settings")
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

