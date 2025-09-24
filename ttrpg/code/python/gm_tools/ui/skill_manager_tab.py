# gm_tools/ui/skill_manager_tab.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import sys
import csv

# Use the correct import path for your structure
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.database.skill_db import SkillDatabase, SkillCategory, TalentType

class SkillManagerTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

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
        # Create notebook for different management modes
        self.manager_notebook = ttk.Notebook(self.frame)
        self.manager_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create all tabs
        self.create_browse_tab()
        self.create_import_export_tab()
        self.create_manage_custom_tab()
        
    def create_browse_tab(self):
        # Create the browse frame
        browse_frame = ttk.Frame(self.manager_notebook)
        
        # Create filter controls
        filter_frame = ttk.LabelFrame(browse_frame, text="Filter Content", padding="10")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Filter controls row
        filter_row = ttk.Frame(filter_frame)
        filter_row.pack(fill=tk.X)
        
        # Skill Category Filter
        ttk.Label(filter_row, text="Skill Category:").pack(side=tk.LEFT, padx=(0, 5))
        self.skill_category_var = tk.StringVar(value="All")
        categories = ["All"] + [cat.value for cat in SkillCategory]
        self.skill_category_combo = ttk.Combobox(filter_row, textvariable=self.skill_category_var,
                                                 values=categories, width=12, state="readonly")
        self.skill_category_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.skill_category_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_content_list())
        
        # Talent Type Filter
        ttk.Label(filter_row, text="Talent Type:").pack(side=tk.LEFT, padx=(0, 5))
        self.talent_type_var = tk.StringVar(value="All")
        talent_types = ["All"] + [t.value for t in TalentType]
        self.talent_type_combo = ttk.Combobox(filter_row, textvariable=self.talent_type_var,
                                             values=talent_types, width=12, state="readonly")
        self.talent_type_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.talent_type_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_content_list())
        
        # Prestige Tier Filter
        ttk.Label(filter_row, text="Prestige Tier:").pack(side=tk.LEFT, padx=(0, 5))
        self.prestige_tier_var = tk.StringVar(value="All")
        tiers = ["All", "1", "2", "3", "4", "5"]
        self.prestige_tier_combo = ttk.Combobox(filter_row, textvariable=self.prestige_tier_var,
                                               values=tiers, width=8, state="readonly")
        self.prestige_tier_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.prestige_tier_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_content_list())
        
        # Refresh Button
        ttk.Button(filter_row, text="Refresh", command=self.refresh_content_list).pack(side=tk.LEFT)
        
        # Content Tree
        content_frame = ttk.Frame(browse_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ("Name", "Type", "Category/Tier", "Cost", "Custom")
        self.content_tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=12)
        
        # Define headings
        self.content_tree.heading("Name", text="Name")
        self.content_tree.heading("Type", text="Type")
        self.content_tree.heading("Category/Tier", text="Category/Tier")
        self.content_tree.heading("Cost", text="Cost")
        self.content_tree.heading("Custom", text="Custom")
        
        # Define column widths
        self.content_tree.column("Name", width=150)
        self.content_tree.column("Type", width=100)
        self.content_tree.column("Category/Tier", width=120)
        self.content_tree.column("Cost", width=80)
        self.content_tree.column("Custom", width=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.content_tree.yview)
        h_scrollbar = ttk.Scrollbar(content_frame, orient=tk.HORIZONTAL, command=self.content_tree.xview)
        self.content_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.content_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Bind selection
        self.content_tree.bind("<<TreeviewSelect>>", self.on_content_selected)
        
        # Details Frame
        details_frame = ttk.LabelFrame(browse_frame, text="Content Details", padding="10")
        details_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        # Text widget with scrollbar
        self.details_text = tk.Text(details_frame, height=8, wrap=tk.WORD)
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scrollbar.set)
        
        self.details_text.grid(row=0, column=0, sticky="nsew")
        details_scrollbar.grid(row=0, column=1, sticky="ns")
        
        details_frame.grid_rowconfigure(0, weight=1)
        details_frame.grid_columnconfigure(0, weight=1)
        
        # Add to notebook
        self.manager_notebook.add(browse_frame, text="Browse Content")
        
    def create_import_export_tab(self):
        # Create the import/export frame
        io_frame = ttk.Frame(self.manager_notebook)
        
        # Main label frame
        main_frame = ttk.LabelFrame(io_frame, text="Import/Export Skills & Talents", padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # JSON Section
        json_frame = ttk.LabelFrame(main_frame, text="JSON Format", padding="10")
        json_frame.pack(fill=tk.X, pady=(0, 10))
        
        json_btn_frame = ttk.Frame(json_frame)
        json_btn_frame.pack(fill=tk.X)
        
        ttk.Button(json_btn_frame, text="Export All Content", command=self.export_all_json).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(json_btn_frame, text="Export Custom Only", command=self.export_custom_json).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(json_btn_frame, text="Import from JSON", command=self.import_json).pack(side=tk.LEFT)
        
        json_desc = ttk.Label(json_frame, text="JSON: Complete data exchange format. 'Custom Only' exports player-friendly content.")
        json_desc.pack(anchor=tk.W, pady=(5, 0))
        
        # CSV Section
        csv_frame = ttk.LabelFrame(main_frame, text="CSV Format", padding="10")
        csv_frame.pack(fill=tk.X, pady=(0, 10))
        
        csv_btn_frame = ttk.Frame(csv_frame)
        csv_btn_frame.pack(fill=tk.X)
        
        ttk.Button(csv_btn_frame, text="Export All to CSV", command=self.export_all_csv).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(csv_btn_frame, text="Import from CSV", command=self.import_csv).pack(side=tk.LEFT)
        
        csv_desc = ttk.Label(csv_frame, text="CSV: Multiple files for each content type. Easier to edit in spreadsheets.")
        csv_desc.pack(anchor=tk.W, pady=(5, 0))
        
        # Status Area
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        self.io_status_text = tk.Text(status_frame, height=10)
        io_status_scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.io_status_text.yview)
        self.io_status_text.configure(yscrollcommand=io_status_scrollbar.set)
        
        self.io_status_text.grid(row=0, column=0, sticky="nsew")
        io_status_scrollbar.grid(row=0, column=1, sticky="ns")
        
        status_frame.grid_rowconfigure(0, weight=1)
        status_frame.grid_columnconfigure(0, weight=1)
        
        # Add to notebook
        self.manager_notebook.add(io_frame, text="Import/Export")
        
    def create_manage_custom_tab(self):
        # Create the manage custom frame
        manage_frame = ttk.Frame(self.manager_notebook)
        
        # Main label frame
        main_frame = ttk.LabelFrame(manage_frame, text="Manage Custom Content", padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Custom content tree
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        columns = ("Name", "Type", "Cost")
        self.custom_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
        
        # Define headings
        self.custom_tree.heading("Name", text="Name")
        self.custom_tree.heading("Type", text="Type")
        self.custom_tree.heading("Cost", text="Cost")
        
        # Define column widths
        self.custom_tree.column("Name", width=200)
        self.custom_tree.column("Type", width=120)
        self.custom_tree.column("Cost", width=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.custom_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.custom_tree.xview)
        self.custom_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.custom_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Refresh List", command=self.refresh_custom_list).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected_custom).pack(side=tk.LEFT)
        
        # Add to notebook
        self.manager_notebook.add(manage_frame, text="Manage Custom")
        
    def refresh_data(self):
        """Refresh all data in the UI"""
        self.refresh_content_list()
        self.refresh_custom_list()
        
    def refresh_content_list(self):
        """Refresh the main content list based on filters"""
        # Clear existing items
        for item in self.content_tree.get_children():
            self.content_tree.delete(item)
            
        try:
            # Get filtered content
            # Skills
            skill_category = self.skill_category_var.get()
            if skill_category == "All":
                skills = self.db.get_all_skills()
            else:
                skills = self.db.get_skills_by_category(SkillCategory(skill_category))
                
            for skill in skills:
                self.content_tree.insert("", tk.END, values=(
                    skill.name,
                    "Skill",
                    skill.category.value,
                    skill.cost_formula or "-",
                    "Yes" if skill.is_custom else "No"
                ))
                
            # Talents
            talent_type = self.talent_type_var.get()
            if talent_type == "All":
                talents = self.db.get_all_talents()
            else:
                talents = self.db.get_talents_by_type(TalentType(talent_type))
                
            for talent in talents:
                self.content_tree.insert("", tk.END, values=(
                    talent.name,
                    "Talent",
                    talent.talent_type.value,
                    str(talent.cost) if talent.cost else "-",
                    "Yes" if talent.is_custom else "No"
                ))
                
            # Prestige Talents
            prestige_tier = self.prestige_tier_var.get()
            if prestige_tier == "All":
                prestige_talents = self.db.get_all_prestige_talents()
            else:
                prestige_talents = self.db.get_prestige_talents_by_tier(int(prestige_tier))
                
            for talent in prestige_talents:
                self.content_tree.insert("", tk.END, values=(
                    talent.name,
                    "Prestige",
                    f"Tier {talent.tier}",
                    str(talent.cost) if talent.cost else "-",
                    "Yes" if talent.is_custom else "No"
                ))
                
        except Exception as e:
            self.show_status(f"Error refreshing content: {e}")
            
    def refresh_custom_list(self):
        """Refresh the custom content list"""
        # Clear existing items
        for item in self.custom_tree.get_children():
            self.custom_tree.delete(item)
            
        try:
            # Add custom skills
            custom_skills = [s for s in self.db.get_all_skills() if s.is_custom]
            for skill in custom_skills:
                self.custom_tree.insert("", tk.END, values=(
                    skill.name,
                    "Skill",
                    skill.cost_formula or "-"
                ))
                
            # Add custom talents
            custom_talents = [t for t in self.db.get_all_talents() if t.is_custom]
            for talent in custom_talents:
                self.custom_tree.insert("", tk.END, values=(
                    talent.name,
                    "Talent",
                    str(talent.cost) if talent.cost else "-"
                ))
                
            # Add custom prestige talents
            custom_prestige = [p for p in self.db.get_all_prestige_talents() if p.is_custom]
            for talent in custom_prestige:
                self.custom_tree.insert("", tk.END, values=(
                    talent.name,
                    "Prestige",
                    str(talent.cost) if talent.cost else "-"
                ))
                
        except Exception as e:
            self.show_status(f"Error refreshing custom list: {e}")
            
    def on_content_selected(self, event=None):
        """Handle content selection in the treeview"""
        selection = self.content_tree.selection()
        if not selection:
            return
            
        try:
            item = self.content_tree.item(selection[0])
            values = item['values']
            content_name = values[0]
            content_type = values[1]
            
            details = f"Name: {content_name}\n"
            details += f"Type: {content_type}\n"
            
            if content_type == "Skill":
                skill = self.db.get_skill_by_name(content_name)
                if skill:
                    details += f"Category: {skill.category.value}\n"
                    details += f"Attributes: {skill.attribute_links}\n"
                    details += f"Max Rating: {skill.max_rating}\n"
                    details += f"Cost Formula: {skill.cost_formula}\n"
                    details += f"Custom Content: {'Yes' if skill.is_custom else 'No'}\n\n"
                    details += f"Description:\n{skill.description}"
                    
            elif content_type == "Talent":
                talents = self.db.get_all_talents()
                talent = next((t for t in talents if t.name == content_name), None)
                if talent:
                    details += f"Talent Type: {talent.talent_type.value}\n"
                    details += f"Cost: {talent.cost} XP\n"
                    details += f"Culture: {talent.culture or 'Any'}\n"
                    details += f"Custom Content: {'Yes' if talent.is_custom else 'No'}\n\n"
                    details += f"Prerequisites: {talent.prerequisites}\n\n"
                    details += f"Description:\n{talent.description}"
                    
            elif content_type == "Prestige":
                talents = self.db.get_all_prestige_talents()
                talent = next((t for t in talents if t.name == content_name), None)
                if talent:
                    details += f"Tier: {talent.tier}\n"
                    details += f"Cost: {talent.cost} XP\n"
                    details += f"Culture: {talent.culture or 'Any'}\n"
                    details += f"Custom Content: {'Yes' if talent.is_custom else 'No'}\n\n"
                    details += f"Prerequisites: {talent.prerequisites}\n\n"
                    details += f"Description:\n{talent.description}"
                    
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(1.0, details)
            
        except Exception as e:
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(1.0, f"Error loading details: {e}")
            
    def export_all_json(self):
        """Export all content to JSON"""
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Export All Content"
            )
            
            if filepath:
                data = {
                    "skills": [skill.__dict__ for skill in self.db.get_all_skills()],
                    "talents": [talent.__dict__ for talent in self.db.get_all_talents()],
                    "prestige_talents": [talent.__dict__ for talent in self.db.get_all_prestige_talents()]
                }
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, default=str)
                    
                self.show_status(f"Successfully exported ALL content to:\n{filepath}")
                messagebox.showinfo("Success", "All content exported successfully!")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export content: {str(e)}")
            
    def export_custom_json(self):
        """Export only custom content for players"""
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Export Custom Content for Players"
            )
            
            if filepath:
                if self.db.export_to_json(filepath):
                    self.show_status(f"Successfully exported CUSTOM content for players to:\n{filepath}")
                    messagebox.showinfo("Success", "Custom content exported successfully for players!")
                else:
                    messagebox.showerror("Export Error", "Failed to export custom content")
                    
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export custom content: {str(e)}")
            
    def import_json(self):
        """Import content from JSON"""
        try:
            filepath = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Import Content from JSON"
            )
            
            if filepath:
                results = self.db.import_from_json(filepath)
                self.show_import_results(results, "JSON")
                self.refresh_data()
                
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import content: {str(e)}")
            
    def export_all_csv(self):
        """Export all content to CSV"""
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension="",
                filetypes=[("CSV files", "*"), ("All files", "*.*")],
                title="Select base filename for CSV export (no extension)"
            )
            
            if filepath:
                # Remove extension if provided
                if "." in os.path.basename(filepath):
                    filepath = os.path.splitext(filepath)[0]
                    
                if self.db.export_to_csv(filepath):
                    self.show_status(f"Successfully exported ALL content to CSV files with base name:\n{filepath}")
                    messagebox.showinfo("Success", "All content exported successfully to CSV!")
                else:
                    messagebox.showerror("Export Error", "Failed to export content to CSV")
                    
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export content to CSV: {str(e)}")
            
    def import_csv(self):
        """Import content from CSV files"""
        try:
            directory = filedialog.askdirectory(title="Select Directory with CSV Files")
            
            if directory:
                results = self.db.import_from_csv(directory)
                self.show_import_results(results, "CSV")
                self.refresh_data()
                
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import content: {str(e)}")

