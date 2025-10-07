# ui/cp_spend_tab.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class (SB)SpendTab:
    def __init__(self, parent):
        self.parent = parent
        self.available_cp = 0
        self.banked_cp = 0
        self.cp_log = []  # List of (SB) transactions
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Complication Point Tracker", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # (SB) Summary Frame
        summary_frame = ttk.LabelFrame(self.parent, text="(SB) Summary", padding="15")
        summary_frame.pack(fill="x", padx=20, pady=10)
        
        # Available (SB)
        avail_frame = ttk.Frame(summary_frame)
        avail_frame.pack(side="left", padx=20)
        ttk.Label(avail_frame, text="Available (SB):", font=("Arial", 12, "bold")).pack()
        self.avail_label = ttk.Label(avail_frame, text=f"{self.available_cp}", 
                                   font=("Arial", 16, "bold"), foreground="red")
        self.avail_label.pack()
        
        # Banked (SB)
        bank_frame = ttk.Frame(summary_frame)
        bank_frame.pack(side="left", padx=20)
        ttk.Label(bank_frame, text="Banked (SB):", font=("Arial", 12, "bold")).pack()
        self.bank_label = ttk.Label(bank_frame, text=f"{self.banked_cp}", 
                                  font=("Arial", 16, "bold"), foreground="blue")
        self.bank_label.pack()
        
        # Total (SB)
        total_frame = ttk.Frame(summary_frame)
        total_frame.pack(side="left", padx=20)
        ttk.Label(total_frame, text="Total (SB):", font=("Arial", 12, "bold")).pack()
        self.total_label = ttk.Label(total_frame, text=f"{self.available_cp + self.banked_cp}", 
                                   font=("Arial", 16, "bold"))
        self.total_label.pack()
        
        # Control Buttons
        control_frame = ttk.Frame(summary_frame)
        control_frame.pack(side="right")
        ttk.Button(control_frame, text="Add (SB)", command=self.add_cp_dialog).pack(pady=2)
        ttk.Button(control_frame, text="Reset All", command=self.reset_cp).pack(pady=2)
        
        # (SB) Actions Frame
        actions_frame = ttk.LabelFrame(self.parent, text="(SB) Actions", padding="15")
        actions_frame.pack(fill="x", padx=20, pady=10)
        
        # Spend (SB) Section
        spend_frame = ttk.LabelFrame(actions_frame, text="Spend (SB)", padding="10")
        spend_frame.pack(side="left", fill="y", padx=10)
        
        ttk.Label(spend_frame, text="(SB) Amount:").pack()
        self.spend_amount = ttk.Spinbox(spend_frame, from_=1, to=10, width=5)
        self.spend_amount.pack(pady=5)
        self.spend_amount.set("1")
        
        ttk.Label(spend_frame, text="Purpose:").pack()
        self.purpose_var = tk.StringVar()
        purpose_combo = ttk.Combobox(spend_frame, textvariable=self.purpose_var, 
                                   values=["Noise/Trace", "Alarm", "Exhaustion", "Exposure", 
                                          "Collateral", "Reinforcements", "Gear Break", 
                                          "Split Party", "Major Twist", "Custom"],
                                   width=15, state="readonly")
        purpose_combo.pack(pady=5)
        purpose_combo.set("Noise/Trace")
        
        ttk.Label(spend_frame, text="Custom Description:").pack()
        self.custom_desc = ttk.Entry(spend_frame, width=20)
        self.custom_desc.pack(pady=5)
        
        ttk.Button(spend_frame, text="Spend (SB)", command=self.spend_cp).pack(pady=10)
        
        # Bank/Unbank Section
        bank_frame = ttk.LabelFrame(actions_frame, text="Bank Management", padding="10")
        bank_frame.pack(side="left", fill="y", padx=10)
        
        ttk.Button(bank_frame, text="Bank All (SB)", command=self.bank_all).pack(pady=5)
        ttk.Button(bank_frame, text="Unbank 1 (SB)", command=self.unbank_cp).pack(pady=5)
        ttk.Button(bank_frame, text="Spend Banked (SB)", command=self.spend_banked_dialog).pack(pady=5)
        
        # Quick Spend Buttons
        quick_frame = ttk.LabelFrame(actions_frame, text="Quick Spend (1 (SB) each)", padding="10")
        quick_frame.pack(side="left", fill="y", padx=10)
        
        quick_spends = [
            ("Noise/Trace", lambda: self.quick_spend("Noise/Trace")),
            ("Fatigue", lambda: self.quick_spend("Fatigue")),
            ("Tool Compromised", lambda: self.quick_spend("Tool Compromised")),
            ("Position Lost", lambda: self.quick_spend("Position Lost"))
        ]
        
        for label, command in quick_spends:
            ttk.Button(quick_frame, text=label, command=command).pack(pady=2)
        
        # (SB) Log Frame
        log_frame = ttk.LabelFrame(self.parent, text="(SB) Log", padding="10")
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Log Controls
        log_control_frame = ttk.Frame(log_frame)
        log_control_frame.pack(fill="x", pady=5)
        
        ttk.Button(log_control_frame, text="Clear Log", command=self.clear_log).pack(side="right")
        
        # Log Display
        self.log_display_frame = ttk.Frame(log_frame)
        self.log_display_frame.pack(fill="both", expand=True)
        
        self.refresh_log_display()
        
        # (SB) Info Frame
        info_frame = ttk.LabelFrame(self.parent, text="(SB) Spend Menu", padding="10")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
