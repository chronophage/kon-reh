# ui/follower_tracker_tab.py
import tkinter as tk
from tkinter import ttk

class FollowerTrackerTab:
    def __init__(self, parent):
        self.parent = parent
        self.followers = []  # List of follower dictionaries
        self.assets = []     # List of asset dictionaries
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Followers & Assets Tracker", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Notebook for Followers vs Assets
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Followers Tab
        self.followers_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.followers_frame, text="Followers")
        self.create_followers_ui()
        
        # Assets Tab
        self.assets_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.assets_frame, text="Assets")
        self.create_assets_ui()
        
        # Resource Info
        info_frame = ttk.LabelFrame(self.parent, text="Resource Management Information", padding="10")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
Follower & Asset Management:
• Condition Track: Maintained → Neglected → Compromised
• Upkeep: Required after heavy use or at end of arc
• Maintenance Options: Downtime (Significant Time) or XP cost
• Complications: GM can spend (SB) to Harm or Degrade followers/assets
• Loyalty: Wary / Steady / Devoted (optional tracking)

Follower Capabilities:
• Cap 1-5: Assistance bonus up to Cap value (max +3 total)
• Specialty: Narrow lane where they can assist
• Exposure: Risk from being used in scenes

Asset Tiers:
• Minor (4 XP): Safehouse, small shop charter, petty title
• Standard (8 XP): Noble title, guild section, spy ring
• Major (12 XP): City license, regional network, fortress lease
        """.strip()
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack()
        
    def create_followers_ui(self):
        # Add Follower Section
        add_frame = ttk.LabelFrame(self.followers_frame, text="Add Follower", padding="10")
        add_frame.pack(fill="x", padx=10, pady=10)
        
        # Name and Cap
        name_frame = ttk.Frame(add_frame)
        name_frame.pack(fill="x", pady=2)
        ttk.Label(name_frame, text="Name:").pack(side="left")
        self.follower_name_entry = ttk.Entry(name_frame, width=15)
        self.follower_name_entry.pack(side="left", padx=5)
        
        ttk.Label(name_frame, text="Cap:").pack(side="left", padx=(20,0))
        self.cap_var = tk.StringVar(value="2")
        cap_combo = ttk.Combobox(name_frame, textvariable=self.cap_var, 
                                values=["1", "2", "3", "4", "5"], width=5, state="readonly")
        cap_combo.pack(side="left", padx=5)
        
        # Specialty
        spec_frame = ttk.Frame(add_frame)
        spec_frame.pack(fill="x", pady=2)
        ttk.Label(spec_frame, text="Specialty:").pack(side="left")
        self.specialty_entry = ttk.Entry(spec_frame, width=25)
        self.specialty_entry.pack(side="left", padx=5)
        
        # Loyalty (Optional)
        loyalty_frame = ttk.Frame(add_frame)
        loyalty_frame.pack(fill="x", pady=2)
        ttk.Label(loyalty_frame, text="Loyalty:").pack(side="left")
        self.loyalty_var = tk.StringVar(value="Steady")
        loyalty_combo = ttk.Combobox(loyalty_frame, textvariable=self.loyalty_var, 
                                   values=["Wary", "Steady", "Devoted"], width=10, state="readonly")
        loyalty_combo.pack(side="left", padx=5)
        
        ttk.Button(add_frame, text="Add Follower", command=self.add_follower).pack(side="left", padx=10)
        
        # Followers Display
        self.followers_display_frame = ttk.Frame(self.followers_frame)
        self.followers_display_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_followers_display()
        
    def create_assets_ui(self):
        # Add Asset Section
        add_frame = ttk.LabelFrame(self.assets_frame, text="Add Asset", padding="10")
        add_frame.pack(fill="x", padx=10, pady=10)
        
        # Name and Tier
        name_frame = ttk.Frame(add_frame)
        name_frame.pack(fill="x", pady=2)
        ttk.Label(name_frame, text="Name:").pack(side="left")
        self.asset_name_entry = ttk.Entry(name_frame, width=20)
        self.asset_name_entry.pack(side="left", padx=5)
        
        ttk.Label(name_frame, text="Tier:").pack(side="left", padx=(20,0))
        self.tier_var = tk.StringVar(value="Standard")
        tier_combo = ttk.Combobox(name_frame, textvariable=self.tier_var, 
                                values=["Minor", "Standard", "Major"], width=10, state="readonly")
        tier_combo.pack(side="left", padx=5)
        
        ttk.Button(add_frame, text="Add Asset", command=self.add_asset).pack(side="left", padx=10)
        
        # Assets Display
        self.assets_display_frame = ttk.Frame(self.assets_frame)
        self.assets_display_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_assets_display()
        
    def add_follower(self):
        name = self.follower_name_entry.get().strip()
        if name:
            follower = {
                "name": name,
                "cap": int(self.cap_var.get()),
                "specialty": self.specialty_entry.get().strip() or "General",
                "condition": "Maintained",  # Maintained, Neglected, Compromised
                "loyalty": self.loyalty_var.get(),
                "exposure": 0  # 0-2
            }
            self.followers.append(follower)
            self.follower_name_entry.delete(0, tk.END)
            self.specialty_entry.delete(0, tk.END)
            self.refresh_followers_display()
            
    def add_asset(self):
        name = self.asset_name_entry.get().strip()
        if name:
            asset = {
                "name": name,
                "tier": self.tier_var.get(),
                "condition": "Maintained",  # Maintained, Neglected, Compromised
            }
            self.assets.append(asset)
            self.asset_name_entry.delete(0, tk.END)
            self.refresh_assets_display()
            
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
        
        # Create follower cards
        for i, follower in enumerate(self.followers):
            follower_card = ttk.LabelFrame(scrollable_frame, text=follower["name"], padding="10")
            follower_card.pack(fill="x", pady=5, padx=5)
            
            # Stats row
            stats_frame = ttk.Frame(follower_card)
            stats_frame.pack(fill="x", pady=2)
            
            ttk.Label(stats_frame, text=f"Cap: {follower['cap']}").pack(side="left", padx=10)
            ttk.Label(stats_frame, text=f"Specialty: {follower['specialty']}").pack(side="left", padx=10)
            ttk.Label(stats_frame, text=f"Loyalty: {follower['loyalty']}").pack(side="left", padx=10)
            
            # Condition and Exposure
            condition_frame = ttk.Frame(follower_card)
            condition_frame.pack(fill="x", pady=2)
            
            ttk.Label(condition_frame, text="Condition:", font=("Arial", 9, "bold")).pack(side="left")
            condition_label = ttk.Label(condition_frame, text=follower["condition"], 
                                      foreground=self.get_condition_color(follower["condition"]))
            condition_label.pack(side="left", padx=5)
            
            ttk.Label(condition_frame, text=f" | Exposure: {follower['exposure']}/2").pack(side="left", padx=10)
            
            # Controls
            control_frame = ttk.Frame(follower_card)
            control_frame.pack(fill="x", pady=5)
            
            # Condition controls
            cond_frame = ttk.Frame(control_frame)
            cond_frame.pack(side="left", padx=5)
            ttk.Button(cond_frame, text="↑", width=3, command=lambda idx=i: self.improve_condition(idx, "follower")).pack(side="left")
            ttk.Button(cond_frame, text="↓", width=3, command=lambda idx=i: self.degrade_condition(idx, "follower")).pack(side="left", padx=2)
            
            # Exposure controls
            exp_frame = ttk.Frame(control_frame)
            exp_frame.pack(side="left", padx=5)
            ttk.Button(exp_frame, text="Exp+", width=4, command=lambda idx=i: self.add_exposure(idx)).pack(side="left")
            ttk.Button(exp_frame, text="Exp-", width=4, command=lambda idx=i: self.reduce_exposure(idx)).pack(side="left", padx=2)
            
            # Promote button (increase Cap)
            ttk.Button(control_frame, text="Promote", command=lambda idx=i: self.promote_follower(idx)).pack(side="left", padx=5)
            
            # Remove button
            ttk.Button(control_frame, text="Remove", command=lambda idx=i: self.remove_follower(idx)).pack(side="right", padx=5)
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
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
        
        # Create asset cards
        for i, asset in enumerate(self.assets):
            asset_card = ttk.LabelFrame(scrollable_frame, text=asset["name"], padding="10")
            asset_card.pack(fill="x", pady=5, padx=5)
            
            # Stats row
            stats_frame = ttk.Frame(asset_card)
            stats_frame.pack(fill="x", pady=2)
            
            ttk.Label(stats_frame, text=f"Tier: {asset['tier']}").pack(side="left", padx=10)
            
            # Condition
            condition_frame = ttk.Frame(asset_card)
            condition_frame.pack(fill="x", pady=2)
            
            ttk.Label(condition_frame, text="Condition:", font=("Arial", 9, "bold")).pack(side="left")
            condition_label = ttk.Label(condition_frame, text=asset["condition"], 
                                      foreground=self.get_condition_color(asset["condition"]))
            condition_label.pack(side="left", padx=5)
            
            # Controls
            control_frame = ttk.Frame(asset_card)
            control_frame.pack(fill="x", pady=5)
            
            # Condition controls
            cond_frame = ttk.Frame(control_frame)
            cond_frame.pack(side="left", padx=5)
            ttk.Button(cond_frame, text="↑", width=3, command=lambda idx=i: self.improve_condition(idx, "asset")).pack(side="left")
            ttk.Button(cond_frame, text="↓", width=3, command=lambda idx=i: self.degrade_condition(idx, "asset")).pack(side="left", padx=2)
            
            # Remove button
            ttk.Button(control_frame, text="Remove", command=lambda idx=i: self.remove_asset(idx)).pack(side="right", padx=5)
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def get_condition_color(self, condition):
        colors = {
            "Maintained": "green",
            "Neglected": "orange",
            "Compromised": "red"
        }
        return colors.get(condition, "black")
        
    def improve_condition(self, index, resource_type):
        if resource_type == "follower" and 0 <= index < len(self.followers):
            conditions = ["Maintained", "Neglected", "Compromised"]
            current = self.followers[index]["condition"]
            current_idx = conditions.index(current)
            if current_idx > 0:
                self.followers[index]["condition"] = conditions[current_idx - 1]
                self.refresh_followers_display()
        elif resource_type == "asset" and 0 <= index < len(self.assets):
            conditions = ["Maintained", "Neglected", "Compromised"]
            current = self.assets[index]["condition"]
            current_idx = conditions.index(current)
            if current_idx > 0:
                self.assets[index]["condition"] = conditions[current_idx - 1]
                self.refresh_assets_display()
                
    def degrade_condition(self, index, resource_type):
        if resource_type == "follower" and 0 <= index < len(self.followers):
            conditions = ["Maintained", "Neglected", "Compromised"]
            current = self.followers[index]["condition"]
            current_idx = conditions.index(current)
            if current_idx < len(conditions) - 1:
                self.followers[index]["condition"] = conditions[current_idx + 1]
                self.refresh_followers_display()
        elif resource_type == "asset" and 0 <= index < len(self.assets):
            conditions = ["Maintained", "Neglected", "Compromised"]
            current = self.assets[index]["condition"]
            current_idx = conditions.index(current)
            if current_idx < len(conditions) - 1:
                self.assets[index]["condition"] = conditions[current_idx + 1]
                self.refresh_assets_display()
                
    def add_exposure(self, index):
        if 0 <= index < len(self.followers) and self.followers[index]["exposure"] < 2:
            self.followers[index]["exposure"] += 1
            self.refresh_followers_display()
            
    def reduce_exposure(self, index):
        if 0 <= index < len(self.followers) and self.followers[index]["exposure"] > 0:
            self.followers[index]["exposure"] -= 1
            self.refresh_followers_display()
            
    def promote_follower(self, index):
        if 0 <= index < len(self.followers) and self.followers[index]["cap"] < 5:
            self.followers[index]["cap"] += 1
            self.refresh_followers_display()
            
    def remove_follower(self, index):
        if 0 <= index < len(self.followers):
            del self.followers[index]
            self.refresh_followers_display()
            
    def remove_asset(self, index):
        if 0 <= index < len(self.assets):
            del self.assets[index]
            self.refresh_assets_display()
