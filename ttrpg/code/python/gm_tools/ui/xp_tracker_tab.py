# ui/xp_tracker_tab.py
import tkinter as tk
from tkinter import ttk

class XPTrackerTab:
    def __init__(self, parent):
        self.parent = parent
        self.players = {}  # {player_name: {"total": xp_amount, "spent": xp_spent, "history": []}}
        self.session_log = []  # Session XP awards
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="XP Tracker", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Session Controls
        session_frame = ttk.LabelFrame(self.parent, text="Session Management", padding="15")
        session_frame.pack(fill="x", padx=20, pady=10)
        
        # Session XP Award
        award_frame = ttk.Frame(session_frame)
        award_frame.pack(side="left", padx=10)
        ttk.Label(award_frame, text="Session XP:").pack()
        self.session_xp_var = tk.StringVar(value="6")
        session_combo = ttk.Combobox(award_frame, textvariable=self.session_xp_var,
                                   values=["4", "6", "8", "10", "12", "14"],
                                   width=5, state="readonly")
        session_combo.pack(pady=5)
        ttk.Button(award_frame, text="Award Session XP", command=self.award_session_xp).pack()
        
        # Custom Award
        custom_frame = ttk.Frame(session_frame)
        custom_frame.pack(side="left", padx=20)
        ttk.Label(custom_frame, text="Custom Award:").pack()
        self.custom_xp_entry = ttk.Entry(custom_frame, width=8)
        self.custom_xp_entry.pack(pady=5)
        ttk.Button(custom_frame, text="Award Custom XP", command=self.award_custom_xp).pack()
        
        # Session Log
        log_frame = ttk.Frame(session_frame)
        log_frame.pack(side="right")
        ttk.Button(log_frame, text="Clear Session Log", command=self.clear_session_log).pack(pady=5)
        
        # Player Management
        player_frame = ttk.LabelFrame(self.parent, text="Player Management", padding="15")
        player_frame.pack(fill="x", padx=20, pady=10)
        
        # Add Player
        add_frame = ttk.Frame(player_frame)
        add_frame.pack(fill="x", pady=5)
        ttk.Label(add_frame, text="Player Name:").pack(side="left")
        self.player_name_entry = ttk.Entry(add_frame, width=15)
        self.player_name_entry.pack(side="left", padx=5)
        ttk.Label(add_frame, text="Starting XP:").pack(side="left", padx=(20,0))
        self.starting_xp_entry = ttk.Entry(add_frame, width=8)
        self.starting_xp_entry.pack(side="left", padx=5)
        self.starting_xp_entry.insert(0, "30")
        ttk.Button(add_frame, text="Add Player", command=self.add_player).pack(side="left", padx=10)
        ttk.Button(add_frame, text="Clear All Players", command=self.clear_players).pack(side="left", padx=5)
        
        # Players Display
        self.players_display_frame = ttk.Frame(player_frame)
        self.players_display_frame.pack(fill="both", expand=True, pady=10)
        
        # XP Spending Section
        spend_frame = ttk.LabelFrame(self.parent, text="XP Spending", padding="15")
        spend_frame.pack(fill="x", padx=20, pady=10)
        
        # Quick Spend Categories
        categories_frame = ttk.Frame(spend_frame)
        categories_frame.pack(fill="x")
        
        # Attributes
        attr_frame = ttk.LabelFrame(categories_frame, text="Attributes", padding="10")
        attr_frame.pack(side="left", fill="y", padx=5)
        ttk.Button(attr_frame, text="Raise Attribute", command=self.raise_attribute_dialog).pack(pady=2)
        ttk.Label(attr_frame, text="Cost: (new rating × 3) XP", font=("Arial", 8)).pack()
        
        # Skills
        skill_frame = ttk.LabelFrame(categories_frame, text="Skills", padding="10")
        skill_frame.pack(side="left", fill="y", padx=5)
        ttk.Button(skill_frame, text="Raise Skill", command=self.raise_skill_dialog).pack(pady=2)
        ttk.Label(skill_frame, text="Cost: (new level × 2) XP", font=("Arial", 8)).pack()
        
        # Followers
        follower_frame = ttk.LabelFrame(categories_frame, text="Followers", padding="10")
        follower_frame.pack(side="left", fill="y", padx=5)
        ttk.Button(follower_frame, text="Buy Follower", command=self.buy_follower_dialog).pack(pady=2)
        ttk.Label(follower_frame, text="Cost: Cap² XP", font=("Arial", 8)).pack()
        
        # Assets
        asset_frame = ttk.LabelFrame(categories_frame, text="Assets", padding="10")
        asset_frame.pack(side="left", fill="y", padx=5)
        ttk.Button(asset_frame, text="Buy Asset", command=self.buy_asset_dialog).pack(pady=2)
        ttk.Label(asset_frame, text="Minor: 4 XP, Standard: 8 XP, Major: 12 XP", font=("Arial", 8)).pack()
        
        # Custom Spend
        custom_spend_frame = ttk.LabelFrame(categories_frame, text="Custom", padding="10")
        custom_spend_frame.pack(side="left", fill="y", padx=5)
        ttk.Button(custom_spend_frame, text="Custom Spend", command=self.custom_spend_dialog).pack(pady=2)
        ttk.Button(custom_spend_frame, text="Refund XP", command=self.refund_xp_dialog).pack(pady=2)
        
        # XP History
        history_frame = ttk.LabelFrame(self.parent, text="XP History", padding="10")
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        history_control_frame = ttk.Frame(history_frame)
        history_control_frame.pack(fill="x", pady=5)
        ttk.Button(history_control_frame, text="Clear History", command=self.clear_history).pack(side="right")
        
        self.history_display_frame = ttk.Frame(history_frame)
        self.history_display_frame.pack(fill="both", expand=True)
        
        # XP Info
        info_frame = ttk.LabelFrame(self.parent, text="XP Information", padding="10")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
