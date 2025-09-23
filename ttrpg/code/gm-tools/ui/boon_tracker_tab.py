# ui/boon_tracker_tab.py
import tkinter as tk
from tkinter import ttk

class BoonTrackerTab:
    def __init__(self, parent):
        self.parent = parent
        self.player_boons = {}  # {player_name: boon_count}
        self.party_boons = 0    # Shared boons that any player can use
        self.boon_log = []      # Log of boon transactions
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Boon Tracker", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Boon Summary
        summary_frame = ttk.LabelFrame(self.parent, text="Boon Summary", padding="15")
        summary_frame.pack(fill="x", padx=20, pady=10)
        
        # Party Boons
        party_frame = ttk.Frame(summary_frame)
        party_frame.pack(side="left", padx=20)
        ttk.Label(party_frame, text="Party Boons:", font=("Arial", 12, "bold")).pack()
        self.party_label = ttk.Label(party_frame, text=f"{self.party_boons}", 
                                   font=("Arial", 16, "bold"), foreground="gold")
        self.party_label.pack()
        
        # Total Player Boons
        total_frame = ttk.Frame(summary_frame)
        total_frame.pack(side="left", padx=20)
        total_player_boons = sum(self.player_boons.values())
        ttk.Label(total_frame, text="Total Player Boons:", font=("Arial", 12, "bold")).pack()
        self.total_label = ttk.Label(total_frame, text=f"{total_player_boons}", 
                                   font=("Arial", 16, "bold"), foreground="blue")
        self.total_label.pack()
        
        # Controls
        control_frame = ttk.Frame(summary_frame)
        control_frame.pack(side="right")
        ttk.Button(control_frame, text="Add Party Boon", command=self.add_party_boon).pack(pady=2)
        ttk.Button(control_frame, text="Spend Party Boon", command=self.spend_party_boon).pack(pady=2)
        
        # Player Boons Section
        players_frame = ttk.LabelFrame(self.parent, text="Player Boons", padding="15")
        players_frame.pack(fill="x", padx=20, pady=10)
        
        # Add Player Section
        add_frame = ttk.Frame(players_frame)
        add_frame.pack(fill="x", pady=10)
        
        ttk.Label(add_frame, text="Player Name:").pack(side="left")
        self.player_entry = ttk.Entry(add_frame, width=15)
        self.player_entry.pack(side="left", padx=5)
        
        ttk.Button(add_frame, text="Add Player", command=self.add_player).pack(side="left", padx=10)
        ttk.Button(add_frame, text="Clear All Players", command=self.clear_players).pack(side="left", padx=5)
        
        # Players Display
        self.players_display_frame = ttk.Frame(players_frame)
        self.players_display_frame.pack(fill="both", expand=True)
        
        # Boon Actions Section
        actions_frame = ttk.LabelFrame(self.parent, text="Boon Actions", padding="15")
        actions_frame.pack(fill="x", padx=20, pady=10)
        
        # Quick Actions
        quick_frame = ttk.LabelFrame(actions_frame, text="Quick Boon Actions", padding="10")
        quick_frame.pack(side="left", fill="y", padx=10)
        
        ttk.Button(quick_frame, text="Player Earns Boon", command=self.player_earns_boon_dialog).pack(pady=5)
        ttk.Button(quick_frame, text="Player Spends Boon", command=self.player_spends_boon_dialog).pack(pady=5)
        ttk.Button(quick_frame, text="Convert 2 Boons → 1 XP", command=self.convert_boons_dialog).pack(pady=5)
        
        # Asset Activation
        asset_frame = ttk.LabelFrame(actions_frame, text="Asset Activation Costs", padding="10")
        asset_frame.pack(side="left", fill="y", padx=10)
        
        ttk.Label(asset_frame, text="Standard Asset Activation:", font=("Arial", 9, "bold")).pack()
        ttk.Label(asset_frame, text="1 Boon (preferred) or 2 XP").pack()
        ttk.Button(asset_frame, text="Spend for Asset", command=self.asset_activation_dialog).pack(pady=5)
        
        # Re-roll Actions
        reroll_frame = ttk.LabelFrame(actions_frame, text="Re-roll Actions", padding="10")
        reroll_frame.pack(side="left", fill="y", padx=10)
        
        ttk.Label(reroll_frame, text="Re-roll Cost: 1 Boon", font=("Arial", 9, "bold")).pack()
        ttk.Button(reroll_frame, text="Spend for Re-roll", command=self.reroll_dialog).pack(pady=5)
        
        # Boon Log
        log_frame = ttk.LabelFrame(self.parent, text="Boon Log", padding="10")
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        log_control_frame = ttk.Frame(log_frame)
        log_control_frame.pack(fill="x", pady=5)
        
        ttk.Button(log_control_frame, text="Clear Log", command=self.clear_log).pack(side="right")
        
        self.log_display_frame = ttk.Frame(log_frame)
        self.log_display_frame.pack(fill="both", expand=True)
        
        # Boon Info
        info_frame = ttk.LabelFrame(self.parent, text="Boon Information", padding="10")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