(SB) Spend Options (Default Costs):
1 (SB): Noise, trace, +1 Supply segment, tool Compromised, time passes, bystander notices
2 (SB): Alarmed attention, lose position/cover, add lesser foe, advance Threat clock, Fatigue 1
3 (SB): Reinforcements, Out of Supply, gear breaks, split party options, escalate faction clock
4+ (SB): Major turns - trap springs, rival claims prize, authority arrives, scene-defining twists

Combat (SB):
1 (SB): Lose footing (next defense -1d)
2 (SB): Weapon Compromised
3 (SB): Pinned, disarmed, separated, battlefield shifts

Stealth (SB):
1 (SB): Footstep/squeak, shadow seen
2 (SB): Patrol path changes, lock resists
3 (SB): Partial alarm initiated

Social (SB):
1 (SB): Rumor cost, faux pas (-1d with this character)
2 (SB): Concession required (gift, favor)
3 (SB): Rival interjects with leverage

Travel (SB):
1 (SB): Lose time, minor injury, weather turns
2 (SB): +1 Supply segment, mount lamed
3 (SB): Wrong valley, Fatigue 1 to all

Arcana (SB):
1 (SB): Backlash prickle, sensory bleed
2 (SB): Unintended side-effect
3 (SB): Residue anchors foe/hex
        """.strip()
        
        # Create scrollable text widget for (SB) info
        info_text_frame = ttk.Frame(info_frame)
        info_text_frame.pack(fill="both", expand=True)
        
        info_canvas = tk.Canvas(info_text_frame)
        info_scrollbar = ttk.Scrollbar(info_text_frame, orient="vertical", command=info_canvas.yview)
        info_text_content = ttk.Frame(info_canvas)
        
        info_text_content.bind(
            "<Configure>",
            lambda e: info_canvas.configure(scrollregion=info_canvas.bbox("all"))
        )
        
        info_canvas.create_window((0, 0), window=info_text_content, anchor="nw")
        info_canvas.configure(yscrollcommand=info_scrollbar.set)
        
        info_label = ttk.Label(info_text_content, text=info_text, justify="left")
        info_label.pack()
        
        info_canvas.pack(side="left", fill="both", expand=True)
        info_scrollbar.pack(side="right", fill="y")
        
    def add_cp_dialog(self):
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add (SB)")
        dialog.geometry("300x150")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Add (SB) to:").pack(pady=10)
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack()
        
        ttk.Button(btn_frame, text="Available (SB)", 
                  command=lambda: [self.add_cp("available"), dialog.destroy()]).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Banked (SB)", 
                  command=lambda: [self.add_cp("banked"), dialog.destroy()]).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Both", 
                  command=lambda: [self.add_cp("both"), dialog.destroy()]).pack(side="left", padx=5)
                  
    def add_cp(self, target):
        if target in ["available", "both"]:
            self.available_cp += 1
        if target in ["banked", "both"]:
            self.banked_cp += 1
        self.update_display()
        
    def spend_cp(self):
        try:
            amount = int(self.spend_amount.get())
            if amount <= 0:
                return
                
            if amount <= self.available_cp:
                self.available_cp -= amount
                
                # Determine purpose
                purpose = self.purpose_var.get()
                if purpose == "Custom" or not purpose:
                    description = self.custom_desc.get().strip() or "Custom spend"
                else:
                    description = purpose
                    
                # Log the transaction
                self.log_transaction("Spend", amount, description)
                self.update_display()
                
                # Clear custom description
                self.custom_desc.delete(0, tk.END)
            else:
                # Not enough available (SB), try to use banked
                if amount <= (self.available_cp + self.banked_cp):
                    # Use available first
                    to_spend_avail = min(amount, self.available_cp)
                    to_spend_banked = amount - to_spend_avail
                    
                    if to_spend_avail > 0:
                        self.available_cp -= to_spend_avail
                        self.log_transaction("Spend", to_spend_avail, f"{self.purpose_var.get()} (Available)")
                        
                    if to_spend_banked > 0:
                        self.banked_cp -= to_spend_banked
                        self.log_transaction("Spend", to_spend_banked, f"{self.purpose_var.get()} (Banked)")
                        
                    self.update_display()
                    self.custom_desc.delete(0, tk.END)
        except ValueError:
            pass  # Invalid amount
            
    def quick_spend(self, purpose):
        if self.available_cp >= 1:
            self.available_cp -= 1
            self.log_transaction("Spend", 1, purpose)
            self.update_display()
            
    def bank_all(self):
        if self.available_cp > 0:
            amount = self.available_cp
            self.banked_cp += amount
            self.available_cp = 0
            self.log_transaction("Bank", amount, "Bank all available (SB)")
            self.update_display()
            
    def unbank_cp(self):
        if self.banked_cp >= 1:
            self.banked_cp -= 1
            self.available_cp += 1
            self.log_transaction("Unbank", 1, "Unbank 1 (SB)")
            self.update_display()
            
    def spend_banked_dialog(self):
        if self.banked_cp >= 1:
            dialog = tk.Toplevel(self.parent)
            dialog.title("Spend Banked (SB)")
            dialog.geometry("250x120")
            dialog.transient(self.parent)
            dialog.grab_set()
            
            ttk.Label(dialog, text=f"Banked (SB): {self.banked_cp}").pack(pady=10)
            
            amount_frame = ttk.Frame(dialog)
            amount_frame.pack()
            ttk.Label(amount_frame, text="Amount:").pack(side="left")
            amount_spin = ttk.Spinbox(amount_frame, from_=1, to=min(10, self.banked_cp), width=5)
            amount_spin.pack(side="left", padx=5)
            amount_spin.set("1")
            
            btn_frame = ttk.Frame(dialog)
            btn_frame.pack(pady=10)
            
            def spend_banked():
                try:
                    amount = int(amount_spin.get())
                    if 1 <= amount <= self.banked_cp:
                        self.banked_cp -= amount
                        self.log_transaction("Spend", amount, f"Spend banked (SB)")
                        self.update_display()
                except ValueError:
                    pass
                dialog.destroy()
                
            ttk.Button(btn_frame, text="Spend", command=spend_banked).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
            
    def reset_cp(self):
        self.available_cp = 0
        self.banked_cp = 0
        self.update_display()
        
    def clear_log(self):
        self.cp_log = []
        self.refresh_log_display()
        
    def log_transaction(self, action, amount, description):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "action": action,
            "amount": amount,
            "description": description
        }
        self.cp_log.append(log_entry)
        self.refresh_log_display()
        
    def update_display(self):
        self.avail_label.config(text=f"{self.available_cp}")
        self.bank_label.config(text=f"{self.banked_cp}")
        self.total_label.config(text=f"{self.available_cp + self.banked_cp}")
        
    def refresh_log_display(self):
        # Clear existing widgets
        for widget in self.log_display_frame.winfo_children():
            widget.destroy()
            
        if not self.cp_log:
            ttk.Label(self.log_display_frame, text="No (SB) transactions logged").pack(pady=20)
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
        for entry in reversed(self.cp_log[-50:]):  # Show last 50 entries
            entry_frame = ttk.Frame(scrollable_frame)
            entry_frame.pack(fill="x", pady=2, padx=5)
            
            # Timestamp
            ttk.Label(entry_frame, text=entry["timestamp"], width=10).pack(side="left", padx=5)
            
            # Action
            action_color = "red" if entry["action"] == "Spend" else "blue" if entry["action"] == "Bank" else "green"
            ttk.Label(entry_frame, text=entry["action"], foreground=action_color, width=10).pack(side="left", padx=5)
            
            # Amount
            ttk.Label(entry_frame, text=f"{entry['amount']}", width=5).pack(side="left", padx=5)
            
            # Description
            ttk.Label(entry_frame, text=entry["description"], wraplength=400).pack(side="left", padx=5, fill="x", expand=True)
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
