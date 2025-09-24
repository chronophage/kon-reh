# player_tools/ui/asset_manager_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class AssetManagerTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.assets = []  # List of asset dictionaries
        self.load_assets()
        self.create_ui()
        
    def create_ui(self):
        # Asset Overview
        overview_frame = ttk.LabelFrame(self.frame, text="Asset Overview", padding="10")
        overview_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Summary stats
        stats_frame = ttk.Frame(overview_frame)
        stats_frame.pack(fill=tk.X)
        
        ttk.Label(stats_frame, text="Total Assets:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.total_label = ttk.Label(stats_frame, text="0")
        self.total_label.pack(side=tk.LEFT, padx=(5, 20))
        
        ttk.Label(stats_frame, text="Maintained:", foreground="green").pack(side=tk.LEFT)
        self.maintained_label = ttk.Label(stats_frame, text="0")
        self.maintained_label.pack(side=tk.LEFT, padx=(5, 20))
        
        ttk.Label(stats_frame, text="Neglected:", foreground="orange").pack(side=tk.LEFT)
        self.neglected_label = ttk.Label(stats_frame, text="0")
        self.neglected_label.pack(side=tk.LEFT, padx=(5, 20))
        
        ttk.Label(stats_frame, text="Compromised:", foreground="red").pack(side=tk.LEFT)
        self.compromised_label = ttk.Label(stats_frame, text="0")
        self.compromised_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Asset List
        list_frame = ttk.LabelFrame(self.frame, text="Your Assets", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for assets
        columns = ("Name", "Type", "Tier/Cap", "Condition", "Upkeep Due")
        self.asset_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.asset_tree.heading(col, text=col)
            self.asset_tree.column(col, width=120)
            
        self.asset_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.asset_tree.bind("<<TreeviewSelect>>", self.on_asset_selected)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.asset_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.asset_tree.configure(yscrollcommand=scrollbar.set)
        
        # Action buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Add Asset", command=self.add_asset_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Edit Selected", command=self.edit_asset_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_asset).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Refresh", command=self.refresh_assets).pack(side=tk.LEFT, padx=(0, 5))
        
        # Asset Details
        details_frame = ttk.LabelFrame(self.frame, text="Asset Details", padding="10")
        details_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        self.details_text = tk.Text(details_frame, height=8, wrap=tk.WORD)
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scrollbar.set)
        
        self.details_text.grid(row=0, column=0, sticky="nsew")
        details_scrollbar.grid(row=0, column=1, sticky="ns")
        
        details_frame.grid_rowconfigure(0, weight=1)
        details_frame.grid_columnconfigure(0, weight=1)
        
        # Asset Actions
        actions_frame = ttk.LabelFrame(self.frame, text="Asset Actions", padding="10")
        actions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(actions_frame, text="Activate Asset (1 Boon)", 
                  command=self.activate_with_boon).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="Activate Asset (2 XP)", 
                  command=self.activate_with_xp).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="Maintain Selected", 
                  command=self.maintain_asset).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="Pay Upkeep", 
                  command=self.pay_upkeep).pack(side=tk.LEFT)
        
        self.refresh_assets()
        
    def load_assets(self):
        """Load assets from file"""
        try:
            asset_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'assets.json')
            if os.path.exists(asset_file):
                with open(asset_file, 'r') as f:
                    self.assets = json.load(f)
            else:
                self.assets = []
        except Exception as e:
            print(f"Error loading assets: {e}")
            self.assets = []
            
    def save_assets(self):
        """Save assets to file"""
        try:
            asset_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'assets.json')
            os.makedirs(os.path.dirname(asset_file), exist_ok=True)
            with open(asset_file, 'w') as f:
                json.dump(self.assets, f, indent=2)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save assets: {e}")
            
    def refresh_assets(self):
        """Refresh the asset list display"""
        # Clear existing items
        for item in self.asset_tree.get_children():
            self.asset_tree.delete(item)
            
        # Update summary stats
        total = len(self.assets)
        maintained = len([a for a in self.assets if a.get('condition', 'Maintained') == 'Maintained'])
        neglected = len([a for a in self.assets if a.get('condition', 'Maintained') == 'Neglected'])
        compromised = len([a for a in self.assets if a.get('condition', 'Maintained') == 'Compromised'])
        
        self.total_label.config(text=str(total))
        self.maintained_label.config(text=str(maintained))
        self.neglected_label.config(text=str(neglected))
        self.compromised_label.config(text=str(compromised))
        
        # Add assets to treeview
        for asset in self.assets:
            condition = asset.get('condition', 'Maintained')
            condition_color = {
                'Maintained': 'green',
                'Neglected': 'orange',
                'Compromised': 'red'
            }.get(condition, 'black')
            
            self.asset_tree.insert("", tk.END, values=(
                asset['name'],
                asset['type'],
                asset.get('tier', asset.get('cap', 'N/A')),
                asset.get('condition', 'Maintained'),
                asset.get('upkeep_due', 'N/A')
            ), tags=(condition,))
            
        self.asset_tree.tag_configure('Maintained', foreground='green')
        self.asset_tree.tag_configure('Neglected', foreground='orange')
        self.asset_tree.tag_configure('Compromised', foreground='red')
        
    def on_asset_selected(self, event=None):
        """Handle asset selection"""
        selection = self.asset_tree.selection()
        if not selection:
            self.details_text.delete(1.0, tk.END)
            return
            
        item = self.asset_tree.item(selection[0])
        asset_name = item['values'][0]
        
        # Find asset
        asset = next((a for a in self.assets if a['name'] == asset_name), None)
        if asset:
            details = f"Name: {asset['name']}\n"
            details += f"Type: {asset['type']}\n"
            if asset['type'] == 'Off-Screen':
                details += f"Tier: {asset.get('tier', 'N/A')}\n"
                details += f"Cost: {asset.get('tier', 0) * 4} XP\n"
            else:  # On-Screen Follower
                details += f"Cap: {asset.get('cap', 'N/A')}\n"
                details += f"Cost: {asset.get('cap', 0) ** 2} XP\n"
                
            details += f"Condition: {asset.get('condition', 'Maintained')}\n"
            details += f"Upkeep Due: {asset.get('upkeep_due', 'N/A')}\n"
            details += f"Description: {asset.get('description', 'No description')}\n\n"
            
            # Upkeep cost
            if asset['type'] == 'Off-Screen':
                upkeep_cost = asset.get('tier', 0) * 2
            else:
                upkeep_cost = asset.get('cap', 0)
                
            details += f"Upkeep Cost: {upkeep_cost} XP or Downtime\n"
            
            # Activation info
            if asset['type'] == 'Off-Screen':
                details += "\nActivation: 1 Boon or 2 XP\n"
                details += "Can be used between sessions to solve problems or provide advantages."
            
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(1.0, details)
            
    def add_asset_dialog(self):
        """Open dialog to add new asset"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("Add New Asset")
        dialog.geometry("400x350")
        dialog.transient(self.frame)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text="Asset Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Asset Type:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        type_var = tk.StringVar(value="Off-Screen")
        type_combo = ttk.Combobox(dialog, textvariable=type_var, 
                                 values=["Off-Screen", "On-Screen Follower"], width=27)
        type_combo.grid(row=1, column=1, padx=10, pady=5)
        type_combo.bind("<<ComboboxSelected>>", 
                       lambda e: self.update_asset_form(dialog, type_var.get()))
        
        # Tier/Cap field (changes based on type)
        self.tier_label = ttk.Label(dialog, text="Tier (1-3):")
        self.tier_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.tier_var = tk.StringVar(value="1")
        self.tier_combo = ttk.Combobox(dialog, textvariable=self.tier_var, 
                                      values=["1", "2", "3"], width=27)
        self.tier_combo.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Description:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        desc_text = tk.Text(dialog, height=4, width=30)
        desc_text.grid(row=3, column=1, padx=10, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Add Asset", 
                  command=lambda: self.add_asset(name_var.get(), type_var.get(), 
                                               self.tier_var.get(), desc_text.get(1.0, tk.END).strip(), dialog)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)
        
    def update_asset_form(self, dialog, asset_type):
        """Update form based on asset type"""
        if asset_type == "Off-Screen":
            self.tier_label.config(text="Tier (1-3):")
            self.tier_combo.config(values=["1", "2", "3"])
            self.tier_var.set("1")
        else:  # On-Screen Follower
            self.tier_label.config(text="Cap (1-5):")
            self.tier_combo.config(values=["1", "2", "3", "4", "5"])
            self.tier_var.set("1")
            
    def add_asset(self, name, asset_type, tier_cap, description, dialog):
        """Add new asset to list"""
        if not name:
            messagebox.showerror("Error", "Asset name is required")
            return
            
        # Validate tier/cap
        try:
            value = int(tier_cap)
            if asset_type == "Off-Screen" and not (1 <= value <= 3):
                raise ValueError("Tier must be 1-3")
            elif asset_type == "On-Screen Follower" and not (1 <= value <= 5):
                raise ValueError("Cap must be 1-5")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
            
        # Create asset
        asset = {
            "name": name,
            "type": asset_type,
            "condition": "Maintained",
            "description": description,
            "upkeep_due": "Next Arc"
        }
        
        if asset_type == "Off-Screen":
            asset["tier"] = value
        else:
            asset["cap"] = value
            
        self.assets.append(asset)
        self.save_assets()
        self.refresh_assets()
        dialog.destroy()
        
    def edit_asset_dialog(self):
        """Edit selected asset"""
        selection = self.asset_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an asset to edit")
            return
            
        item = self.asset_tree.item(selection[0])
        asset_name = item['values'][0]
        asset = next((a for a in self.assets if a['name'] == asset_name), None)
        
        if not asset:
            return
            
        dialog = tk.Toplevel(self.frame)
        dialog.title("Edit Asset")
        dialog.geometry("400x400")
        dialog.transient(self.frame)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text="Asset Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        name_var = tk.StringVar(value=asset['name'])
        ttk.Entry(dialog, textvariable=name_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Asset Type:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        type_var = tk.StringVar(value=asset['type'])
        type_combo = ttk.Combobox(dialog, textvariable=type_var, 
                                 values=["Off-Screen", "On-Screen Follower"], width=27, state="disabled")
        type_combo.grid(row=1, column=1, padx=10, pady=5)
        
        # Tier/Cap field
        is_offscreen = asset['type'] == "Off-Screen"
        label_text = "Tier (1-3):" if is_offscreen else "Cap (1-5):"
        values = ["1", "2", "3"] if is_offscreen else ["1", "2", "3", "4", "5"]
        current_value = str(asset.get('tier' if is_offscreen else 'cap', '1'))
        
        ttk.Label(dialog, text=label_text).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        tier_var = tk.StringVar(value=current_value)
        tier_combo = ttk.Combobox(dialog, textvariable=tier_var, values=values, width=27)
        tier_combo.grid(row=2, column=1, padx=10, pady=5)
        
        # Condition
        ttk.Label(dialog, text="Condition:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        condition_var = tk.StringVar(value=asset.get('condition', 'Maintained'))
        condition_combo = ttk.Combobox(dialog, textvariable=condition_var, 
                                      values=["Maintained", "Neglected", "Compromised"], width=27)
        condition_combo.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Upkeep Due:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        upkeep_var = tk.StringVar(value=asset.get('upkeep_due', 'Next Arc'))
        upkeep_combo = ttk.Combobox(dialog, textvariable=upkeep_var, 
                                   values=["Next Arc", "Next Session", "Overdue"], width=27)
        upkeep_combo.grid(row=4, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Description:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        desc_text = tk.Text(dialog, height=4, width=30)
        desc_text.grid(row=5, column=1, padx=10, pady=5)
        desc_text.insert(1.0, asset.get('description', ''))
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Update Asset", 
                  command=lambda: self.update_asset(asset_name, name_var.get(), type_var.get(), 
                                                  tier_var.get(), condition_var.get(), 
                                                  upkeep_var.get(), desc_text.get(1.0, tk.END).strip(), dialog)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)
        
    def update_asset(self, old_name, name, asset_type, tier_cap, condition, upkeep_due, description, dialog):
        """Update existing asset"""
        # Find and update asset
        for asset in self.assets:
            if asset['name'] == old_name:
                asset['name'] = name
                asset['condition'] = condition
                asset['upkeep_due'] = upkeep_due
                asset['description'] = description
                
                # Update tier/cap
                if asset_type == "Off-Screen":
                    asset['tier'] = int(tier_cap)
                else:
                    asset['cap'] = int(tier_cap)
                break
                
        self.save_assets()
        self.refresh_assets()
        dialog.destroy()
        
    def delete_asset(self):
        """Delete selected asset"""
        selection = self.asset_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an asset to delete")
            return
            
        item = self.asset_tree.item(selection[0])
        asset_name = item['values'][0]
        
        if messagebox.askyesno("Confirm Delete", f"Delete asset '{asset_name}'?"):
            self.assets = [a for a in self.assets if a['name'] != asset_name]
            self.save_assets()
            self.refresh_assets()
            
    def activate_with_boon(self):
        """Activate selected asset with boon"""
        selection = self.asset_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an asset to activate")
            return
            
        item = self.asset_tree.item(selection[0])
        asset_name = item['values'][0]
        asset_type = item['values'][1]
        
        if asset_type != "Off-Screen":
            messagebox.showwarning("Wrong Type", "Only Off-Screen assets can be activated")
            return
            
        asset = next((a for a in self.assets if a['name'] == asset_name), None)
        if asset and asset.get('condition') == 'Compromised':
            messagebox.showwarning("Compromised Asset", "Compromised assets cannot be activated")
            return
            
        # In a real implementation, this would interact with the boon system
        messagebox.showinfo("Activation", f"Activated '{asset_name}' with 1 Boon!\n\nRemember to spend a Boon token or track this activation.")
        
    def activate_with_xp(self):
        """Activate selected asset with XP"""
        selection = self.asset_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an asset to activate")
            return
            
        item = self.asset_tree.item(selection[0])
        asset_name = item['values'][0]
        asset_type = item['values'][1]
        
        if asset_type != "Off-Screen":
            messagebox.showwarning("Wrong Type", "Only Off-Screen assets can be activated")
            return
            
        asset = next((a for a in self.assets if a['name'] == asset_name), None)
        if asset and asset.get('condition') == 'Compromised':
            messagebox.showwarning("Compromised Asset", "Compromised assets cannot be activated")
            return
            
        # In a real implementation, this would interact with the XP system
        messagebox.showinfo("Activation", f"Activated '{asset_name}' with 2 XP!\n\nRemember to track this XP expenditure.")
        
    def maintain_asset(self):
        """Maintain selected asset"""
        selection = self.asset_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an asset to maintain")
            return
            
        item = self.asset_tree.item(selection[0])
        asset_name = item['values'][0]
        
        # Find and update asset
        for asset in self.assets:
            if asset['name'] == asset_name:
                old_condition = asset.get('condition', 'Maintained')
                asset['condition'] = 'Maintained'
                self.save_assets()
                self.refresh_assets()
                messagebox.showinfo("Maintenance", f"Asset '{asset_name}' maintained!\n\nCondition changed from {old_condition} to Maintained.")
                break
                
    def pay_upkeep(self):
        """Pay upkeep for selected asset"""
        selection = self.asset_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an asset to pay upkeep for")
            return
            
        item = self.asset_tree.item(selection[0])
        asset_name = item['values'][0]
        asset_type = item['values'][1]
        
        asset = next((a for a in self.assets if a['name'] == asset_name), None)
        if not asset:
            return
            
        # Calculate upkeep cost
        if asset_type == "Off-Screen":
            cost = asset.get('tier', 1) * 2
            cost_type = "XP"
        else:
            cost = asset.get('cap', 1)
            cost_type = "XP"
            
        # In a real implementation, this would interact with the XP system
        asset['condition'] = 'Maintained'
        asset['upkeep_due'] = 'Next Arc'
        self.save_assets()
        self.refresh_assets()
        
        messagebox.showinfo("Upkeep Paid", f"Paid {cost} {cost_type} upkeep for '{asset_name}'\n\nAsset is now Maintained and upkeep due Next Arc.")
        
    def get_frame(self):
        return self.frame
