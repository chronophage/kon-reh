# player_tools/ui/character_builder_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.database.skill_db import SkillDatabase, SkillCategory

class CharacterBuilderTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.db = SkillDatabase()
        self.character_data = {
            "name": "",
            "attributes": {"Body": 2, "Wits": 2, "Spirit": 2, "Presence": 2},
            "skills": [],
            "talents": [],
            "assets": [],
            "xp_spent": 0,
            "xp_total": 30,
            "boons": 0,
            "complications": []
        }
        self.current_step = 0
        self.steps = [
            "Character Basics",
            "Attributes",
            "Skills",
            "Talents",
            "Assets",
            "Review & Finish"
        ]
        self.create_ui()
        
    def create_ui(self):
        # Header
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="Character Builder", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        # Progress indicator
        self.progress_var = tk.StringVar()
        self.progress_label = ttk.Label(header_frame, textvariable=self.progress_var, font=("Arial", 10))
        self.progress_label.pack(side=tk.RIGHT)
        
        # Main content notebook (no scrolling)
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create all step frames
        self.step_frames = []
        for i in range(len(self.steps)):
            frame = ttk.Frame(self.notebook)
            frame.pack(fill=tk.BOTH, expand=True)
            self.step_frames.append(frame)
            self.notebook.add(frame, text=self.steps[i])
            
        # Navigation buttons
        nav_frame = ttk.Frame(self.frame)
        nav_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.prev_button = ttk.Button(nav_frame, text="Previous", command=self.previous_step, state="disabled")
        self.prev_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.next_button = ttk.Button(nav_frame, text="Next", command=self.next_step)
        self.next_button.pack(side=tk.RIGHT)
        
        self.finish_button = ttk.Button(nav_frame, text="Finish & Save", command=self.finish_character, state="disabled")
        self.finish_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Show first step
        self.show_step_content(0)
        self.notebook.select(0)
        
    def show_step_content(self, step):
        """Populate content for a specific step"""
        frame = self.step_frames[step]
        
        # Clear existing content
        for widget in frame.winfo_children():
            widget.destroy()
            
        # Add content based on step
        if step == 0:
            self.populate_basics_step(frame)
        elif step == 1:
            self.populate_attributes_step(frame)
        elif step == 2:
            self.populate_skills_step(frame)
        elif step == 3:
            self.populate_talents_step(frame)
        elif step == 4:
            self.populate_assets_step(frame)
        elif step == 5:
            self.populate_review_step(frame)
            
    def populate_basics_step(self, frame):
        ttk.Label(frame, text="Character Basics", font=("Arial", 14, "bold")).pack(pady=(10, 20))
        
        # Character name
        name_frame = ttk.Frame(frame)
        name_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(name_frame, text="Character Name:").pack(anchor=tk.W)
        self.name_var = tk.StringVar(value=self.character_data["name"])
        ttk.Entry(name_frame, textvariable=self.name_var, width=30).pack(fill=tk.X, pady=(5, 0))
        
        # Starting XP
        xp_frame = ttk.LabelFrame(frame, text="Starting Resources", padding="10")
        xp_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(xp_frame, text=f"Starting XP: {self.character_data['xp_total']}").pack(anchor=tk.W)
        ttk.Label(xp_frame, text="Baseline 30 XP for new characters").pack(anchor=tk.W, pady=(5, 0))
        
        # Complication options
        comp_frame = ttk.LabelFrame(frame, text="Optional Starting Complications", padding="10")
        comp_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(comp_frame, text="Accept complications for extra XP:").pack(anchor=tk.W)
        
        self.complication_vars = {}
        complications = [
            ("Obligation Deficit", "Begin with up to 2 XP deficit (debt, unfinished business)"),
            ("Complication Trade", "Accept 1-2 Complications for +1 XP each")
        ]
        
        for i, (name, desc) in enumerate(complications):
            var = tk.BooleanVar()
            self.complication_vars[name] = var
            check = ttk.Checkbutton(comp_frame, text=f"{name}: {desc}", variable=var)
            check.pack(anchor=tk.W, pady=(5, 0))
            
    def populate_attributes_step(self, frame):
        ttk.Label(frame, text="Attributes", font=("Arial", 14, "bold")).pack(pady=(10, 20))
        
        # XP info
        xp_info = ttk.Frame(frame)
        xp_info.pack(fill=tk.X, padx=20, pady=(0, 20))
        ttk.Label(xp_info, text=f"XP Available: {self.character_data['xp_total'] - self.character_data['xp_spent']}", 
                 font=("Arial", 10, "bold")).pack(side=tk.RIGHT)
        
        # Attributes grid
        attr_frame = ttk.LabelFrame(frame, text="Attributes (Base 2, Max 5)", padding="10")
        attr_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.attr_vars = {}
        attributes = ["Body", "Wits", "Spirit", "Presence"]
        
        for i, attr in enumerate(attributes):
            row = ttk.Frame(attr_frame)
            row.pack(fill=tk.X, pady=5)
            
            ttk.Label(row, text=attr, width=10).pack(side=tk.LEFT)
            
            # Current value
            current_var = tk.StringVar(value=str(self.character_data["attributes"][attr]))
            self.attr_vars[attr] = current_var
            ttk.Label(row, textvariable=current_var, width=3, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(10, 0))
            
            # Buttons
            ttk.Button(row, text="-", width=3, command=lambda a=attr: self.decrease_attr(a)).pack(side=tk.LEFT, padx=(10, 0))
            ttk.Button(row, text="+", width=3, command=lambda a=attr: self.increase_attr(a)).pack(side=tk.LEFT, padx=(5, 0))
            
            # Cost info
            cost_label = ttk.Label(row, text=f"(Cost: {(int(current_var.get()) + 1) * 3} XP to raise)")
            cost_label.pack(side=tk.RIGHT)
            
        # Attribute descriptions
        desc_frame = ttk.Frame(frame)
        desc_frame.pack(fill=tk.X, padx=20, pady=10)
        
        descriptions = [
            ("Body", "Strength, endurance, and physical action"),
            ("Wits", "Perception, cleverness, and reaction speed"),
            ("Spirit", "Willpower, intuition, and resilience"),
            ("Presence", "Charm, command, and social force")
        ]
        
        for attr, desc in descriptions:
            ttk.Label(desc_frame, text=f"• {attr}: {desc}").pack(anchor=tk.W)
            
    def populate_skills_step(self, frame):
        ttk.Label(frame, text="Skills", font=("Arial", 14, "bold")).pack(pady=(10, 20))
        
        # XP info
        xp_info = ttk.Frame(frame)
        xp_info.pack(fill=tk.X, padx=20, pady=(0, 20))
        ttk.Label(xp_info, text=f"XP Available: {self.character_data['xp_total'] - self.character_data['xp_spent']}", 
                 font=("Arial", 10, "bold")).pack(side=tk.RIGHT)
        
        # Create canvas with scrollbar for skills
        canvas = tk.Canvas(frame, height=400)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y", padx=(0, 20))
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        
        # Skill categories
        categories = list(SkillCategory)
        self.skill_vars = {}
        
        for category in categories:
            cat_frame = ttk.LabelFrame(scrollable_frame, text=f"{category.value} Skills", padding="10")
            cat_frame.pack(fill=tk.X, pady=5, padx=5)
            
            # Get skills in this category
            try:
                skills = self.db.get_skills_by_category(category)
            except:
                skills = []  # Fallback if DB not available
                
            if not skills:
                ttk.Label(cat_frame, text="No skills available in this category").pack(pady=10)
                continue
                
            # Skill entries
            for skill in skills:
                skill_frame = ttk.Frame(cat_frame)
                skill_frame.pack(fill=tk.X, pady=5)
                
                # Skill info
                info_frame = ttk.Frame(skill_frame)
                info_frame.pack(fill=tk.X)
                
                ttk.Label(info_frame, text=skill.name, font=("Arial", 9, "bold"), width=20).pack(side=tk.LEFT)
                ttk.Label(info_frame, text=skill.description, wraplength=300).pack(side=tk.LEFT, padx=(10, 0))
                
                # Level selector
                level_frame = ttk.Frame(skill_frame)
                level_frame.pack(fill=tk.X, pady=(5, 0))
                
                ttk.Label(level_frame, text="Level:").pack(side=tk.LEFT)
                
                level_var = tk.StringVar(value="0")
                self.skill_vars[skill.name] = level_var
                
                level_combo = ttk.Combobox(level_frame, textvariable=level_var,
                                          values=["0", "1", "2", "3", "4", "5"], width=5)
                level_combo.pack(side=tk.LEFT, padx=(5, 10))
                
                # Cost info
                cost_label = ttk.Label(level_frame, text=f"Cost: {int(level_var.get()) * 2} XP")
                cost_label.pack(side=tk.LEFT)
                
                # Update cost when level changes
                def update_cost(lv, cl):
                    def callback(*args):
                        if lv.get().isdigit():
                            cl.config(text=f"Cost: {int(lv.get()) * 2} XP")
                    return callback
                
                level_var.trace('w', update_cost(level_var, cost_label))
                
    def populate_talents_step(self, frame):
        ttk.Label(frame, text="Talents", font=("Arial", 14, "bold")).pack(pady=(10, 20))
        
        # XP info
        xp_info = ttk.Frame(frame)
        xp_info.pack(fill=tk.X, padx=20, pady=(0, 20))
        ttk.Label(xp_info, text=f"XP Available: {self.character_data['xp_total'] - self.character_data['xp_spent']}", 
                 font=("Arial", 10, "bold")).pack(side=tk.RIGHT)
        
        # Note about prerequisites
        ttk.Label(frame, text="Note: Talent prerequisites are not automatically validated in this wizard", 
                 foreground="orange").pack(padx=20, pady=(0, 10))
        
        # Create canvas with scrollbar for talents
        canvas = tk.Canvas(frame, height=400)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y", padx=(0, 20))
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        
        from shared.database.skill_db import TalentType
        talent_types = list(TalentType)
        self.talent_vars = {}
        
        for talent_type in talent_types:
            type_frame = ttk.LabelFrame(scrollable_frame, text=f"{talent_type.value} Talents", padding="10")
            type_frame.pack(fill=tk.X, pady=5, padx=5)
            
            # Get talents of this type
            try:
                talents = [t for t in self.db.get_all_talents() if t.talent_type == talent_type]
            except:
                talents = []
                
            if not talents:
                ttk.Label(type_frame, text="No talents available in this category").pack(pady=10)
                continue
                
            # Talent entries
            for talent in talents:
                talent_frame = ttk.Frame(type_frame)
                talent_frame.pack(fill=tk.X, pady=5)
                
                # Talent info
                info_frame = ttk.Frame(talent_frame)
                info_frame.pack(fill=tk.X)
                
                ttk.Label(info_frame, text=talent.name, font=("Arial", 9, "bold"), width=20).pack(side=tk.LEFT)
                ttk.Label(info_frame, text=talent.description, wraplength=300).pack(side=tk.LEFT, padx=(10, 0))
                
                # Talent details
                details_frame = ttk.Frame(talent_frame)
                details_frame.pack(fill=tk.X, pady=(2, 5))
                
                ttk.Label(details_frame, text=f"Cost: {talent.cost} XP", font=("Arial", 8, "bold")).pack(side=tk.LEFT)
                if talent.culture:
                    ttk.Label(details_frame, text=f" | Culture: {talent.culture}", foreground="blue").pack(side=tk.LEFT)
                
                # Selection checkbox
                var = tk.BooleanVar()
                self.talent_vars[talent.name] = var
                ttk.Checkbutton(details_frame, text="Select", variable=var).pack(side=tk.RIGHT)
                
    def populate_assets_step(self, frame):
        ttk.Label(frame, text="Assets & Followers", font=("Arial", 14, "bold")).pack(pady=(10, 20))
        
        # XP info
        xp_info = ttk.Frame(frame)
        xp_info.pack(fill=tk.X, padx=20, pady=(0, 20))
        ttk.Label(xp_info, text=f"XP Available: {self.character_data['xp_total'] - self.character_data['xp_spent']}", 
                 font=("Arial", 10, "bold")).pack(side=tk.RIGHT)
        
        # Create notebook for asset types
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Off-Screen Assets tab
        assets_frame = ttk.Frame(notebook)
        assets_frame.pack(fill=tk.BOTH, expand=True)
        notebook.add(assets_frame, text="Off-Screen Assets")
        
        # Create scrollable area for assets
        assets_canvas = tk.Canvas(assets_frame, height=300)
        assets_scrollbar = ttk.Scrollbar(assets_frame, orient="vertical", command=assets_canvas.yview)
        assets_scrollable = ttk.Frame(assets_canvas)
        
        assets_scrollable.bind(
            "<Configure>",
            lambda e: assets_canvas.configure(scrollregion=assets_canvas.bbox("all"))
        )
        
        assets_canvas.create_window((0, 0), window=assets_scrollable, anchor="nw")
        assets_canvas.configure(yscrollcommand=assets_scrollbar.set)
        
        assets_canvas.pack(side="left", fill="both", expand=True)
        assets_scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_assets_mousewheel(event):
            assets_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        assets_canvas.bind("<MouseWheel>", _on_assets_mousewheel)
        assets_scrollable.bind("<MouseWheel>", _on_assets_mousewheel)
        
        ttk.Label(assets_scrollable, text="Off-Screen Assets (Background Resources)", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        assets = [
            ("Minor (4 XP)", "Safehouse, small shop charter, parish patron"),
            ("Standard (8 XP)", "Noble title, guild section, spy ring, estated farm"),
            ("Major (12 XP)", "City license/monopoly, regional network, fortress lease")
        ]
        
        self.asset_vars = {}
        
        for name, desc in assets:
            asset_frame = ttk.LabelFrame(assets_scrollable, text=name, padding="10")
            asset_frame.pack(fill=tk.X, pady=5, padx=5)
            
            ttk.Label(asset_frame, text=desc).pack(anchor=tk.W)
            
            var = tk.BooleanVar()
            self.asset_vars[name] = var
            ttk.Checkbutton(asset_frame, text="Select this asset", variable=var).pack(anchor=tk.W, pady=(10, 0))
            
        # On-Screen Followers tab
        followers_frame = ttk.Frame(notebook)
        followers_frame.pack(fill=tk.BOTH, expand=True)
        notebook.add(followers_frame, text="On-Screen Followers")
        
        # Create scrollable area for followers
        followers_canvas = tk.Canvas(followers_frame, height=300)
        followers_scrollbar = ttk.Scrollbar(followers_frame, orient="vertical", command=followers_canvas.yview)
        followers_scrollable = ttk.Frame(followers_canvas)
        
        followers_scrollable.bind(
            "<Configure>",
            lambda e: followers_canvas.configure(scrollregion=followers_canvas.bbox("all"))
        )
        
        followers_canvas.create_window((0, 0), window=followers_scrollable, anchor="nw")
        followers_canvas.configure(yscrollcommand=followers_scrollbar.set)
        
        followers_canvas.pack(side="left", fill="both", expand=True)
        followers_scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_followers_mousewheel(event):
            followers_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        followers_canvas.bind("<MouseWheel>", _on_followers_mousewheel)
        followers_scrollable.bind("<MouseWheel>", _on_followers_mousewheel)
        
        ttk.Label(followers_scrollable, text="On-Screen Followers (Active Helpers)", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        followers = [
            ("Cap 1 (3 XP)", "Competent assistant (e.g., Porter, Squire)"),
            ("Cap 2 (5 XP)", "Trained specialist (e.g., Scout, Bodyguard)"),
            ("Cap 3 (8 XP)", "Veteran operative (e.g., Spymaster's Agent)"),
            ("Cap 4 (12 XP)", "Elite aide (e.g., Master-at-Arms)"),
            ("Cap 5 (17 XP)", "Exceptional lieutenant (rare)")
        ]
        
        self.follower_vars = {}
        
        for name, desc in followers:
            follower_frame = ttk.LabelFrame(followers_scrollable, text=name, padding="10")
            follower_frame.pack(fill=tk.X, pady=5, padx=5)
            
            ttk.Label(follower_frame, text=desc).pack(anchor=tk.W)
            
            var = tk.BooleanVar()
            self.follower_vars[name] = var
            ttk.Checkbutton(follower_frame, text="Select this follower", variable=var).pack(anchor=tk.W, pady=(10, 0))
            
    def populate_review_step(self, frame):
        ttk.Label(frame, text="Character Review", font=("Arial", 14, "bold")).pack(pady=(10, 20))
        
        # Character name
        if hasattr(self, 'name_var'):
            self.character_data["name"] = self.name_var.get()
            
        ttk.Label(frame, text=f"Character: {self.character_data['name'] or 'Unnamed Character'}", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 20))
        
        # Summary info
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(info_frame, text=f"Total XP: {self.character_data['xp_total']}").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(info_frame, text=f"XP Spent: {self.character_data['xp_spent']}", foreground="red").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(info_frame, text=f"XP Remaining: {self.character_data['xp_total'] - self.character_data['xp_spent']}", 
                 foreground="green" if self.character_data['xp_total'] >= self.character_data['xp_spent'] else "red").pack(side=tk.LEFT)
        
        # Create scrollable area for review content
        canvas = tk.Canvas(frame, height=400)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        
        # Attributes summary
        attr_frame = ttk.LabelFrame(scrollable_frame, text="Attributes", padding="10")
        attr_frame.pack(fill=tk.X, pady=5, padx=5)
        
        attr_row = ttk.Frame(attr_frame)
        attr_row.pack(fill=tk.X)
        for attr, value in self.character_data["attributes"].items():
            ttk.Label(attr_row, text=f"{attr}: {value}", width=12).pack(side=tk.LEFT)
            
        # Skills summary
        skills_frame = ttk.LabelFrame(scrollable_frame, text="Skills", padding="10")
        skills_frame.pack(fill=tk.X, pady=5, padx=5)
        
        if hasattr(self, 'skill_vars') and self.skill_vars:
            selected_skills = [(name, var.get()) for name, var in self.skill_vars.items() if var.get() != "0"]
            if selected_skills:
                for name, level in selected_skills:
                    ttk.Label(skills_frame, text=f"{name}: {level}").pack(anchor=tk.W)
            else:
                ttk.Label(skills_frame, text="No skills selected").pack(anchor=tk.W)
        else:
            ttk.Label(skills_frame, text="No skills selected").pack(anchor=tk.W)
            
        # Talents summary
        talents_frame = ttk.LabelFrame(scrollable_frame, text="Talents", padding="10")
        talents_frame.pack(fill=tk.X, pady=5, padx=5)
        
        if hasattr(self, 'talent_vars') and self.talent_vars:
            selected_talents = [name for name, var in self.talent_vars.items() if var.get()]
            if selected_talents:
                for name in selected_talents:
                    ttk.Label(talents_frame, text=name).pack(anchor=tk.W)
            else:
                ttk.Label(talents_frame, text="No talents selected").pack(anchor=tk.W)
        else:
            ttk.Label(talents_frame, text="No talents selected").pack(anchor=tk.W)
            
        # Assets/Followers summary
        assets_frame = ttk.LabelFrame(scrollable_frame, text="Assets & Followers", padding="10")
        assets_frame.pack(fill=tk.X, pady=5, padx=5)
        
        if hasattr(self, 'asset_vars') and self.asset_vars:
            selected_assets = [name for name, var in self.asset_vars.items() if var.get()]
            if selected_assets:
                for name in selected_assets:
                    ttk.Label(assets_frame, text=f"Asset: {name}").pack(anchor=tk.W)
            else:
                ttk.Label(assets_frame, text="No assets selected").pack(anchor=tk.W)
                
        if hasattr(self, 'follower_vars') and self.follower_vars:
            selected_followers = [name for name, var in self.follower_vars.items() if var.get()]
            if selected_followers:
                for name in selected_followers:
                    ttk.Label(assets_frame, text=f"Follower: {name}").pack(anchor=tk.W)
            else:
                ttk.Label(assets_frame, text="No followers selected").pack(anchor=tk.W)
                
        if not (hasattr(self, 'asset_vars') and hasattr(self, 'follower_vars')):
            ttk.Label(assets_frame, text="No assets or followers selected").pack(anchor=tk.W)
            
    def increase_attr(self, attr):
        current_value = int(self.attr_vars[attr].get())
        if current_value < 5:
            cost = (current_value + 1) * 3
            available_xp = self.character_data['xp_total'] - self.character_data['xp_spent']
            if cost <= available_xp:
                self.attr_vars[attr].set(str(current_value + 1))
                self.character_data["attributes"][attr] = current_value + 1
                # In a full implementation, you'd track XP spending
            else:
                messagebox.showwarning("Insufficient XP", f"Not enough XP to raise {attr}")
                
    def decrease_attr(self, attr):
        current_value = int(self.attr_vars[attr].get())
        if current_value > 2:  # Base value
            self.attr_vars[attr].set(str(current_value - 1))
            self.character_data["attributes"][attr] = current_value - 1
            # In a full implementation, you'd refund XP
            
    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.notebook.select(self.current_step)
            self.update_navigation_buttons()
            
    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            # Validate current step before proceeding
            if self.validate_current_step():
                self.current_step += 1
                self.notebook.select(self.current_step)
                self.update_navigation_buttons()
            else:
                messagebox.showwarning("Validation Error", "Please complete the required fields in this step")
                
    def update_navigation_buttons(self):
        """Update navigation button states"""
        self.prev_button.config(state="normal" if self.current_step > 0 else "disabled")
        self.next_button.config(state="normal" if self.current_step < len(self.steps) - 1 else "disabled")
        self.finish_button.config(state="normal" if self.current_step == len(self.steps) - 1 else "disabled")
        self.progress_var.set(f"Step {self.current_step + 1} of {len(self.steps)}: {self.steps[self.current_step]}")
                
    def validate_current_step(self):
        # Basic validation for each step
        if self.current_step == 0:  # Basics
            if hasattr(self, 'name_var') and not self.name_var.get().strip():
                self.character_data["name"] = "Unnamed Character"
            else:
                self.character_data["name"] = self.name_var.get().strip() if hasattr(self, 'name_var') else "Unnamed Character"
            return True
        return True  # Other steps can proceed without validation for now
        
    def finish_character(self):
        # Collect all data
        if hasattr(self, 'name_var'):
            self.character_data["name"] = self.name_var.get()
            
        # Collect attributes
        if hasattr(self, 'attr_vars'):
            for attr, var in self.attr_vars.items():
                self.character_data["attributes"][attr] = int(var.get())
                
        # Collect skills
        if hasattr(self, 'skill_vars'):
            self.character_data["skills"] = [
                {"name": name, "level": int(var.get())} 
                for name, var in self.skill_vars.items() 
                if var.get() != "0"
            ]
            
        # Collect talents
        if hasattr(self, 'talent_vars'):
            self.character_data["talents"] = [
                {"name": name} 
                for name, var in self.talent_vars.items() 
                if var.get()
            ]
            
        # Collect assets
        if hasattr(self, 'asset_vars'):
            self.character_data["assets"].extend([
                {"type": "asset", "name": name} 
                for name, var in self.asset_vars.items() 
                if var.get()
            ])
            
        # Collect followers
        if hasattr(self, 'follower_vars'):
            self.character_data["assets"].extend([
                {"type": "follower", "name": name} 
                for name, var in self.follower_vars.items() 
                if var.get()
            ])
            
        # Save character
        self.save_character()
        messagebox.showinfo("Success", f"Character '{self.character_data['name']}' created successfully!")
        
    def save_character(self):
        """Save character to file"""
        try:
            # Create characters directory if it doesn't exist
            char_dir = os.path.join(os.path.dirname(__file__), '..', 'characters')
            os.makedirs(char_dir, exist_ok=True)
            
            # Save character file
            filename = f"{self.character_data['name'].replace(' ', '_')}.json"
            filepath = os.path.join(char_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(self.character_data, f, indent=2)
                
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save character: {e}")
            
    def get_frame(self):
        return self.frame