XP in Fate's Edge:
• Starting XP: 30 XP for character creation
• Session Awards: 4-14 XP depending on campaign pace
• Spending Paths:
  - Enhance Self: Attributes (new rating × 3 XP), Skills (new level × 2 XP)
  - Acquire Assets: Followers (Cap² XP), Off-Screen Assets (4/8/12 XP)
  - Learn Talents: Various costs (3-20 XP)

Session Award Guidelines:
• Gritty Pace: 4-6 XP per session (slow burn)
• Standard Pace: 6-10 XP per session (default)
• Heroic Pace: 10-14 XP per session (fast growth)

Award Triggers:
• Table Attendance: +2 XP
• Major Objective Reached: +2-4 XP
• Discovery or Lore Unlocked: +1-2 XP
• Hard Choice Embraced: +1-2 XP
• Complication Spotlight: +1-3 XP
• Bond/Flag Driven Play: +1-2 XP
• GM Curveball Award: +0-3 XP

Milestone Awards:
• End of Major Arc: +8-12 XP to all players
• Signature Moment: +2 XP bonus
        """.strip()
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack()
        
        self.refresh_players_display()
        self.refresh_history_display()
        
    def add_player(self):
        name = self.player_name_entry.get().strip()
        starting_xp = self.starting_xp_entry.get().strip()
        
        if name and name not in self.players:
            try:
                xp = int(starting_xp) if starting_xp else 30
                self.players[name] = {
                    "total": xp,
                    "spent": 0,
                    "available": xp,
                    "history": []
                }
                self.player_name_entry.delete(0, tk.END)
                self.refresh_players_display()
                self.log_history("Add Player", name, xp, f"Starting XP: {xp}")
            except ValueError:
                pass  # Invalid XP value
                
    def clear_players(self):
        self.players = {}
        self.refresh_players_display()
        self.refresh_history_display()
        
    def award_session_xp(self):
        try:
            xp_amount = int(self.session_xp_var.get())
            for player_name in self.players:
                self.players[player_name]["total"] += xp_amount
                self.players[player_name]["available"] += xp_amount
                self.log_history("Session Award", player_name, xp_amount, f"Session XP")
            self.log_session(f"Awarded {xp_amount} XP to all players")
            self.refresh_players_display()
        except ValueError:
            pass
            
    def award_custom_xp(self):
        try:
            xp_amount = int(self.custom_xp_entry.get().strip())
            if xp_amount > 0:
                # Would need player selection in full implementation
                for player_name in self.players:
                    self.players[player_name]["total"] += xp_amount
                    self.players[player_name]["available"] += xp_amount
                    self.log_history("Custom Award", player_name, xp_amount, f"Custom XP")
                self.log_session(f"Awarded {xp_amount} custom XP to all players")
                self.custom_xp_entry.delete(0, tk.END)
                self.refresh_players_display()
        except ValueError:
            pass
            
    def raise_attribute_dialog(self):
        if not self.players:
            return
            
        dialog = tk.Toplevel(self.parent)
        dialog.title("Raise Attribute")
        dialog.geometry("350x250")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Raise Attribute", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Player Selection
        player_frame = ttk.Frame(dialog)
        player_frame.pack(pady=5)
        ttk.Label(player_frame, text="Player:").pack()
        player_var = tk.StringVar()
        player_combo = ttk.Combobox(player_frame, textvariable=player_var,
                                  values=list(self.players.keys()),
                                  state="readonly", width=20)
        player_combo.pack(pady=5)
        if self.players:
            player_combo.set(list(self.players.keys())[0])
            
        # Attribute Details
        attr_frame = ttk.Frame(dialog)
        attr_frame.pack(pady=10)
        ttk.Label(attr_frame, text="New Attribute Rating:").pack()
        rating_var = tk.StringVar()
        rating_combo = ttk.Combobox(attr_frame, textvariable=rating_var,
                                  values=["2", "3", "4", "5"],
                                  state="readonly", width=10)
        rating_combo.pack(pady=5)
        rating_combo.set("2")
        
        # Cost Display
        cost_label = ttk.Label(dialog, text="Cost: 6 XP", font=("Arial", 10, "bold"))
        cost_label.pack(pady=5)
        
        def update_cost(*args):
            try:
                rating = int(rating_var.get())
                cost = rating * 3
                cost_label.config(text=f"Cost: {cost} XP")
            except ValueError:
                cost_label.config(text="Cost: ? XP")
                
        rating_var.trace("w", update_cost)
        
        def raise_attribute():
            player = player_var.get()
            try:
                new_rating = int(rating_var.get())
                cost = new_rating * 3
                if player in self.players and self.players[player]["available"] >= cost:
                    self.players[player]["available"] -= cost
                    self.players[player]["spent"] += cost
                    self.players[player]["history"].append({
                        "type": "Attribute",
                        "amount": cost,
                        "details": f"Raised attribute to {new_rating}"
                    })
                    self.log_history("Spend", player, cost, f"Raised attribute to {new_rating}")
                    self.refresh_players_display()
                    dialog.destroy()
            except ValueError:
                pass
                
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Raise Attribute", command=raise_attribute).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def raise_skill_dialog(self):
        if not self.players:
            return
            
        dialog = tk.Toplevel(self.parent)
        dialog.title("Raise Skill")
        dialog.geometry("350x250")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Raise Skill", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Player Selection
        player_frame = ttk.Frame(dialog)
        player_frame.pack(pady=5)
        ttk.Label(player_frame, text="Player:").pack()
        player_var = tk.StringVar()
        player_combo = ttk.Combobox(player_frame, textvariable=player_var,
                                  values=list(self.players.keys()),
                                  state="readonly", width=20)
        player_combo.pack(pady=5)
        if self.players:
            player_combo.set(list(self.players.keys())[0])
            
        # Skill Details
        skill_frame = ttk.Frame(dialog)
        skill_frame.pack(pady=10)
        ttk.Label(skill_frame, text="Skill Name:").pack()
        skill_entry = ttk.Entry(skill_frame, width=20)
        skill_entry.pack(pady=5)
        
        ttk.Label(skill_frame, text="New Skill Level:").pack()
        level_var = tk.StringVar()
        level_combo = ttk.Combobox(skill_frame, textvariable=level_var,
                                 values=["1", "2", "3", "4", "5"],
                                 state="readonly", width=10)
        level_combo.pack(pady=5)
        level_combo.set("1")
        
        # Cost Display
        cost_label = ttk.Label(dialog, text="Cost: 2 XP", font=("Arial", 10, "bold"))
        cost_label.pack(pady=5)
        
        def update_cost(*args):
            try:
                level = int(level_var.get())
                cost = level * 2
                cost_label.config(text=f"Cost: {cost} XP")
            except ValueError:
                cost_label.config(text="Cost: ? XP")
                
        level_var.trace("w", update_cost)
        
        def raise_skill():
            player = player_var.get()
            skill_name = skill_entry.get().strip()
            try:
                new_level = int(level_var.get())
                cost = new_level * 2
                if player in self.players and self.players[player]["available"] >= cost and skill_name:
                    self.players[player]["available"] -= cost
                    self.players[player]["spent"] += cost
                    self.players[player]["history"].append({
                        "type": "Skill",
                        "amount": cost,
                        "details": f"Raised {skill_name} to {new_level}"
                    })
                    self.log_history("Spend", player, cost, f"Raised {skill_name} to {new_level}")
                    self.refresh_players_display()
                    dialog.destroy()
            except ValueError:
                pass
                
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Raise Skill", command=raise_skill).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def buy_follower_dialog(self):
        if not self.players:
            return
            
        dialog = tk.Toplevel(self.parent)
        dialog.title("Buy Follower")
        dialog.geometry("350x300")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Buy Follower", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Player Selection
        player_frame = ttk.Frame(dialog)
        player_frame.pack(pady=5)
        ttk.Label(player_frame, text="Player:").pack()
        player_var = tk.StringVar()
        player_combo = ttk.Combobox(player_frame, textvariable=player_var,
                                  values=list(self.players.keys()),
                                  state="readonly", width=20)
        player_combo.pack(pady=5)
        if self.players:
            player_combo.set(list(self.players.keys())[0])
            
        # Follower Details
        follower_frame = ttk.Frame(dialog)
        follower_frame.pack(pady=10)
        ttk.Label(follower_frame, text="Follower Name:").pack()
        name_entry = ttk.Entry(follower_frame, width=20)
        name_entry.pack(pady=5)
        
        ttk.Label(follower_frame, text="Specialty:").pack()
        specialty_entry = ttk.Entry(follower_frame, width=20)
        specialty_entry.pack(pady=5)
        
        ttk.Label(follower_frame, text="Cap Rating:").pack()
        cap_var = tk.StringVar()
        cap_combo = ttk.Combobox(follower_frame, textvariable=cap_var,
                               values=["1", "2", "3", "4", "5"],
                               state="readonly", width=10)
        cap_combo.pack(pady=5)
        cap_combo.set("2")
        
        # Cost Display
        cost_label = ttk.Label(dialog, text="Cost: 4 XP", font=("Arial", 10, "bold"))
        cost_label.pack(pady=5)
        
        def update_cost(*args):
            try:
                cap = int(cap_var.get())
                cost = cap * cap  # Cap²
                cost_label.config(text=f"Cost: {cost} XP")
            except ValueError:
                cost_label.config(text="Cost: ? XP")
                
        cap_var.trace("w", update_cost)
        
        def buy_follower():
            player = player_var.get()
            name = name_entry.get().strip()
            specialty = specialty_entry.get().strip()
            try:
                cap = int(cap_var.get())
                cost = cap * cap
                if player in self.players and self.players[player]["available"] >= cost and name:
                    self.players[player]["available"] -= cost
                    self.players[player]["spent"] += cost
                    self.players[player]["history"].append({
                        "type": "Follower",
                        "amount": cost,
                        "details": f"Bought {name} (Cap {cap}) - {specialty}"
                    })
                    self.log_history("Spend", player, cost, f"Bought follower {name} (Cap {cap})")
                    self.refresh_players_display()
                    dialog.destroy()
            except ValueError:
                pass
                
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Buy Follower", command=buy_follower).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def buy_asset_dialog(self):
        if not self.players:
            return
            
        dialog = tk.Toplevel(self.parent)
        dialog.title("Buy Asset")
        dialog.geometry("350x250")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Buy Off-Screen Asset", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Player Selection
        player_frame = ttk.Frame(dialog)
        player_frame.pack(pady=5)
        ttk.Label(player_frame, text="Player:").pack()
        player_var = tk.StringVar()
        player_combo = ttk.Combobox(player_frame, textvariable=player_var,
                                  values=list(self.players.keys()),
                                  state="readonly", width=20)
        player_combo.pack(pady=5)
        if self.players:
            player_combo.set(list(self.players.keys())[0])
            
        # Asset Details
        asset_frame = ttk.Frame(dialog)
        asset_frame.pack(pady=10)
        ttk.Label(asset_frame, text="Asset Name:").pack()
        name_entry = ttk.Entry(asset_frame, width=20)
        name_entry.pack(pady=5)
        
        ttk.Label(asset_frame, text="Asset Tier:").pack()
        tier_var = tk.StringVar()
        tier_combo = ttk.Combobox(asset_frame, textvariable=tier_var,
                                values=["Minor (4 XP)", "Standard (8 XP)", "Major (12 XP)"],
                                state="readonly", width=20)
        tier_combo.pack(pady=5)
        tier_combo.set("Standard (8 XP)")
        
        def buy_asset():
            player = player_var.get()
            name = name_entry.get().strip()
            tier_text = tier_var.get()
            
            # Extract cost from tier text
            if "4 XP" in tier_text:
                cost, tier = 4, "Minor"
            elif "8 XP" in tier_text:
                cost, tier = 8, "Standard"
            elif "12 XP" in tier_text:
                cost, tier = 12, "Major"
            else:
                return
                
            if player in self.players and self.players[player]["available"] >= cost and name:
                self.players[player]["available"] -= cost
                self.players[player]["spent"] += cost
                self.players[player]["history"].append({
                    "type": "Asset",
                    "amount": cost,
                    "details": f"Bought {name} ({tier})"
                })
                self.log_history("Spend", player, cost, f"Bought asset {name} ({tier})")
                self.refresh_players_display()
                dialog.destroy()
                
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Buy Asset", command=buy_asset).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def custom_spend_dialog(self):
        if not self.players:
            return
            
        dialog = tk.Toplevel(self.parent)
        dialog.title("Custom XP Spend")
        dialog.geometry("350x250")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Custom XP Spend", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Player Selection
        player_frame = ttk.Frame(dialog)
        player_frame.pack(pady=5)
        ttk.Label(player_frame, text="Player:").pack()
        player_var = tk.StringVar()
        player_combo = ttk.Combobox(player_frame, textvariable=player_var,
                                  values=list(self.players.keys()),
                                  state="readonly", width=20)
        player_combo.pack(pady=5)
        if self.players:
            player_combo.set(list(self.players.keys())[0])
            
        # Spend Details
        spend_frame = ttk.Frame(dialog)
        spend_frame.pack(pady=10)
        ttk.Label(spend_frame, text="XP Amount:").pack()
        amount_entry = ttk.Entry(spend_frame, width=10)
        amount_entry.pack(pady=5)
        
        ttk.Label(spend_frame, text="Description:").pack()
        desc_entry = ttk.Entry(spend_frame, width=30)
        desc_entry.pack(pady=5)
        
        def custom_spend():
            player = player_var.get()
            try:
                amount = int(amount_entry.get().strip())
                description = desc_entry.get().strip()
                if player in self.players and self.players[player]["available"] >= amount and amount > 0 and description:
                    self.players[player]["available"] -= amount
                    self.players[player]["spent"] += amount
                    self.players[player]["history"].append({
                        "type": "Custom",
                        "amount": amount,
                        "details": description
                    })
                    self.log_history("Spend", player, amount, description)
                    self.refresh_players_display()
                    dialog.destroy()
            except ValueError:
                pass
                
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Spend XP", command=custom_spend).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def refund_xp_dialog(self):
        if not self.players:
            return
            
        dialog = tk.Toplevel(self.parent)
        dialog.title("Refund XP")
        dialog.geometry("350x200")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Refund XP", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Player Selection
        player_frame = ttk.Frame(dialog)
        player_frame.pack(pady=5)
        ttk.Label(player_frame, text="Player:").pack()
        player_var = tk.StringVar()
        player_combo = ttk.Combobox(player_frame, textvariable=player_var,
                                  values=list(self.players.keys()),
                                  state="readonly", width=20)
        player_combo.pack(pady=5)
        if self.players:
            player_combo.set(list(self.players.keys())[0])
            
        # Refund Details
        refund_frame = ttk.Frame(dialog)
        refund_frame.pack(pady=10)
        ttk.Label(refund_frame, text="XP Amount:").pack()
        amount_entry = ttk.Entry(refund_frame, width=10)
        amount_entry.pack(pady=5)
        amount_entry.insert(0, "1")
        
        ttk.Label(refund_frame, text="Reason:").pack()
        reason_entry = ttk.Entry(refund_frame, width=25)
        reason_entry.pack(pady=5)
        
        def refund_xp():
            player = player_var.get()
            try:
                amount = int(amount_entry.get().strip())
                reason = reason_entry.get().strip() or "Refund"
                if player in self.players and amount > 0:
                    # Add XP back to available (spent tracking remains for history)
                    self.players[player]["available"] += amount
                    self.log_history("Refund", player, amount, reason)
                    self.refresh_players_display()
                    dialog.destroy()
            except ValueError:
                pass
                
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Refund XP", command=refund_xp).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def log_history(self, action, player, amount, description):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = {
            "timestamp": timestamp,
            "action": action,
            "player": player,
            "amount": amount,
            "description": description
        }
        # Add to global history
        self.session_log.append(history_entry)
        self.refresh_history_display()
        
    def log_session(self, description):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        session_entry = {
            "timestamp": timestamp,
            "action": "Session",
            "player": "ALL",
            "amount": 0,
            "description": description
        }
        self.session_log.append(session_entry)
        self.refresh_history_display()
        
    def clear_session_log(self):
        self.session_log = []
        self.refresh_history_display()
        
    def clear_history(self):
        # Clear individual player histories
        for player_data in self.players.values():
            player_data["history"] = []
        self.session_log = []
        self.refresh_history_display()
        
    def refresh_players_display(self):
        # Clear existing widgets
        for widget in self.players_display_frame.winfo_children():
            widget.destroy()
            
        if not self.players:
            ttk.Label(self.players_display_frame, text="No players added").pack(pady=20)
            return
            
        # Create scrollable area
        canvas = tk.Canvas(self.players_display_frame)
        scrollbar = ttk.Scrollbar(self.players_display_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display players
        for player_name, player_data in self.players.items():
            player_frame = ttk.LabelFrame(scrollable_frame, text=player_name, padding="10")
            player_frame.pack(fill="x", pady=5, padx=5)
            
            # XP Summary
            summary_frame = ttk.Frame(player_frame)
            summary_frame.pack(fill="x", pady=5)
            
            ttk.Label(summary_frame, text=f"Total XP: {player_data['total']}", 
                     font=("Arial", 10, "bold")).pack(side="left", padx=10)
            ttk.Label(summary_frame, text=f"Available: {player_data['available']}", 
                     foreground="green" if player_data['available'] > 0 else "red",
                     font=("Arial", 10, "bold")).pack(side="left", padx=10)
            ttk.Label(summary_frame, text=f"Spent: {player_data['spent']}", 
                     foreground="blue",
                     font=("Arial", 10, "bold")).pack(side="left", padx=10)
            
            # Player Controls
            control_frame = ttk.Frame(player_frame)
            control_frame.pack(fill="x", pady=5)
            
            ttk.Button(control_frame, text="View History", 
                      command=lambda p=player_name: self.view_player_history(p)).pack(side="left", padx=5)
            ttk.Button(control_frame, text="Add XP", 
                      command=lambda p=player_name: self.add_xp_dialog(p)).pack(side="left", padx=5)
            ttk.Button(control_frame, text="Remove Player", 
                      command=lambda p=player_name: self.remove_player(p)).pack(side="right", padx=5)
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def refresh_history_display(self):
        # Clear existing widgets
        for widget in self.history_display_frame.winfo_children():
            widget.destroy()
            
        if not self.session_log:
            ttk.Label(self.history_display_frame, text="No XP transactions logged").pack(pady=20)
            return
            
        # Create scrollable area
        canvas = tk.Canvas(self.history_display_frame)
        scrollbar = ttk.Scrollbar(self.history_display_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display history entries (most recent first)
        for entry in reversed(self.session_log[-50:]):  # Show last 50 entries
            entry_frame = ttk.Frame(scrollable_frame)
            entry_frame.pack(fill="x", pady=2, padx=5)
            
            # Timestamp
            ttk.Label(entry_frame, text=entry["timestamp"], width=10).pack(side="left", padx=5)
            
            # Action
            action_colors = {
                "Spend": "red",
                "Add Player": "green",
                "Session Award": "blue",
                "Custom Award": "purple",
                "Refund": "orange",
                "Session": "gray"
            }
            action_color = action_colors.get(entry["action"], "black")
            ttk.Label(entry_frame, text=entry["action"], foreground=action_color, width=15).pack(side="left", padx=5)
            
            # Player
            ttk.Label(entry_frame, text=entry["player"], width=15).pack(side="left", padx=5)
            
            # Amount
            if entry["amount"] > 0:
                ttk.Label(entry_frame, text=f"{entry['amount']} XP", width=10).pack(side="left", padx=5)
            
            # Description
            ttk.Label(entry_frame, text=entry["description"], wraplength=300).pack(side="left", padx=5, fill="x", expand=True)
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def view_player_history(self, player_name):
        if player_name not in self.players:
            return
            
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"XP History - {player_name}")
        dialog.geometry("500x400")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Player total info
        info_frame = ttk.Frame(dialog)
        info_frame.pack(fill="x", padx=20, pady=10)
        player_data = self.players[player_name]
        ttk.Label(info_frame, text=f"Total: {player_data['total']} | Available: {player_data['available']} | Spent: {player_data['spent']}",
                 font=("Arial", 12, "bold")).pack()
        
        # History display
        history_frame = ttk.Frame(dialog)
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(history_frame)
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display player history
        for entry in reversed(player_data["history"][-30:]):  # Show last 30 entries
            entry_frame = ttk.Frame(scrollable_frame)
            entry_frame.pack(fill="x", pady=2, padx=5)
            
            ttk.Label(entry_frame, text=entry["type"], width=12).pack(side="left", padx=5)
            ttk.Label(entry_frame, text=f"{entry['amount']} XP", width=10).pack(side="left", padx=5)
            ttk.Label(entry_frame, text=entry["details"], wraplength=300).pack(side="left", padx=5, fill="x", expand=True)
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def add_xp_dialog(self, player_name):
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Add XP to {player_name}")
        dialog.geometry("250x150")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Add XP to {player_name}").pack(pady=10)
        
        amount_frame = ttk.Frame(dialog)
        amount_frame.pack(pady=5)
        ttk.Label(amount_frame, text="Amount:").pack(side="left")
        amount_entry = ttk.Entry(amount_frame, width=10)
        amount_entry.pack(side="left", padx=5)
        amount_entry.insert(0, "1")
        
        reason_frame = ttk.Frame(dialog)
        reason_frame.pack(pady=5)
        ttk.Label(reason_frame, text="Reason:").pack(side="left")
        reason_entry = ttk.Entry(reason_frame, width=15)
        reason_entry.pack(side="left", padx=5)
        
        def add_xp():
            try:
                amount = int(amount_entry.get().strip())
                reason = reason_entry.get().strip() or "Manual addition"
                if amount > 0 and player_name in self.players:
                    self.players[player_name]["total"] += amount
                    self.players[player_name]["available"] += amount
                    self.log_history("Custom Award", player_name, amount, reason)
                    self.refresh_players_display()
                    dialog.destroy()
            except ValueError:
                pass
                
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Add XP", command=add_xp).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def remove_player(self, player_name):
        if player_name in self.players:
            del self.players[player_name]
            self.refresh_players_display()