Boon System in Fate's Edge:
• Players earn boons from meaningful failure and complications
• Maximum 5 boons per player at any time
• Overflow boons convert to XP (2 boons = 1 XP, up to 2 XP per session)
• Boons can be spent for:
  - Re-rolling a single die (1 boon)
  - Activating Off-Screen Assets (1 boon preferred, 2 XP emergency)
  - Converting to XP between sessions (2 boons = 1 XP)

Boon Earning Guidelines:
• Award boons when failure has narrative teeth
• GM should introduce complications to earn boons
• Boons represent learning from mistakes and seizing opportunities
• Empty actions taken solely to trigger failure do NOT qualify

Design Philosophy:
• Boons ensure failure still rewards play
• They turn setbacks into fuel for later triumphs
• Every boon represents a lesson paid for with genuine dramatic weight
        """.strip()
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack()
        
        self.refresh_players_display()
        self.refresh_log_display()
        
    def add_party_boon(self):
        self.party_boons += 1
        self.update_summary()
        self.log_transaction("Add", "Party", 1, "Added party boon")
        
    def spend_party_boon(self):
        if self.party_boons > 0:
            self.party_boons -= 1
            self.update_summary()
            self.log_transaction("Spend", "Party", 1, "Spent party boon")
            
    def add_player(self):
        name = self.player_entry.get().strip()
        if name and name not in self.player_boons:
            self.player_boons[name] = 0
            self.player_entry.delete(0, tk.END)
            self.refresh_players_display()
            self.update_summary()
            
    def clear_players(self):
        self.player_boons = {}
        self.refresh_players_display()
        self.update_summary()
        
    def add_player_boon(self, player_name):
        if player_name in self.player_boons and self.player_boons[player_name] < 5:
            self.player_boons[player_name] += 1
            self.refresh_players_display()
            self.update_summary()
            self.log_transaction("Add", player_name, 1, "Earned boon from complication")
            
    def spend_player_boon(self, player_name):
        if player_name in self.player_boons and self.player_boons[player_name] > 0:
            self.player_boons[player_name] -= 1
            self.refresh_players_display()
            self.update_summary()
            self.log_transaction("Spend", player_name, 1, "Spent boon")
            
    def convert_boons_to_xp(self, player_name):
        if player_name in self.player_boons and self.player_boons[player_name] >= 2:
            boons_to_convert = min(2, self.player_boons[player_name])  # Max 2 boons per conversion
            xp_gained = boons_to_convert // 2
            self.player_boons[player_name] -= boons_to_convert
            self.refresh_players_display()
            self.update_summary()
            self.log_transaction("Convert", player_name, boons_to_convert, f"Converted to {xp_gained} XP")
            
    def player_earns_boon_dialog(self):
        if not self.player_boons:
            return
            
        dialog = tk.Toplevel(self.parent)
        dialog.title("Player Earns Boon")
        dialog.geometry("300x200")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select Player:").pack(pady=10)
        
        player_var = tk.StringVar()
        player_combo = ttk.Combobox(dialog, textvariable=player_var,
                                  values=list(self.player_boons.keys()),
                                  state="readonly")
        player_combo.pack(pady=5)
        if self.player_boons:
            player_combo.set(list(self.player_boons.keys())[0])
            
        ttk.Label(dialog, text="Reason:").pack(pady=(10,5))
        reason_entry = ttk.Entry(dialog, width=30)
        reason_entry.pack(pady=5)
        
        def earn_boon():
            player = player_var.get()
            reason = reason_entry.get().strip() or "Complication"
            if player:
                if self.player_boons[player] < 5:
                    self.add_player_boon(player)
                    self.log_transaction("Add", player, 1, f"Earned: {reason}")
                else:
                    # Handle overflow - convert to XP
                    self.convert_boons_to_xp(player)
                    self.log_transaction("Add+Convert", player, 1, f"Overflow: {reason} (converted to XP)")
                dialog.destroy()
                
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Earn Boon", command=earn_boon).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def player_spends_boon_dialog(self):
        if not self.player_boons:
            return
            
        dialog = tk.Toplevel(self.parent)
        dialog.title("Player Spends Boon")
        dialog.geometry("300x200")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select Player:").pack(pady=10)
        
        player_var = tk.StringVar()
        player_combo = ttk.Combobox(dialog, textvariable=player_var,
                                  values=[p for p, b in self.player_boons.items() if b > 0],
                                  state="readonly")
        player_combo.pack(pady=5)
        available_players = [p for p, b in self.player_boons.items() if b > 0]
        if available_players:
            player_combo.set(available_players[0])
            
        ttk.Label(dialog, text="Purpose:").pack(pady=(10,5))
        purpose_var = tk.StringVar()
        purpose_combo = ttk.Combobox(dialog, textvariable=purpose_var,
                                   values=["Re-roll Die", "Asset Activation", "Other"],
                                   state="readonly")
        purpose_combo.pack(pady=5)
        purpose_combo.set("Re-roll Die")
        
        def spend_boon():
            player = player_var.get()
            purpose = purpose_var.get()
            if player and player in self.player_boons and self.player_boons[player] > 0:
                self.spend_player_boon(player)
                self.log_transaction("Spend", player, 1, f"Spent for: {purpose}")
                dialog.destroy()
                
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Spend Boon", command=spend_boon).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def convert_boons_dialog(self):
        available_players = [p for p, b in self.player_boons.items() if b >= 2]
        if not available_players:
            return
            
        dialog = tk.Toplevel(self.parent)
        dialog.title("Convert Boons to XP")
        dialog.geometry("300x150")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select Player:").pack(pady=10)
        
        player_var = tk.StringVar()
        player_combo = ttk.Combobox(dialog, textvariable=player_var,
                                  values=available_players,
                                  state="readonly")
        player_combo.pack(pady=5)
        if available_players:
            player_combo.set(available_players[0])
            
        def convert_boons():
            player = player_var.get()
            if player and player in self.player_boons and self.player_boons[player] >= 2:
                self.convert_boons_to_xp(player)
                dialog.destroy()
                
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Convert 2 Boons → 1 XP", command=convert_boons).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def asset_activation_dialog(self):
        dialog = tk.Toplevel(self.parent)
        dialog.title("Asset Activation")
        dialog.geometry("350x200")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Asset Activation Cost:", font=("Arial", 10, "bold")).pack(pady=10)
        ttk.Label(dialog, text="1 Boon (preferred) or 2 XP (emergency)").pack()
        
        ttk.Label(dialog, text="Payment Method:").pack(pady=(15,5))
        payment_var = tk.StringVar(value="Boon")
        payment_frame = ttk.Frame(dialog)
        payment_frame.pack()
        ttk.Radiobutton(payment_frame, text="Use Boon", variable=payment_var, value="Boon").pack(side="left", padx=10)
        ttk.Radiobutton(payment_frame, text="Use 2 XP", variable=payment_var, value="XP").pack(side="left", padx=10)
        
        if payment_var.get() == "Boon":
            ttk.Label(dialog, text="Select Player:").pack(pady=(15,5))
            player_var = tk.StringVar()
            player_combo = ttk.Combobox(dialog, textvariable=player_var,
                                      values=[p for p, b in self.player_boons.items() if b > 0],
                                      state="readonly")
            player_combo.pack(pady=5)
            available_players = [p for p, b in self.player_boons.items() if b > 0]
            if available_players:
                player_combo.set(available_players[0])
                
        def activate_asset():
            payment = payment_var.get()
            if payment == "Boon":
                player = player_var.get()
                if player and player in self.player_boons and self.player_boons[player] > 0:
                    self.spend_player_boon(player)
                    self.log_transaction("Spend", player, 1, "Asset activation (boon)")
            else:  # XP
                # In a full implementation, this would connect to XP tracking
                self.log_transaction("Spend", "Party", 0, "Asset activation (2 XP)")
            dialog.destroy()
            
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Activate Asset", command=activate_asset).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def reroll_dialog(self):
        available_players = [p for p, b in self.player_boons.items() if b > 0]
        if not available_players:
            return
            
        dialog = tk.Toplevel(self.parent)
        dialog.title("Spend Boon for Re-roll")
        dialog.geometry("300x150")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select Player:").pack(pady=10)
        
        player_var = tk.StringVar()
        player_combo = ttk.Combobox(dialog, textvariable=player_var,
                                  values=available_players,
                                  state="readonly")
        player_combo.pack(pady=5)
        if available_players:
            player_combo.set(available_players[0])
            
        def spend_for_reroll():
            player = player_var.get()
            if player and player in self.player_boons and self.player_boons[player] > 0:
                self.spend_player_boon(player)
                self.log_transaction("Spend", player, 1, "Re-roll die")
                dialog.destroy()
                
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Spend Boon for Re-roll", command=spend_for_reroll).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def log_transaction(self, action, target, amount, description):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "action": action,
            "target": target,
            "amount": amount,
            "description": description
        }
        self.boon_log.append(log_entry)
        self.refresh_log_display()
        
    def clear_log(self):
        self.boon_log = []
        self.refresh_log_display()
        
    def update_summary(self):
        self.party_label.config(text=f"{self.party_boons}")
        total_player_boons = sum(self.player_boons.values())
        self.total_label.config(text=f"{total_player_boons}")
        
    def refresh_players_display(self):
        # Clear existing widgets
        for widget in self.players_display_frame.winfo_children():
            widget.destroy()
            
        if not self.player_boons:
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
        for player_name, boon_count in self.player_boons.items():
            player_frame = ttk.LabelFrame(scrollable_frame, text=player_name, padding="10")
            player_frame.pack(fill="x", pady=5, padx=5)
            
            # Boon count with visual indicator
            count_frame = ttk.Frame(player_frame)
            count_frame.pack(side="left")
            
            ttk.Label(count_frame, text="Boons:", font=("Arial", 9, "bold")).pack()
            boon_label = ttk.Label(count_frame, text=f"{boon_count}/5", 
                                 font=("Arial", 12, "bold"),
                                 foreground="gold" if boon_count > 0 else "gray")
            boon_label.pack()
            
            # Visual boon indicators
            visual_frame = ttk.Frame(player_frame)
            visual_frame.pack(side="left", padx=20)
            
            for i in range(5):
                color = "gold" if i < boon_count else "lightgray"
                canvas_indicator = tk.Canvas(visual_frame, width=20, height=20)
                canvas_indicator.pack(side="left", padx=2)
                canvas_indicator.create_oval(5, 5, 15, 15, fill=color, outline="black")
            
            # Player controls
            control_frame = ttk.Frame(player_frame)
            control_frame.pack(side="right")
            
            ttk.Button(control_frame, text="+", width=3,
                      command=lambda p=player_name: self.add_player_boon(p)).pack(side="left", padx=2)
            ttk.Button(control_frame, text="-", width=3,
                      command=lambda p=player_name: self.spend_player_boon(p)).pack(side="left", padx=2)
            ttk.Button(control_frame, text="Convert", 
                      command=lambda p=player_name: self.convert_boons_to_xp(p)).pack(side="left", padx=5)
            ttk.Button(control_frame, text="Remove", 
                      command=lambda p=player_name: self.remove_player(p)).pack(side="left", padx=5)
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def refresh_log_display(self):
        # Clear existing widgets
        for widget in self.log_display_frame.winfo_children():
            widget.destroy()
            
        if not self.boon_log:
            ttk.Label(self.log_display_frame, text="No boon transactions logged").pack(pady=20)
            return
            
        # Create scrollable area
        canvas = tk.Canvas(self.log_display_frame)
        scrollbar = ttk.Scrollbar(self.log_display_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display log entries (most recent first)
        for entry in reversed(self.boon_log[-30:]):  # Show last 30 entries
            entry_frame = ttk.Frame(scrollable_frame)
            entry_frame.pack(fill="x", pady=2, padx=5)
            
            # Timestamp
            ttk.Label(entry_frame, text=entry["timestamp"], width=10).pack(side="left", padx=5)
            
            # Action
            action_color = "green" if entry["action"] in ["Add", "Earn"] else \
                          "blue" if entry["action"] == "Convert" else "red"
            ttk.Label(entry_frame, text=entry["action"], foreground=action_color, width=10).pack(side="left", padx=5)
            
            # Target
            ttk.Label(entry_frame, text=entry["target"], width=15).pack(side="left", padx=5)
            
            # Amount
            if entry["amount"] > 0:
                ttk.Label(entry_frame, text=f"{entry['amount']}", width=5).pack(side="left", padx=5)
            
            # Description
            ttk.Label(entry_frame, text=entry["description"], wraplength=300).pack(side="left", padx=5, fill="x", expand=True)
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def remove_player(self, player_name):
        if player_name in self.player_boons:
            del self.player_boons[player_name]
            self.refresh_players_display()
            self.update_summary()
