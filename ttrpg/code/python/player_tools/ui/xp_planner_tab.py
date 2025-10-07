# player_tools/ui/xp_planner_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class XPPlannerTab:
    def __init__(self, parent, character_data):
        self.parent = parent
        self.character_data = character_data
        self.frame = ttk.Frame(parent)
        
        # XP Tracking
        self.xp_frame = ttk.LabelFrame(self.frame, text="XP Tracking", padding="10")
        self.xp_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.xp_frame, text="Current XP:").grid(row=0, column=0, sticky=tk.W)
        self.current_xp_var = tk.StringVar(value="0")
        self.current_xp_entry = ttk.Entry(self.xp_frame, textvariable=self.current_xp_var, width=10)
        self.current_xp_entry.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(self.xp_frame, text="Total Earned XP:").grid(row=1, column=0, sticky=tk.W)
        self.total_xp_var = tk.StringVar(value="0")
        self.total_xp_entry = ttk.Entry(self.xp_frame, textvariable=self.total_xp_var, width=10)
        self.total_xp_entry.grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        # Planning Section
        self.plan_frame = ttk.LabelFrame(self.frame, text="Advancement Planning", padding="10")
        self.plan_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Enhancement Options
        ttk.Label(self.plan_frame, text="Enhance Self:").grid(row=0, column=0, sticky=tk.W)
        self.enhance_var = tk.StringVar()
        self.enhance_combo = ttk.Combobox(self.plan_frame, textvariable=self.enhance_var, 
                                          values=["Attribute", "Skill", "Talent"], width=15)
        self.enhance_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        self.enhance_combo.bind("<<ComboboxSelected>>", self._on_enhance_type_selected)
        
        self.enhance_details_frame = ttk.Frame(self.plan_frame)
        self.enhance_details_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Assets Options
        ttk.Label(self.plan_frame, text="Acquire Assets:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        self.asset_var = tk.StringVar()
        self.asset_combo = ttk.Combobox(self.plan_frame, textvariable=self.asset_var, 
                                       values=["On-Screen Follower", "Off-Screen Asset"], width=15)
        self.asset_combo.grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=(10, 0))
        self.asset_combo.bind("<<ComboboxSelected>>", self._on_asset_type_selected)
        
        self.asset_details_frame = ttk.Frame(self.plan_frame)
        self.asset_details_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Follower Initiative Actions (New Section)
        self.initiative_frame = ttk.LabelFrame(self.frame, text="Follower Initiative Actions", padding="10")
        self.initiative_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.initiative_frame, text="Follower:").grid(row=0, column=0, sticky=tk.W)
        self.follower_var = tk.StringVar()
        self.follower_combo = ttk.Combobox(self.initiative_frame, textvariable=self.follower_var, 
                                          values=["Select Follower"], width=15)
        self.follower_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(self.initiative_frame, text="Action:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.action_var = tk.StringVar()
        self.action_combo = ttk.Combobox(self.initiative_frame, textvariable=self.action_var,
                                        values=["Scout & Signal", "Distract & Draw", "Fetch & Carry"], width=15)
        self.action_combo.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        self.initiative_info = tk.Text(self.initiative_frame, height=4, width=50)
        self.initiative_info.grid(row=2, column=0, columnspan=2, pady=(5, 0))
        self.initiative_info.insert(1.0, "Select a follower and action to see details...")
        self.initiative_info.config(state=tk.DISABLED)
        
        self.follower_combo.bind("<<ComboboxSelected>>", self._on_follower_selected)
        self.action_combo.bind("<<ComboboxSelected>>", self._on_action_selected)
        
        # Plan Summary
        self.summary_frame = ttk.LabelFrame(self.frame, text="Plan Summary", padding="10")
        self.summary_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.summary_text = tk.Text(self.summary_frame, height=8, width=50)
        self.summary_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(self.summary_frame, orient=tk.VERTICAL, command=self.summary_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.summary_text.configure(yscrollcommand=scrollbar.set)
        
        # Action Buttons
        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        self.calculate_btn = ttk.Button(self.button_frame, text="Calculate Costs", command=self._calculate_costs)
        self.calculate_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.save_btn = ttk.Button(self.button_frame, text="Save Plan", command=self._save_plan)
        self.save_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.load_btn = ttk.Button(self.button_frame, text="Load Plan", command=self._load_plan)
        self.load_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Initialize detail frames
        self._init_enhance_details()
        self._init_asset_details()
        
    def _init_enhance_details(self):
        # Attribute enhancement
        self.attr_frame = ttk.Frame(self.enhance_details_frame)
        ttk.Label(self.attr_frame, text="Attribute:").grid(row=0, column=0, sticky=tk.W)
        self.attr_var = tk.StringVar()
        self.attr_combo = ttk.Combobox(self.attr_frame, textvariable=self.attr_var,
                                      values=["Body", "Wits", "Spirit", "Presence"], width=10)
        self.attr_combo.grid(row=0, column=1, padx=(5, 0))
        
        ttk.Label(self.attr_frame, text="New Rating:").grid(row=1, column=0, sticky=tk.W)
        self.attr_new_var = tk.StringVar()
        self.attr_new_entry = ttk.Entry(self.attr_frame, textvariable=self.attr_new_var, width=5)
        self.attr_new_entry.grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        # Skill enhancement
        self.skill_frame = ttk.Frame(self.enhance_details_frame)
        ttk.Label(self.skill_frame, text="Skill:").grid(row=0, column=0, sticky=tk.W)
        self.skill_var = tk.StringVar()
        self.skill_combo = ttk.Combobox(self.skill_frame, textvariable=self.skill_var,
                                       values=["Melee", "Ranged", "Athletics", "Arcana", 
                                              "Diplomacy", "Stealth", "Deception", "Survival",
                                              "Command", "Craft", "Performance", "Lore"], width=10)
        self.skill_combo.grid(row=0, column=1, padx=(5, 0))
        
        ttk.Label(self.skill_frame, text="New Level:").grid(row=1, column=0, sticky=tk.W)
        self.skill_new_var = tk.StringVar()
        self.skill_new_entry = ttk.Entry(self.skill_frame, textvariable=self.skill_new_var, width=5)
        self.skill_new_entry.grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        # Talent enhancement
        self.talent_frame = ttk.Frame(self.enhance_details_frame)
        ttk.Label(self.talent_frame, text="Talent:").grid(row=0, column=0, sticky=tk.W)
        self.talent_var = tk.StringVar()
        self.talent_combo = ttk.Combobox(self.talent_frame, textvariable=self.talent_var,
                                        values=["Battle Instincts", "Silver Tongue", "Iron Stomach",
                                               "Stone-Sense", "Backlash Soothing", "Blood Memory",
                                               "Familiar Bond", "Echo-Walker", "Warglord", "Spirit-Shield"], width=15)
        self.talent_combo.grid(row=0, column=1, padx=(5, 0))
        
    def _init_asset_details(self):
        # Follower details
        self.follower_asset_frame = ttk.Frame(self.asset_details_frame)
        ttk.Label(self.follower_asset_frame, text="Follower Name:").grid(row=0, column=0, sticky=tk.W)
        self.follower_name_var = tk.StringVar()
        self.follower_name_entry = ttk.Entry(self.follower_asset_frame, textvariable=self.follower_name_var, width=15)
        self.follower_name_entry.grid(row=0, column=1, padx=(5, 0))
        
        ttk.Label(self.follower_asset_frame, text="Role:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.follower_role_var = tk.StringVar()
        self.follower_role_combo = ttk.Combobox(self.follower_asset_frame, textvariable=self.follower_role_var,
                                               values=["Scout", "Mimic", "Distract", "Fetch", "Sentry", 
                                                      "Bodyguard", "Archivist"], width=10)
        self.follower_role_combo.grid(row=1, column=1, padx=(5, 0), pady=(5, 0))
        
        ttk.Label(self.follower_asset_frame, text="Cap:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.follower_cap_var = tk.StringVar()
        self.follower_cap_entry = ttk.Entry(self.follower_asset_frame, textvariable=self.follower_cap_var, width=5)
        self.follower_cap_entry.grid(row=2, column=1, padx=(5, 0), pady=(5, 0))
        
        # Asset details
        self.asset_frame = ttk.Frame(self.asset_details_frame)
        ttk.Label(self.asset_frame, text="Asset Name:").grid(row=0, column=0, sticky=tk.W)
        self.asset_name_var = tk.StringVar()
        self.asset_name_entry = ttk.Entry(self.asset_frame, textvariable=self.asset_name_var, width=15)
        self.asset_name_entry.grid(row=0, column=1, padx=(5, 0))
        
        ttk.Label(self.asset_frame, text="Tier:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.asset_tier_var = tk.StringVar()
        self.asset_tier_combo = ttk.Combobox(self.asset_frame, textvariable=self.asset_tier_var,
                                            values=["Minor", "Standard", "Major"], width=10)
        self.asset_tier_combo.grid(row=1, column=1, padx=(5, 0), pady=(5, 0))
        
    def _on_enhance_type_selected(self, event=None):
        # Clear previous selections
        for widget in self.enhance_details_frame.winfo_children():
            widget.grid_forget()
            
        # Show appropriate frame
        selection = self.enhance_var.get()
        if selection == "Attribute":
            self.attr_frame.grid(row=0, column=0, sticky=tk.W)
        elif selection == "Skill":
            self.skill_frame.grid(row=0, column=0, sticky=tk.W)
        elif selection == "Talent":
            self.talent_frame.grid(row=0, column=0, sticky=tk.W)
            
    def _on_asset_type_selected(self, event=None):
        # Clear previous selections
        for widget in self.asset_details_frame.winfo_children():
            widget.grid_forget()
            
        # Show appropriate frame
        selection = self.asset_var.get()
        if selection == "On-Screen Follower":
            self.follower_asset_frame.grid(row=0, column=0, sticky=tk.W)
        elif selection == "Off-Screen Asset":
            self.asset_frame.grid(row=0, column=0, sticky=tk.W)
            
    def _on_follower_selected(self, event=None):
        self._update_initiative_info()
        
    def _on_action_selected(self, event=None):
        self._update_initiative_info()
        
    def _update_initiative_info(self):
        follower = self.follower_var.get()
        action = self.action_var.get()
        
        if follower and action and follower != "Select Follower":
            # In a real implementation, this would get info from the follower object
            info_text = f"Follower: {follower}\n"
            info_text += f"Action: {action}\n\n"
            
            if action == "Scout & Signal":
                info_text += "Effect: Change ally's next action position to Controlled or grant +1 effect\n"
                info_text += "Cost: Mark Exposure +1 or Harm 1\n"
                info_text += "Pressure: GM may spend 1 (SB) to escalate"
            elif action == "Distract & Draw":
                info_text += "Effect: Reduce a kinetic rail (Hunt/Escape/Hazard) by -1 tick\n"
                info_text += "Cost: Mark Exposure +1 or Harm 1\n"
                info_text += "Pressure: GM may spend 1 (SB) to escalate"
            elif action == "Fetch & Carry":
                info_text += "Effect: Move small object; on recipient's next success, advance +1 tick on target clock\n"
                info_text += "Cost: Mark Exposure +1 or Harm 1\n"
                info_text += "Pressure: GM may spend 1 (SB) to escalate"
                
            self.initiative_info.config(state=tk.NORMAL)
            self.initiative_info.delete(1.0, tk.END)
            self.initiative_info.insert(1.0, info_text)
            self.initiative_info.config(state=tk.DISABLED)
        else:
            self.initiative_info.config(state=tk.NORMAL)
            self.initiative_info.delete(1.0, tk.END)
            self.initiative_info.insert(1.0, "Select a follower and action to see details...")
            self.initiative_info.config(state=tk.DISABLED)
            
    def _calculate_costs(self):
        try:
            current_xp = int(self.current_xp_var.get() or 0)
            total_earned = int(self.total_xp_var.get() or 0)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for XP values")
            return
        
        plan_details = []
        total_cost = 0
        
        # Calculate enhancement costs
        enhance_type = self.enhance_var.get()
        if enhance_type == "Attribute":
            attr = self.attr_var.get()
            try:
                new_rating = int(self.attr_new_var.get() or 0)
                if attr and new_rating > 0:
                    cost = new_rating * 3
                    total_cost += cost
                    plan_details.append(f"Enhance {attr} to {new_rating}: {cost} XP")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid number for attribute rating")
                
        elif enhance_type == "Skill":
            skill = self.skill_var.get()
            try:
                new_level = int(self.skill_new_var.get() or 0)
                if skill and new_level > 0:
                    cost = new_level * 2
                    total_cost += cost
                    plan_details.append(f"Enhance {skill} to {new_level}: {cost} XP")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid number for skill level")
                
        elif enhance_type == "Talent":
            talent = self.talent_var.get()
            if talent:
                # Talent costs based on the SRD examples
                talent_costs = {
                    "Battle Instincts": 4,
                    "Silver Tongue": 3,
                    "Iron Stomach": 3,
                    "Stone-Sense": 5,
                    "Backlash Soothing": 6,
                    "Blood Memory": 7,
                    "Familiar Bond": 9,
                    "Echo-Walker": 20,
                    "Warglord": 18,
                    "Spirit-Shield": 15
                }
                cost = talent_costs.get(talent, 5)  # Default cost
                total_cost += cost
                plan_details.append(f"Learn {talent}: {cost} XP")
                
        # Calculate asset costs
        asset_type = self.asset_var.get()
        if asset_type == "On-Screen Follower":
            follower_name = self.follower_name_var.get()
            follower_role = self.follower_role_var.get()
            try:
                cap = int(self.follower_cap_var.get() or 0)
                if follower_name and follower_role and cap > 0:
                    cost = cap * cap  # Cap^2 cost
                    total_cost += cost
                    plan_details.append(f"Acquire Follower '{follower_name}' (Cap {cap}): {cost} XP")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid number for follower cap")
                
        elif asset_type == "Off-Screen Asset":
            asset_name = self.asset_name_var.get()
            tier = self.asset_tier_var.get()
            if asset_name and tier:
                tier_costs = {"Minor": 4, "Standard": 8, "Major": 12}
                cost = tier_costs.get(tier, 0)
                total_cost += cost
                plan_details.append(f"Acquire Asset '{asset_name}' ({tier}): {cost} XP")
                
        # Update summary
        summary = f"Current XP: {current_xp}\n"
        summary += f"Total Earned XP: {total_earned}\n"
        summary += f"Planned Expenditure: {total_cost} XP\n"
        summary += f"Remaining XP: {current_xp - total_cost}\n\n"
        summary += "Plan Details:\n" + "\n".join(plan_details)
        
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(1.0, summary)
        
        # Check if plan is affordable
        if total_cost > current_xp:
            messagebox.showwarning("Insufficient XP", 
                                 f"Plan costs {total_cost} XP but you only have {current_xp} XP")
        elif total_cost == 0:
            messagebox.showinfo("No Plan", "No advancement options selected")
        else:
            messagebox.showinfo("Plan Calculated", f"Total cost: {total_cost} XP")
            
    def _save_plan(self):
        plan_data = {
            "current_xp": self.current_xp_var.get(),
            "total_xp": self.total_xp_var.get(),
            "enhance_type": self.enhance_var.get(),
            "attr": self.attr_var.get(),
            "attr_new": self.attr_new_var.get(),
            "skill": self.skill_var.get(),
            "skill_new": self.skill_new_var.get(),
            "talent": self.talent_var.get(),
            "asset_type": self.asset_var.get(),
            "follower_name": self.follower_name_var.get(),
            "follower_role": self.follower_role_var.get(),
            "follower_cap": self.follower_cap_var.get(),
            "asset_name": self.asset_name_var.get(),
            "asset_tier": self.asset_tier_var.get()
        }
        
        try:
            if not os.path.exists("plans"):
                os.makedirs("plans")
                
            filename = f"plans/xp_plan_{self.current_xp_var.get()}_xp.json"
            with open(filename, "w") as f:
                json.dump(plan_data, f, indent=2)
            messagebox.showinfo("Success", f"Plan saved successfully as {filename}!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save plan: {str(e)}")
            
    def _load_plan(self):
        try:
            # Look for plan files
            if not os.path.exists("plans"):
                os.makedirs("plans")
                
            plan_files = [f for f in os.listdir("plans") if f.endswith(".json")]
            if not plan_files:
                messagebox.showwarning("No Plans", "No saved plans found")
                return
                
            # For simplicity, load the first plan found
            with open(f"plans/{plan_files[0]}", "r") as f:
                plan_data = json.load(f)
                
            self.current_xp_var.set(plan_data.get("current_xp", "0"))
            self.total_xp_var.set(plan_data.get("total_xp", "0"))
            self.enhance_var.set(plan_data.get("enhance_type", ""))
            self.attr_var.set(plan_data.get("attr", ""))
            self.attr_new_var.set(plan_data.get("attr_new", ""))
            self.skill_var.set(plan_data.get("skill", ""))
            self.skill_new_var.set(plan_data.get("skill_new", ""))
            self.talent_var.set(plan_data.get("talent", ""))
            self.asset_var.set(plan_data.get("asset_type", ""))
            self.follower_name_var.set(plan_data.get("follower_name", ""))
            self.follower_role_var.set(plan_data.get("follower_role", ""))
            self.follower_cap_var.set(plan_data.get("follower_cap", ""))
            self.asset_name_var.set(plan_data.get("asset_name", ""))
            self.asset_tier_var.set(plan_data.get("asset_tier", ""))
            
            # Trigger UI updates
            self._on_enhance_type_selected()
            self._on_asset_type_selected()
            
            messagebox.showinfo("Success", f"Plan loaded successfully from {plan_files[0]}!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load plan: {str(e)}")
            
    def get_frame(self):
        return self.frame

