# player_tools/ui/asset_tracker_tab.py
import tkinter as tk
from tkinter import ttk

class AssetTrackerTab:
    def __init__(self, parent):
        self.parent = parent
        self.assets = []  # List of asset dictionaries
        self.followers = []  # List of follower dictionaries
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Assets & Followers", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Notebook for Assets vs Followers
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Assets Tab
        self.assets_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.assets_frame, text="Assets")
        self.create_assets_ui()
        
        # Followers Tab
        self.followers_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.followers_frame, text="Followers")
        self.create_followers_ui()
        
        # Resource Info
        info_frame = ttk.LabelFrame(self.parent, text="Resource Information", padding="10")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
Asset Tiers:
• Minor (4 XP): Safehouse, small shop charter, petty title
• Standard (8 XP): Noble title, guild section, spy ring
• Major (12 XP): City license, regional network, fortress lease

Follower Cap Ratings:
• Cap 1 (3 XP): Competent assistant
• Cap 2 (5 XP): Trained specialist
• Cap 3 (8 XP): Veteran operative
• Cap 4 (12 XP): Elite aide
• Cap 5 (17 XP): Exceptional lieutenant

Condition Track:
• Maintained: Full capability
• Neglected: -1 die when used
• Compromised: Unavailable
        """.strip()
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack()
        
    def create_assets_ui(self):
        # Add Asset Section
        add_frame = ttk.LabelFrame(self.assets_frame, text="Add Asset", padding="10")
        add_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5)
        self.asset_name_entry = ttk.Entry(add_frame, width=20)
        self.asset_name_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(add_frame, text="Tier:").grid(row=0, column=2, sticky="w", padx=5)
        self.asset_tier_var = tk.StringVar(value="Standard")
        tier_combo = ttk.Combobox(add_frame, textvariable=self.asset_tier_var,
                                values=["Minor", "Standard", "Major"],
                                width=10, state="readonly")
        tier_combo.grid(row=0, column=3, padx=5)
        
        ttk.Button(add_frame, text="Add Asset", command=self.add_asset).grid(row=0, column=4, padx=10)
        
        # Assets Display
        self.assets_display_frame = ttk.Frame(self.assets_frame)
        self.assets_display_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_assets_display()
        
    def create_followers_ui(self):
        # Add Follower Section
        add_frame = ttk.LabelFrame(self.followers_frame, text="Add Follower", padding="10")
        add_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5)
        self.follower_name_entry = ttk.Entry(add_frame, width=15)
        self.follower_name_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(add_frame, text="Cap:").grid(row=0, column=2, sticky="w", padx=5)
        self.follower_cap_var = tk.StringVar(value="2")
        cap_combo = ttk.Combobox(add_frame, textvariable=self.follower_cap_var,
                               values=["1", "2", "3", "4", "5"],
                               width=5, state="readonly")
        cap_combo.grid(row=0, column=3, padx=5)
        
        ttk.Label(add_frame, text="Specialty:").grid(row=0, column=4, sticky="w", padx=5)
        self.specialty_entry = ttk.Entry(add_frame, width=15)
        self.specialty_entry.grid(row=0, column=5, padx=5)
        
        ttk.Button(add_frame, text="Add Follower", command=self.add_follower).grid(row=0, column=6, padx=10)
        
        # Followers Display
        self.followers_display_frame = ttk.Frame(self.followers_frame)
        self.followers_display_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_followers_display()
        
    def add_asset(self):
        name = self.asset_name_entry.get().strip()
        if name:
            asset = {
                "name": name,
                "tier": self.asset_tier_var.get(),
                "condition": "Maintained",
                "xp_cost": {"Minor": 4, "Standard": 8, "Major": 12}[self.asset_tier_var.get()]
            }
            self.assets.append(asset)
            self.asset_name_entry.delete(0, tk.END)
            self.refresh_assets_display()
            
    def add_follower(self):
        name = self.follower_name_entry.get().strip()
        if name:
            cap = int(self.follower_cap_var.get())
            follower = {
                "name": name,
                "cap": cap,
                "specialty": self.specialty_entry.get().strip() or "General",
                "condition": "Maintained",
                "xp_cost": cap * cap  # Cap²
            }
            self.followers.append(follower)
            self.follower_name_entry.delete(0, tk.END)
            self.specialty_entry.delete(0, tk.END)
            self.refresh_followers_display()
            
    def remove_asset(self, index):
        if 0 <= index < len(self.assets):
            del self.assets[index]
            self.refresh_assets_display()
            
    def remove_follower(self, index):
        if 0 <= index < len(self.followers):
            del self.followers[index]
            self.refresh_followers_display()
            
    def change_asset_condition(self, index, new_condition):
        if 0 <= index < len(self.assets):
            self.assets[index]["condition"] = new_condition
            self.refresh_assets_display()
            
    def change_follower_condition(self, index, new_condition):
        if 0 <= index < len(self.followers):
            self.followers[index]["condition"] = new_condition
            self.refresh_followers_display()
            
    def refresh_assets_display(self):
        # Clear existing widgets
        for widget in self.assets_display_frame.winfo_children():
            widget.destroy()
            
        if not self.assets:
            ttk.Label(self.assets_display_frame, text="No assets added").pack(pady=20)
            return
            
        # Create scrollable area
        canvas = tk.Canvas(self.assets_display_frame)
        scrollbar = ttk.Scrollbar(self.assets_display_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display assets
        for i, asset in enumerate(self.assets):
            asset_frame = ttk.LabelFrame(scrollable_frame, text=asset["name"], padding="10")
            asset_frame.pack(fill="x", pady=5, padx=5)
            
            # Asset details
            details_frame = ttk.Frame(asset_frame)
            details_frame.pack(fill="x", pady=2)
            
            ttk.Label(details_frame, text=f"Tier: {asset['tier']}").pack(side="left", padx=10)
            ttk.Label(details_frame, text=f"XP Cost: {asset['xp_cost']}").pack(side="left", padx=10)
            
            # Condition
            condition_frame = ttk.Frame(details_frame)
            condition_frame.pack(side="left", padx=10)
            ttk.Label(condition_frame, text="Condition:").pack(side="left")
            
            condition_var = tk.StringVar(value=asset["condition"])
            condition_combo = ttk.Combobox(condition_frame, textvariable=condition_var,
                                         values=["Maintained", "Neglected", "Compromised"],
                                         width=12, state="readonly")
            condition_combo.pack(side="left", padx=5)
            condition_combo.bind("<<ComboboxSelected>>", 
                               lambda e, idx=i, var=condition_var: self.change_asset_condition(idx, var.get()))
            
            # Remove button
            ttk.Button(details_frame, text="Remove", 
                      command=lambda idx=i: self.remove_asset(idx)).pack(side="right")
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def refresh_followers_display(self):
        # Clear existing widgets
        for widget in self.followers_display_frame.winfo_children():
            widget.destroy()
            
        if not self.followers:
            ttk.Label(self.followers_display_frame, text="No followers added").pack(pady=20)
            return
            
        # Create scrollable area
        canvas = tk.Canvas(self.followers_display_frame)
        scrollbar = ttk.Scrollbar(self.followers_display_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display followers
        for i, follower in enumerate(self.followers):
            follower_frame = ttk.LabelFrame(scrollable_frame, text=follower["name"], padding="10")
            follower_frame.pack(fill="x", pady=5, padx=5)
            
            # Follower details
            details_frame = ttk.Frame(follower_frame)
            details_frame.pack(fill="x", pady=2)
            
            ttk.Label(details_frame, text=f"Cap: {follower['cap']}").pack(side="left", padx=10)
            ttk.Label(details_frame, text=f"Specialty: {follower['specialty']}").pack(side="left", padx=10)
            ttk.Label(details_frame, text=f"XP Cost: {follower['xp_cost']}").pack(side="left", padx=10)
            
            # Condition
            condition_frame = ttk.Frame(details_frame)
            condition_frame.pack(side="left", padx=10)
            ttk.Label(condition_frame, text="Condition:").pack(side="left")
            
            condition_var = tk.StringVar(value=follower["condition"])
            condition_combo = ttk.Combobox(condition_frame, textvariable=condition_var,
                                         values=["Maintained", "Neglected", "Compromised"],
                                         width=12, state="readonly")
            condition_combo.pack(side="left", padx=5)
            condition_combo.bind("<<ComboboxSelected>>", 
                               lambda e, idx=i, var=condition_var: self.change_follower_condition(idx, var.get()))
            
            # Remove button
            ttk.Button(details_frame, text="Remove", 
                      command=lambda idx=i: self.remove_follower(idx)).pack(side="right")
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

