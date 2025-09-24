# player_tools/ui/skill_tracker_tab.py
import tkinter as tk
from tkinter import ttk

class SkillTrackerTab:
    def __init__(self, parent):
        self.parent = parent
        # If database access is needed:
        # project_root = os.path.join(os.path.dirname(__file__), '..', '..')
        # db_path = os.path.join(project_root, 'shared', 'data', 'skills.db')
        # db_path = os.path.abspath(db_path)
        # self.db = SkillDatabase(db_path)  # or pass db_path to SkillDatabase()
        
        self.skills = {}  # {skill_name: {"attribute": attr, "level": level}}
        self.create_ui()   

        # Add Skill Frame
        add_frame = ttk.LabelFrame(self.parent, text="Add Skill", padding="15")
        add_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(add_frame, text="Skill Name:").grid(row=0, column=0, sticky="w", padx=5)
        self.skill_name_entry = ttk.Entry(add_frame, width=20)
        self.skill_name_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(add_frame, text="Attribute:").grid(row=0, column=2, sticky="w", padx=5)
        self.skill_attr_var = tk.StringVar(value="Body")
        attr_combo = ttk.Combobox(add_frame, textvariable=self.skill_attr_var,
                                values=["Body", "Wits", "Spirit", "Presence"],
                                width=10, state="readonly")
        attr_combo.grid(row=0, column=3, padx=5)
        
        ttk.Label(add_frame, text="Level:").grid(row=0, column=4, sticky="w", padx=5)
        self.skill_level_var = tk.StringVar(value="0")
        level_combo = ttk.Combobox(add_frame, textvariable=self.skill_level_var,
                                 values=["0", "1", "2", "3", "4", "5"],
                                 width=5, state="readonly")
        level_combo.grid(row=0, column=5, padx=5)
        
        ttk.Button(add_frame, text="Add Skill", command=self.add_skill).grid(row=0, column=6, padx=10)
        
        # Skills Display
        self.skills_frame = ttk.Frame(self.parent)
        self.skills_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Skill Info
        info_frame = ttk.LabelFrame(self.parent, text="Skill Information", padding="10")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
Skill Ratings:
• 0: Untrained - Rely on raw attribute
• 1: Familiar - Basic competence
• 2: Skilled - Reliable training
• 3: Expert - Professional mastery
• 4: Master - Renowned ability
• 5: Legendary - Near-mythic talent

Dice Pool Calculation:
Pool = Attribute + Skill
Example: Body 3 + Melee 3 = 6 dice pool
        """.strip()
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack()
        
        self.refresh_skills_display()
        
    def add_skill(self):
        name = self.skill_name_entry.get().strip()
        if name and name not in self.skills:
            self.skills[name] = {
                "attribute": self.skill_attr_var.get(),
                "level": int(self.skill_level_var.get())
            }
            self.skill_name_entry.delete(0, tk.END)
            self.refresh_skills_display()
            
    def remove_skill(self, skill_name):
        if skill_name in self.skills:
            del self.skills[skill_name]
            self.refresh_skills_display()
            
    def update_skill_level(self, skill_name, new_level):
        if skill_name in self.skills:
            self.skills[skill_name]["level"] = new_level
            self.refresh_skills_display()
            
    def refresh_skills_display(self):
        # Clear existing widgets
        for widget in self.skills_frame.winfo_children():
            widget.destroy()
            
        if not self.skills:
            ttk.Label(self.skills_frame, text="No skills added").pack(pady=20)
            return
            
        # Create scrollable area
        canvas = tk.Canvas(self.skills_frame)
        scrollbar = ttk.Scrollbar(self.skills_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display skills
        for skill_name, skill_data in self.skills.items():
            skill_frame = ttk.LabelFrame(scrollable_frame, text=skill_name, padding="10")
            skill_frame.pack(fill="x", pady=5, padx=5)
            
            # Skill details
            details_frame = ttk.Frame(skill_frame)
            details_frame.pack(fill="x", pady=2)
            
            ttk.Label(details_frame, text=f"Attribute: {skill_data['attribute']}").pack(side="left", padx=10)
            
            # Level control
            level_frame = ttk.Frame(details_frame)
            level_frame.pack(side="left", padx=10)
            ttk.Label(level_frame, text="Level:").pack(side="left")
            level_var = tk.StringVar(value=str(skill_data['level']))
            level_combo = ttk.Combobox(level_frame, textvariable=level_var,
                                     values=["0", "1", "2", "3", "4", "5"],
                                     width=5, state="readonly")
            level_combo.pack(side="left", padx=5)
            level_combo.bind("<<ComboboxSelected>>", 
                           lambda e, s=skill_name, v=level_var: self.update_skill_level(s, int(v.get())))
            
            # Pool calculation
            attr_values = {"Body": 2, "Wits": 2, "Spirit": 2, "Presence": 2}  # Default values
            # In full implementation, these would come from character sheet
            pool = attr_values.get(skill_data['attribute'], 2) + skill_data['level']
            ttk.Label(details_frame, text=f"Pool: {pool}d10", font=("Arial", 10, "bold")).pack(side="left", padx=20)
            
            # Remove button
            ttk.Button(details_frame, text="Remove", 
                      command=lambda s=skill_name: self.remove_skill(s)).pack(side="right")
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
