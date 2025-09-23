# player_tools/ui/character_sheet_tab.py
import tkinter as tk
from tkinter import ttk

class CharacterSheetTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        # Create a simple character sheet layout
        self.create_character_sheet()
        
    def create_character_sheet(self):
        # Character Info Section
        info_frame = ttk.LabelFrame(self.frame, text="Character Information", padding="10")
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Name and Archetype row
        name_frame = ttk.Frame(info_frame)
        name_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(name_frame, text="Name:").pack(side=tk.LEFT)
        self.name_var = tk.StringVar()
        ttk.Entry(name_frame, textvariable=self.name_var, width=25).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(name_frame, text="Archetype:").pack(side=tk.LEFT)
        self.archetype_var = tk.StringVar(value="Solo")
        ttk.Combobox(name_frame, textvariable=self.archetype_var, 
                    values=["Solo", "Mixed", "Mastermind"], width=15).pack(side=tk.LEFT, padx=(5, 0))
        
        # Attributes Section
        attr_frame = ttk.LabelFrame(self.frame, text="Attributes", padding="10")
        attr_frame.pack(fill=tk.X, padx=5, pady=5)
        
        attr_row = ttk.Frame(attr_frame)
        attr_row.pack(fill=tk.X)
        
        self.attributes = {}
        attr_names = ["Body", "Wits", "Spirit", "Presence"]
        for i, attr in enumerate(attr_names):
            if i > 0 and i % 2 == 0:  # Start new row after every 2 attributes
                attr_row = ttk.Frame(attr_frame)
                attr_row.pack(fill=tk.X, pady=(5, 0))
                
            attr_col = ttk.Frame(attr_row)
            attr_col.pack(side=tk.LEFT, expand=True, fill=tk.X)
            
            ttk.Label(attr_col, text=f"{attr}:").pack(side=tk.LEFT)
            var = tk.StringVar(value="2")
            self.attributes[attr] = var
            ttk.Entry(attr_col, textvariable=var, width=5).pack(side=tk.LEFT, padx=(5, 0))
            
        # Skills Section
        skills_frame = ttk.LabelFrame(self.frame, text="Skills", padding="10")
        skills_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.skills = {}
        skill_names = ["Melee", "Ranged", "Athletics", "Arcana", 
                      "Diplomacy", "Stealth", "Deception", "Survival",
                      "Command", "Craft", "Performance", "Lore"]
        
        # Create skill rows with 3 skills per row
        for i in range(0, len(skill_names), 3):
            skill_row = ttk.Frame(skills_frame)
            skill_row.pack(fill=tk.X, pady=(0, 5) if i < len(skill_names) - 3 else 0)
            
            row_skills = skill_names[i:i+3]
            for j, skill in enumerate(row_skills):
                skill_col = ttk.Frame(skill_row)
                skill_col.pack(side=tk.LEFT, expand=True, fill=tk.X)
                
                ttk.Label(skill_col, text=f"{skill}:").pack(side=tk.LEFT)
                var = tk.StringVar(value="0")
                self.skills[skill] = var
                ttk.Entry(skill_col, textvariable=var, width=5).pack(side=tk.LEFT, padx=(5, 0))
        
        # Resources Section
        resources_frame = ttk.LabelFrame(self.frame, text="Resources", padding="10")
        resources_frame.pack(fill=tk.X, padx=5, pady=5)
        
        resources_row = ttk.Frame(resources_frame)
        resources_row.pack(fill=tk.X)
        
        ttk.Label(resources_row, text="Current XP:").pack(side=tk.LEFT)
        self.xp_var = tk.StringVar(value="0")
        ttk.Entry(resources_row, textvariable=self.xp_var, width=10).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(resources_row, text="Boons:").pack(side=tk.LEFT)
        self.boons_var = tk.StringVar(value="0")
        ttk.Entry(resources_row, textvariable=self.boons_var, width=5).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(resources_row, text="Fatigue:").pack(side=tk.LEFT)
        self.fatigue_var = tk.StringVar(value="0")
        ttk.Entry(resources_row, textvariable=self.fatigue_var, width=5).pack(side=tk.LEFT, padx=(5, 0))
        
        # Notes Section
        notes_frame = ttk.LabelFrame(self.frame, text="Notes", padding="10")
        notes_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.notes_text = tk.Text(notes_frame, height=8)
        self.notes_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(notes_frame, orient=tk.VERTICAL, command=self.notes_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.notes_text.configure(yscrollcommand=scrollbar.set)
        
    def get_frame(self):
        return self.frame

