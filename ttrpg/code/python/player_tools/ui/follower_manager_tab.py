# player_tools/ui/follower_manager_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class FollowerManagerTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.followers = []  # List of follower dictionaries
        self.load_followers()
        self.create_ui()
        
    def create_ui(self):
        # Follower Overview
        overview_frame = ttk.LabelFrame(self.frame, text="Follower Overview", padding="10")
        overview_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Summary stats
        stats_frame = ttk.Frame(overview_frame)
        stats_frame.pack(fill=tk.X)
        
        ttk.Label(stats_frame, text="Total Followers:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
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
        
        # Follower List
        list_frame = ttk.LabelFrame(self.frame, text="Your Followers", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for followers
        columns = ("Name", "Specialty", "Cap", "Condition", "Upkeep Due")
        self.follower_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.follower_tree.heading(col, text=col)
            self.follower_tree.column(col, width=120)
            
        self.follower_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.follower_tree.bind("<<TreeviewSelect>>", self.on_follower_selected)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.follower_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.follower_tree.configure(yscrollcommand=scrollbar.set)
        
        # Action buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Add Follower", command=self.add_follower_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Edit Selected", command=self.edit_follower_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_follower).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Refresh", command=self.refresh_followers).pack(side=tk.LEFT, padx=(0, 5))
        
        # Follower Details
        details_frame = ttk.LabelFrame(self.frame, text="Follower Details", padding="10")
        details_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        self.details_text = tk.Text(details_frame, height=8, wrap=tk.WORD)
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scrollbar.set)
        
        self.details_text.grid(row=0, column=0, sticky="nsew")
        details_scrollbar.grid(row=0, column=1, sticky="ns")
        
        details_frame.grid_rowconfigure(0, weight=1)
        details_frame.grid_columnconfigure(0, weight=1)
        
        # Follower Actions
        actions_frame = ttk.LabelFrame(self.frame, text="Follower Actions", padding="10")
        actions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(actions_frame, text="Maintain Selected", 
                  command=self.maintain_follower).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="Pay Upkeep", 
                  command=self.pay_upkeep).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="Promote Follower", 
                  command=self.promote_follower).pack(side=tk.LEFT)
        
        self.refresh_followers()
        
    def load_followers(self):
        """Load followers from file"""
        try:
            follower_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'followers.json')
            if os.path.exists(follower_file):
                with open(follower_file, 'r') as f:
                    self.followers = json.load(f)
            else:
                self.followers = []
        except Exception as e:
            print(f"Error loading followers: {e}")
            self.followers = []
            
    def save_followers(self):
        """Save followers to file"""
        try:
            follower_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'followers.json')
            os.makedirs(os.path.dirname(follower_file), exist_ok=True)
            with open(follower_file, 'w') as f:
                json.dump(self.followers, f, indent=2)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save followers: {e}")
            
    def refresh_followers(self):
        """Refresh the follower list display"""
        # Clear existing items
        for item in self.follower_tree.get_children():
            self.follower_tree.delete(item)
            
        # Update summary stats
        total = len(self.followers)
        maintained = len([f for f in self.followers if f.get('condition', 'Maintained') == 'Maintained'])
        neglected = len([f for f in self.followers if f.get('condition', 'Maintained') == 'Neglected'])
        compromised = len([f for f in self.followers if f.get('condition', 'Maintained') == 'Compromised'])
        
        self.total_label.config(text=str(total))
        self.maintained_label.config(text=str(maintained))
        self.neglected_label.config(text=str(neglected))
        self.compromised_label.config(text=str(compromised))
        
        # Add followers to treeview
        for follower in self.followers:
            condition = follower.get('condition', 'Maintained')
            
            self.follower_tree.insert("", tk.END, values=(
                follower['name'],
                follower.get('specialty', 'General'),
                follower.get('cap', 1),
                follower.get('condition', 'Maintained'),
                follower.get('upkeep_due', 'N/A')
            ), tags=(condition,))
            
        self.follower_tree.tag_configure('Maintained', foreground='green')
        self.follower_tree.tag_configure('Neglected', foreground='orange')
        self.follower_tree.tag_configure('Compromised', foreground='red')
        
    def on_follower_selected(self, event=None):
        """Handle follower selection"""
        selection = self.follower_tree.selection()
        if not selection:
            self.details_text.delete(1.0, tk.END)
            return
            
        item = self.follower_tree.item(selection[0])
        follower_name = item['values'][0]
        
        # Find follower
        follower = next((f for f in self.followers if f['name'] == follower_name), None)
        if follower:
            details = f"Name: {follower['name']}\n"
            details += f"Specialty: {follower.get('specialty', 'General')}\n"
            details += f"Cap: {follower.get('cap', 1)}\n"
            details += f"Cost: {follower.get('cap', 1) ** 2} XP\n"
            details += f"Condition: {follower.get('condition', 'Maintained')}\n"
            details += f"Upkeep Due: {follower.get('upkeep_due', 'N/A')}\n"
            details += f"Description: {follower.get('description', 'No description')}\n\n"
            
            # Upkeep cost
            upkeep_cost = follower.get('cap', 1)
            details += f"Upkeep Cost: {upkeep_cost} XP or Downtime\n"
            
            # Assist info
            details += f"\nAssist Bonus: Up to +{follower.get('cap', 1)} dice\n"
            details += "Can assist in scenes when specialty applies (max +3 dice per roll)"
            
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(1.0, details)
            
    def add_follower_dialog(self):
        """Open dialog to add new follower"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("Add New Follower")
        dialog.geometry("400x400")
        dialog.transient(self.frame)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text="Follower Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Specialty:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        specialty_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=specialty_var, width=30).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Cap (1-5):").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        cap_var = tk.StringVar(value="1")
        cap_combo = ttk.Combobox(dialog, textvariable=cap_var, 
                                values=["1", "2", "3", "4", "5"], width=27)
        cap_combo.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Description:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        desc_text = tk.Text(dialog, height=4, width=30)
        desc_text.grid(row=3, column=1, padx=10, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Add Follower", 
                  command=lambda: self.add_follower(name_var.get(), specialty_var.get(), 
                                                  cap_var.get(), desc_text.get(1.0, tk.END).strip(), dialog)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)
        
    def add_follower(self, name, specialty, cap, description, dialog):
        """Add new follower to list"""
        if not name:
            messagebox.showerror("Error", "Follower name is required")
            return
            
        # Validate cap
        try:
            cap_value = int(cap)
            if not (1 <= cap_value <= 5):
                raise ValueError("Cap must be 1-5")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
            
        # Create follower
        follower = {
            "name": name,
            "specialty": specialty,
            "cap": cap_value,
            "condition": "Maintained",
            "description": description,
            "upkeep_due": "Next Arc"
        }
            
        self.followers.append(follower)
        self.save_followers()
        self.refresh_followers()
        dialog.destroy()
        
    def edit_follower_dialog(self):
        """Edit selected follower"""
        selection = self.follower_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a follower to edit")
            return
            
        item = self.follower_tree.item(selection[0])
        follower_name = item['values'][0]
        follower = next((f for f in self.followers if f['name'] == follower_name), None)
        
        if not follower:
            return
            
        dialog = tk.Toplevel(self.frame)
        dialog.title("Edit Follower")
        dialog.geometry("400x400")
        dialog.transient(self.frame)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text="Follower Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        name_var = tk.StringVar(value=follower['name'])
        ttk.Entry(dialog, textvariable=name_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Specialty:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        specialty_var = tk.StringVar(value=follower.get('specialty', ''))
        ttk.Entry(dialog, textvariable=specialty_var, width=30).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Cap (1-5):").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        cap_var = tk.StringVar(value=str(follower.get('cap', 1)))
        cap_combo = ttk.Combobox(dialog, textvariable=cap_var, 
                                values=["1", "2", "3", "4", "5"], width=27)
        cap_combo.grid(row=2, column=1, padx=10, pady=5)
        
        # Condition
        ttk.Label(dialog, text="Condition:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        condition_var = tk.StringVar(value=follower.get('condition', 'Maintained'))
        condition_combo = ttk.Combobox(dialog, textvariable=condition_var, 
                                      values=["Maintained", "Neglected", "Compromised"], width=27)
        condition_combo.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Upkeep Due:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        upkeep_var = tk.StringVar(value=follower.get('upkeep_due', 'Next Arc'))
        upkeep_combo = ttk.Combobox(dialog, textvariable=upkeep_var, 
                                   values=["Next Arc", "Next Session", "Overdue"], width=27)
        upkeep_combo.grid(row=4, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Description:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        desc_text = tk.Text(dialog, height=4, width=30)
        desc_text.grid(row=5, column=1, padx=10, pady=5)
        desc_text.insert(1.0, follower.get('description', ''))
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Update Follower", 
                  command=lambda: self.update_follower(follower_name, name_var.get(), specialty_var.get(), 
                                                     cap_var.get(), condition_var.get(), 
                                                     upkeep_var.get(), desc_text.get(1.0, tk.END).strip(), dialog)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)
        
    def update_follower(self, old_name, name, specialty, cap, condition, upkeep_due, description, dialog):
        """Update existing follower"""
        # Find and update follower
        for follower in self.followers:
            if follower['name'] == old_name:
                follower['name'] = name
                follower['specialty'] = specialty
                follower['cap'] = int(cap)
                follower['condition'] = condition
                follower['upkeep_due'] = upkeep_due
                follower['description'] = description
                break
                
        self.save_followers()
        self.refresh_followers()
        dialog.destroy()
        
    def delete_follower(self):
        """Delete selected follower"""
        selection = self.follower_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a follower to delete")
            return
            
        item = self.follower_tree.item(selection[0])
        follower_name = item['values'][0]
        
        if messagebox.askyesno("Confirm Delete", f"Delete follower '{follower_name}'?"):
            self.followers = [f for f in self.followers if f['name'] != follower_name]
            self.save_followers()
            self.refresh_followers()
            
    def maintain_follower(self):
        """Maintain selected follower"""
        selection = self.follower_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a follower to maintain")
            return
            
        item = self.follower_tree.item(selection[0])
        follower_name = item['values'][0]
        
        # Find and update follower
        for follower in self.followers:
            if follower['name'] == follower_name:
                old_condition = follower.get('condition', 'Maintained')
                follower['condition'] = 'Maintained'
                self.save_followers()
                self.refresh_followers()
                messagebox.showinfo("Maintenance", f"Follower '{follower_name}' maintained!\n\nCondition changed from {old_condition} to Maintained.")
                break
                
    def pay_upkeep(self):
        """Pay upkeep for selected follower"""
        selection = self.follower_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a follower to pay upkeep for")
            return
            
        item = self.follower_tree.item(selection[0])
        follower_name = item['values'][0]
        
        follower = next((f for f in self.followers if f['name'] == follower_name), None)
        if not follower:
            return
            
        # Calculate upkeep cost
        cost = follower.get('cap', 1)
            
        # In a real implementation, this would interact with the XP system
        follower['condition'] = 'Maintained'
        follower['upkeep_due'] = 'Next Arc'
        self.save_followers()
        self.refresh_followers()
        
        messagebox.showinfo("Upkeep Paid", f"Paid {cost} XP upkeep for '{follower_name}'\n\nFollower is now Maintained and upkeep due Next Arc.")
        
    def promote_follower(self):
        """Promote selected follower (increase Cap)"""
        selection = self.follower_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a follower to promote")
            return
            
        item = self.follower_tree.item(selection[0])
        follower_name = item['values'][0]
        
        follower = next((f for f in self.followers if f['name'] == follower_name), None)
        if not follower:
            return
            
        current_cap = follower.get('cap', 1)
        if current_cap >= 5:
            messagebox.showwarning("Max Cap", "Follower is already at maximum Cap (5)")
            return
            
        new_cap = current_cap + 1
        cost = new_cap ** 2 - current_cap ** 2  # Difference in XP cost
        
        if messagebox.askyesno("Promote Follower", 
                              f"Promote {follower_name} from Cap {current_cap} to {new_cap}?\n\n"
                              f"This will cost {cost} XP."):
            follower['cap'] = new_cap
            self.save_followers()
            self.refresh_followers()
            messagebox.showinfo("Promoted", f"{follower_name} promoted to Cap {new_cap}!")
        
    def get_frame(self):
        return self.frame

