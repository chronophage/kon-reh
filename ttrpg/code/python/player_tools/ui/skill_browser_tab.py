# player_tools/ui/skill_browser_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys

# Use the correct import path for your structure
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.database.skill_db import SkillDatabase, SkillCategory, TalentType

class SkillBrowserTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        try:
            # The database will use the default path (shared/data/skills.db)
            self.db = SkillDatabase()
            self.create_ui()
            self.refresh_data()
        except Exception as e:
            error_frame = ttk.Frame(self.frame)
            error_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            error_label = ttk.Label(error_frame, text=f"Database Error: {str(e)}")
            error_label.pack(pady=20)

    def create_ui(self):
        # Create notebook for different browsing modes
        self.browser_notebook = ttk.Notebook(self.frame)
        self.browser_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Skills Tab
        self.skills_frame = ttk.Frame(self.browser_notebook)
        self.skills_frame.pack(fill=tk.BOTH, expand=True)
        self.create_skills_tab()
        self.browser_notebook.add(self.skills_frame, text="Skills")
        
        # Talents Tab
        self.talents_frame = ttk.Frame(self.browser_notebook)
        self.talents_frame.pack(fill=tk.BOTH, expand=True)
        self.create_talents_tab()
        self.browser_notebook.add(self.talents_frame, text="Talents")
        
        # Prestige Talents Tab
        self.prestige_frame = ttk.Frame(self.browser_notebook)
        self.prestige_frame.pack(fill=tk.BOTH, expand=True)
        self.create_prestige_tab()
        self.browser_notebook.add(self.prestige_frame, text="Prestige Talents")
        
        # Custom Content Tab
        self.custom_frame = ttk.Frame(self.browser_notebook)
        self.custom_frame.pack(fill=tk.BOTH, expand=True)
        self.create_custom_tab()
        self.browser_notebook.add(self.custom_frame, text="Custom Content")
        
    def create_skills_tab(self):
        # Skills filter frame
        filter_frame = ttk.LabelFrame(self.skills_frame, text="Filter Skills", padding="5")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Category:").pack(side=tk.LEFT)
        self.skill_category_var = tk.StringVar(value="All")
        categories = ["All"] + [cat.value for cat in SkillCategory]
        self.skill_category_combo = ttk.Combobox(filter_frame, textvariable=self.skill_category_var,
                                                 values=categories, width=15)
        self.skill_category_combo.pack(side=tk.LEFT, padx=(5, 10))
        self.skill_category_combo.bind("<<ComboboxSelected>>", self._filter_skills)
        
        ttk.Button(filter_frame, text="Refresh", command=self._filter_skills).pack(side=tk.LEFT)
        
        # Skills list
        list_frame = ttk.Frame(self.skills_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for skills
        columns = ("Name", "Category", "Attributes", "Max Rating")
        self.skills_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.skills_tree.heading(col, text=col)
            self.skills_tree.column(col, width=100)
        
        self.skills_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.skills_tree.bind("<<TreeviewSelect>>", self._on_skill_selected)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.skills_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.skills_tree.configure(yscrollcommand=scrollbar.set)
        
        # Skill details
        details_frame = ttk.LabelFrame(self.skills_frame, text="Skill Details", padding="10")
        details_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        self.skill_details_text = tk.Text(details_frame, height=8, wrap=tk.WORD)
        self.skill_details_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.skill_details_text.yview)
        details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.skill_details_text.configure(yscrollcommand=details_scrollbar.set)
        
    def create_talents_tab(self):
        # Talents filter frame
        filter_frame = ttk.LabelFrame(self.talents_frame, text="Filter Talents", padding="5")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Type:").pack(side=tk.LEFT)
        self.talent_type_var = tk.StringVar(value="All")
        types = ["All"] + [t.value for t in TalentType]
        self.talent_type_combo = ttk.Combobox(filter_frame, textvariable=self.talent_type_var,
                                             values=types, width=15)
        self.talent_type_combo.pack(side=tk.LEFT, padx=(5, 10))
        self.talent_type_combo.bind("<<ComboboxSelected>>", self._filter_talents)
        
        ttk.Button(filter_frame, text="Refresh", command=self._filter_talents).pack(side=tk.LEFT)
        
        # Talents list
        list_frame = ttk.Frame(self.talents_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for talents
        columns = ("Name", "Type", "Cost", "Culture")
        self.talents_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.talents_tree.heading(col, text=col)
            self.talents_tree.column(col, width=120)
        
        self.talents_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.talents_tree.bind("<<TreeviewSelect>>", self._on_talent_selected)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.talents_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.talents_tree.configure(yscrollcommand=scrollbar.set)
        
        # Talent details
        details_frame = ttk.LabelFrame(self.talents_frame, text="Talent Details", padding="10")
        details_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        self.talent_details_text = tk.Text(details_frame, height=8, wrap=tk.WORD)
        self.talent_details_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.talent_details_text.yview)
        details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.talent_details_text.configure(yscrollcommand=details_scrollbar.set)
        
    def create_prestige_tab(self):
        # Prestige filter frame
        filter_frame = ttk.LabelFrame(self.prestige_frame, text="Filter Prestige Talents", padding="5")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Tier:").pack(side=tk.LEFT)
        self.prestige_tier_var = tk.StringVar(value="All")
        tiers = ["All", "1", "2", "3", "4", "5"]
        self.prestige_tier_combo = ttk.Combobox(filter_frame, textvariable=self.prestige_tier_var,
                                               values=tiers, width=10)
        self.prestige_tier_combo.pack(side=tk.LEFT, padx=(5, 10))
        self.prestige_tier_combo.bind("<<ComboboxSelected>>", self._filter_prestige)
        
        ttk.Button(filter_frame, text="Refresh", command=self._filter_prestige).pack(side=tk.LEFT)
        
        # Prestige talents list
        list_frame = ttk.Frame(self.prestige_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for prestige talents
        columns = ("Name", "Tier", "Cost", "Culture")
        self.prestige_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.prestige_tree.heading(col, text=col)
            self.prestige_tree.column(col, width=120)
        
        self.prestige_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.prestige_tree.bind("<<TreeviewSelect>>", self._on_prestige_selected)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.prestige_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.prestige_tree.configure(yscrollcommand=scrollbar.set)
        
        # Prestige talent details
        details_frame = ttk.LabelFrame(self.prestige_frame, text="Prestige Talent Details", padding="10")
        details_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        self.prestige_details_text = tk.Text(details_frame, height=8, wrap=tk.WORD)
        self.prestige_details_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.prestige_details_text.yview)
        details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.prestige_details_text.configure(yscrollcommand=details_scrollbar.set)
        
    def create_custom_tab(self):
        # Custom content creation frame
        create_frame = ttk.LabelFrame(self.custom_frame, text="Create Custom Content", padding="10")
        create_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Content type selection
        ttk.Label(create_frame, text="Content Type:").grid(row=0, column=0, sticky=tk.W)
        self.custom_type_var = tk.StringVar(value="Skill")
        self.custom_type_combo = ttk.Combobox(create_frame, textvariable=self.custom_type_var,
                                             values=["Skill", "Talent", "Prestige Talent"], width=15)
        self.custom_type_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        self.custom_type_combo.bind("<<ComboboxSelected>>", self._update_custom_form)
        
        # Custom content form
        self.custom_form_frame = ttk.Frame(create_frame)
        self.custom_form_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        self._create_custom_skill_form()
        
        # Action buttons
        button_frame = ttk.Frame(create_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Save Custom Content", command=self._save_custom_content).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Clear Form", command=self._clear_custom_form).pack(side=tk.LEFT)
        
        # Custom content list
        list_frame = ttk.LabelFrame(self.custom_frame, text="Custom Content", padding="5")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("Name", "Type", "Cost")
        self.custom_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.custom_tree.heading(col, text=col)
            self.custom_tree.column(col, width=150)
        
        self.custom_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.custom_tree.bind("<<TreeviewSelect>>", self._on_custom_selected)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.custom_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.custom_tree.configure(yscrollcommand=scrollbar.set)
        
    def _create_custom_skill_form(self):
        # Clear existing form
        for widget in self.custom_form_frame.winfo_children():
            widget.destroy()
            
        # Skill form fields
        ttk.Label(self.custom_form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.custom_name_var = tk.StringVar()
        ttk.Entry(self.custom_form_frame, textvariable=self.custom_name_var, width=25).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(self.custom_form_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_category_var = tk.StringVar(value="General")
        ttk.Combobox(self.custom_form_frame, textvariable=self.custom_category_var,
                    values=[cat.value for cat in SkillCategory], width=15).grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        ttk.Label(self.custom_form_frame, text="Attributes:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_attributes_var = tk.StringVar()
        ttk.Entry(self.custom_form_frame, textvariable=self.custom_attributes_var, width=25).grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        ttk.Label(self.custom_form_frame, text="Max Rating:").grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_max_rating_var = tk.StringVar(value="5")
        ttk.Spinbox(self.custom_form_frame, from_=1, to=10, textvariable=self.custom_max_rating_var, width=5).grid(row=3, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        ttk.Label(self.custom_form_frame, text="Cost Formula:").grid(row=4, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_cost_formula_var = tk.StringVar(value="new_level * 2")
        ttk.Entry(self.custom_form_frame, textvariable=self.custom_cost_formula_var, width=25).grid(row=4, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        ttk.Label(self.custom_form_frame, text="Description:").grid(row=5, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_description_text = tk.Text(self.custom_form_frame, height=4, width=40)
        self.custom_description_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
    def _create_custom_talent_form(self):
        # Clear existing form
        for widget in self.custom_form_frame.winfo_children():
            widget.destroy()
            
        # Talent form fields
        ttk.Label(self.custom_form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.custom_name_var = tk.StringVar()
        ttk.Entry(self.custom_form_frame, textvariable=self.custom_name_var, width=25).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(self.custom_form_frame, text="Talent Type:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_talent_type_var = tk.StringVar(value="General")
        ttk.Combobox(self.custom_form_frame, textvariable=self.custom_talent_type_var,
                    values=[t.value for t in TalentType], width=15).grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        ttk.Label(self.custom_form_frame, text="Culture:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_culture_var = tk.StringVar()
        ttk.Entry(self.custom_form_frame, textvariable=self.custom_culture_var, width=25).grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        ttk.Label(self.custom_form_frame, text="Cost (XP):").grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_cost_var = tk.StringVar()
        ttk.Entry(self.custom_form_frame, textvariable=self.custom_cost_var, width=10).grid(row=3, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        ttk.Label(self.custom_form_frame, text="Prerequisites:").grid(row=4, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_prerequisites_text = tk.Text(self.custom_form_frame, height=3, width=40)
        self.custom_prerequisites_text.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(self.custom_form_frame, text="Description:").grid(row=6, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_description_text = tk.Text(self.custom_form_frame, height=4, width=40)
        self.custom_description_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
    def _create_custom_prestige_form(self):
        # Clear existing form
        for widget in self.custom_form_frame.winfo_children():
            widget.destroy()
            
        # Prestige talent form fields
        ttk.Label(self.custom_form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.custom_name_var = tk.StringVar()
        ttk.Entry(self.custom_form_frame, textvariable=self.custom_name_var, width=25).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(self.custom_form_frame, text="Tier:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_tier_var = tk.StringVar(value="1")
        ttk.Spinbox(self.custom_form_frame, from_=1, to=5, textvariable=self.custom_tier_var, width=5).grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        ttk.Label(self.custom_form_frame, text="Culture:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_culture_var = tk.StringVar()
        ttk.Entry(self.custom_form_frame, textvariable=self.custom_culture_var, width=25).grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        ttk.Label(self.custom_form_frame, text="Cost (XP):").grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_cost_var = tk.StringVar()
        ttk.Entry(self.custom_form_frame, textvariable=self.custom_cost_var, width=10).grid(row=3, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        ttk.Label(self.custom_form_frame, text="Prerequisites:").grid(row=4, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_prerequisites_text = tk.Text(self.custom_form_frame, height=3, width=40)
        self.custom_prerequisites_text.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(self.custom_form_frame, text="Description:").grid(row=6, column=0, sticky=tk.W, pady=(5, 0))
        self.custom_description_text = tk.Text(self.custom_form_frame, height=4, width=40)
        self.custom_description_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
    def _update_custom_form(self, event=None):
        content_type = self.custom_type_var.get()
        if content_type == "Skill":
            self._create_custom_skill_form()
        elif content_type == "Talent":
            self._create_custom_talent_form()
        elif content_type == "Prestige Talent":
            self._create_custom_prestige_form()
            
    def refresh_data(self):
        """Refresh all data in the browser"""
        self._filter_skills()
        self._filter_talents()
        self._filter_prestige()
        self._refresh_custom_content()
        
    def _filter_skills(self, event=None):
        # Clear existing items
        for item in self.skills_tree.get_children():
            self.skills_tree.delete(item)
            
        # Get filtered skills
        category = self.skill_category_var.get()
        if category == "All":
            skills = self.db.get_all_skills()
        else:
            skills = self.db.get_skills_by_category(SkillCategory(category))
            
        # Add to treeview
        for skill in skills:
            self.skills_tree.insert("", tk.END, values=(
                skill.name,
                skill.category.value,
                skill.attribute_links,
                skill.max_rating
            ))
            
    def _filter_talents(self, event=None):
        # Clear existing items
        for item in self.talents_tree.get_children():
            self.talents_tree.delete(item)
            
        # Get filtered talents
        talent_type = self.talent_type_var.get()
        if talent_type == "All":
            talents = self.db.get_all_talents()
        else:
            talents = self.db.get_talents_by_type(TalentType(talent_type))
            
        # Add to treeview
        for talent in talents:
            self.talents_tree.insert("", tk.END, values=(
                talent.name,
                talent.talent_type.value,
                talent.cost,
                talent.culture or "Any"
            ))
            
    def _filter_prestige(self, event=None):
        # Clear existing items
        for item in self.prestige_tree.get_children():
            self.prestige_tree.delete(item)
            
        # Get filtered prestige talents
        tier = self.prestige_tier_var.get()
        if tier == "All":
            talents = self.db.get_all_prestige_talents()
        else:
            talents = self.db.get_prestige_talents_by_tier(int(tier))
            
        # Add to treeview
        for talent in talents:
            self.prestige_tree.insert("", tk.END, values=(
                talent.name,
                talent.tier,
                talent.cost,
                talent.culture or "Any"
            ))
            
    def _refresh_custom_content(self):
        # Clear existing items
        for item in self.custom_tree.get_children():
            self.custom_tree.delete(item)
            
        # Add custom skills
        custom_skills = [s for s in self.db.get_all_skills() if s.is_custom]
        for skill in custom_skills:
            self.custom_tree.insert("", tk.END, values=(skill.name, "Skill", "-"))
            
        # Add custom talents
        custom_talents = [t for t in self.db.get_all_talents() if t.is_custom]
        for talent in custom_talents:
            self.custom_tree.insert("", tk.END, values=(talent.name, "Talent", talent.cost))
            
        # Add custom prestige talents
        custom_prestige = [p for p in self.db.get_all_prestige_talents() if p.is_custom]
        for talent in custom_prestige:
            self.custom_tree.insert("", tk.END, values=(talent.name, "Prestige Talent", talent.cost))
            
    def _on_skill_selected(self, event=None):
        selection = self.skills_tree.selection()
        if not selection:
            return
            
        item = self.skills_tree.item(selection[0])
        skill_name = item['values'][0]
        
        skill = self.db.get_skill_by_name(skill_name)
        if skill:
            details = f"Name: {skill.name}\n"
            details += f"Category: {skill.category.value}\n"
            details += f"Attributes: {skill.attribute_links}\n"
            details += f"Max Rating: {skill.max_rating}\n"
            details += f"Cost Formula: {skill.cost_formula}\n\n"
            details += f"Description:\n{skill.description}"
            
            self.skill_details_text.delete(1.0, tk.END)
            self.skill_details_text.insert(1.0, details)
            
    def _on_talent_selected(self, event=None):
        selection = self.talents_tree.selection()
        if not selection:
            return
            
        item = self.talents_tree.item(selection[0])
        talent_name = item['values'][0]
        
        # Find talent (simplified - in real implementation would search all talent types)
        talents = self.db.get_all_talents()
        talent = next((t for t in talents if t.name == talent_name), None)
        
        if talent:
            details = f"Name: {talent.name}\n"
            details += f"Type: {talent.talent_type.value}\n"
            details += f"Cost: {talent.cost} XP\n"
            details += f"Culture: {talent.culture or 'Any'}\n\n"
            details += f"Prerequisites: {talent.prerequisites}\n\n"
            details += f"Description:\n{talent.description}"
            
            self.talent_details_text.delete(1.0, tk.END)
            self.talent_details_text.insert(1.0, details)
            
    def _on_prestige_selected(self, event=None):
        selection = self.prestige_tree.selection()
        if not selection:
            return
            
        item = self.prestige_tree.item(selection[0])
        talent_name = item['values'][0]
        
        # Find prestige talent
        talents = self.db.get_all_prestige_talents()
        talent = next((t for t in talents if t.name == talent_name), None)
        
        if talent:
            details = f"Name: {talent.name}\n"
            details += f"Tier: {talent.tier}\n"
            details += f"Cost: {talent.cost} XP\n"
            details += f"Culture: {talent.culture or 'Any'}\n\n"
            details += f"Prerequisites: {talent.prerequisites}\n\n"
            details += f"Description:\n{talent.description}"
            
            self.prestige_details_text.delete(1.0, tk.END)
            self.prestige_details_text.insert(1.0, details)
            
    def _on_custom_selected(self, event=None):
        # In a full implementation, this would show details of selected custom content
        pass
        
    def _save_custom_content(self):
        content_type = self.custom_type_var.get()
        
        try:
            if content_type == "Skill":
                from shared.database.skill_db import Skill
                skill = Skill(
                    id=None,
                    name=self.custom_name_var.get(),
                    category=SkillCategory(self.custom_category_var.get()),
                    description=self.custom_description_text.get(1.0, tk.END).strip(),
                    attribute_links=self.custom_attributes_var.get(),
                    cost_formula=self.custom_cost_formula_var.get(),
                    max_rating=int(self.custom_max_rating_var.get()),
                    is_custom=True
                )
                
                if self.db.add_custom_skill(skill):
                    messagebox.showinfo("Success", "Custom skill saved successfully!")
                else:
                    messagebox.showerror("Error", "Failed to save skill (may already exist)")
                    
            elif content_type == "Talent":
                from shared.database.skill_db import Talent
                talent = Talent(
                    id=None,
                    name=self.custom_name_var.get(),
                    talent_type=TalentType(self.custom_talent_type_var.get()),
                    description=self.custom_description_text.get(1.0, tk.END).strip(),
                    cost=int(self.custom_cost_var.get()),
                    prerequisites=self.custom_prerequisites_text.get(1.0, tk.END).strip(),
                    culture=self.custom_culture_var.get(),
                    is_custom=True
                )
                
                if self.db.add_custom_talent(talent):
                    messagebox.showinfo("Success", "Custom talent saved successfully!")
                else:
                    messagebox.showerror("Error", "Failed to save talent (may already exist)")
                    
            elif content_type == "Prestige Talent":
                from shared.database.skill_db import PrestigeTalent
                talent = PrestigeTalent(
                    id=None,
                    name=self.custom_name_var.get(),
                    description=self.custom_description_text.get(1.0, tk.END).strip(),
                    cost=int(self.custom_cost_var.get()),
                    prerequisites=self.custom_prerequisites_text.get(1.0, tk.END).strip(),
                    tier=int(self.custom_tier_var.get()),
                    culture=self.custom_culture_var.get(),
                    is_custom=True
                )
                
                if self.db.add_custom_prestige_talent(talent):
                    messagebox.showinfo("Success", "Custom prestige talent saved successfully!")
                else:
                    messagebox.showerror("Error", "Failed to save prestige talent (may already exist)")
                    
            # Refresh the custom content list
            self._refresh_custom_content()
            self._clear_custom_form()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save custom content: {str(e)}")
            
    def _clear_custom_form(self):
        # Clear all form fields
        for widget in self.custom_form_frame.winfo_children():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete(1.0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                if hasattr(widget, 'current'):
                    widget.current(0)
            elif isinstance(widget, ttk.Spinbox):
                widget.delete(0, tk.END)
                widget.insert(0, "1" if widget.cget('from') == 1 else "0")
                
    def get_frame(self):
        return self.frame

