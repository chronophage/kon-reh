# player_tools/ui/character_manager.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

class CharacterManager:
    def __init__(self, parent, character_data):
        self.parent = parent
        self.character_data = character_data
        self.frame = ttk.Frame(parent)
        
        # Use shared/data/characters directory
        self.characters_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'shared', 'data', 'characters')
        os.makedirs(self.characters_dir, exist_ok=True)
        
        # Character Selection
        self.selection_frame = ttk.LabelFrame(self.frame, text="Character Selection", padding="10")
        self.selection_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        ttk.Label(self.selection_frame, text="Select Character:").grid(row=0, column=0, sticky=tk.W)
        self.character_var = tk.StringVar()
        self.character_combo = ttk.Combobox(self.selection_frame, textvariable=self.character_var, width=25)
        self.character_combo.grid(row=0, column=1, padx=(5, 0))
        self.character_combo.bind("<<ComboboxSelected>>", self.on_character_selected)
        
        self.refresh_btn = ttk.Button(self.selection_frame, text="Refresh", command=self.refresh_characters)
        self.refresh_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Character Actions
        self.actions_frame = ttk.LabelFrame(self.frame, text="Character Actions", padding="10")
        self.actions_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.new_btn = ttk.Button(self.actions_frame, text="New Character", command=self.new_character)
        self.new_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.save_btn = ttk.Button(self.actions_frame, text="Save Character", command=self.save_character)
        self.save_btn.grid(row=0, column=1, padx=(0, 5))
        
        self.load_btn = ttk.Button(self.actions_frame, text="Load Character", command=self.load_character)
        self.load_btn.grid(row=0, column=2, padx=(0, 5))
        
        self.delete_btn = ttk.Button(self.actions_frame, text="Delete Character", command=self.delete_character)
        self.delete_btn.grid(row=0, column=3, padx=(0, 5))
        
        # Character Details
        self.details_frame = ttk.LabelFrame(self.frame, text="Character Details", padding="10")
        self.details_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Basic Info
        ttk.Label(self.details_frame, text="Character Name:").grid(row=0, column=0, sticky=tk.W)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.details_frame, textvariable=self.name_var, width=25)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(self.details_frame, text="Archetype:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.archetype_var = tk.StringVar()
        self.archetype_combo = ttk.Combobox(self.details_frame, textvariable=self.archetype_var,
                                           values=["Solo", "Mixed", "Mastermind"], width=15)
        self.archetype_combo.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        # XP and Stats
        ttk.Label(self.details_frame, text="Total XP:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.xp_var = tk.StringVar(value="0")
        self.xp_entry = ttk.Entry(self.details_frame, textvariable=self.xp_var, width=10)
        self.xp_entry.grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        # Attributes
        attr_frame = ttk.LabelFrame(self.details_frame, text="Attributes", padding="5")
        attr_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.attributes = {}
        attr_names = ["Body", "Wits", "Spirit", "Presence"]
        for i, attr in enumerate(attr_names):
            ttk.Label(attr_frame, text=f"{attr}:").grid(row=i, column=0, sticky=tk.W)
            var = tk.StringVar(value="2")
            self.attributes[attr] = var
            entry = ttk.Entry(attr_frame, textvariable=var, width=5)
            entry.grid(row=i, column=1, sticky=tk.W, padx=(5, 0))
            
        # Skills
        skills_frame = ttk.LabelFrame(self.details_frame, text="Skills", padding="5")
        skills_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.skills = {}
        skill_names = ["Melee", "Ranged", "Athletics", "Arcana", 
                      "Diplomacy", "Stealth", "Deception", "Survival",
                      "Command", "Craft", "Performance", "Lore"]
        for i, skill in enumerate(skill_names):
            row = i // 3
            col = i % 3
            ttk.Label(skills_frame, text=f"{skill}:").grid(row=row, column=col*2, sticky=tk.W)
            var = tk.StringVar(value="0")
            self.skills[skill] = var
            entry = ttk.Entry(skills_frame, textvariable=var, width=5)
            entry.grid(row=row, column=col*2+1, sticky=tk.W, padx=(5, 0))
            
        # Initialize character list
        self.refresh_characters()
        
    def refresh_characters(self):
        character_files = [f for f in os.listdir(self.characters_dir) if f.endswith(".json")]
        character_names = [f[:-5] for f in character_files]  # Remove .json extension
        
        self.character_combo['values'] = character_names
        if character_names:
            self.character_var.set(character_names[0])
            
    def on_character_selected(self, event=None):
        character_name = self.character_var.get()
        if character_name:
            self.load_character_data(character_name)
            
    def load_character_data(self, character_name):
        try:
            with open(os.path.join(self.characters_dir, f"{character_name}.json"), "r") as f:
                data = json.load(f)
                
            self.name_var.set(data.get("name", ""))
            self.archetype_var.set(data.get("archetype", ""))
            self.xp_var.set(data.get("xp", "0"))
            
            # Load attributes
            for attr, var in self.attributes.items():
                var.set(str(data.get("attributes", {}).get(attr, "2")))
                
            # Load skills
            for skill, var in self.skills.items():
                var.set(str(data.get("skills", {}).get(skill, "0")))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load character: {str(e)}")
            
    def new_character(self):
        # Clear all fields
        self.name_var.set("")
        self.archetype_var.set("")
        self.xp_var.set("0")
        
        # Set default attributes
        for var in self.attributes.values():
            var.set("2")
            
        # Set default skills
        for var in self.skills.values():
            var.set("0")
            
        self.character_var.set("")
        
    def save_character(self):
        character_name = self.name_var.get().strip()
        if not character_name:
            messagebox.showwarning("No Name", "Please enter a character name")
            return
            
        # Prepare character data
        data = {
            "name": character_name,
            "archetype": self.archetype_var.get(),
            "xp": self.xp_var.get(),
            "attributes": {attr: int(var.get()) for attr, var in self.attributes.items()},
            "skills": {skill: int(var.get()) for skill, var in self.skills.items()}
        }
        
        # Save to file
        try:
            with open(os.path.join(self.characters_dir, f"{character_name}.json"), "w") as f:
                json.dump(data, f, indent=2)
                
            messagebox.showinfo("Success", f"Character '{character_name}' saved successfully!")
            self.refresh_characters()
            self.character_var.set(character_name)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save character: {str(e)}")
            
    def load_character(self):
        filename = filedialog.askopenfilename(
            initialdir=self.characters_dir,
            title="Select Character File",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        
        if filename:
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
                    
                # Update UI with loaded data
                self.name_var.set(data.get("name", ""))
                self.archetype_var.set(data.get("archetype", ""))
                self.xp_var.set(data.get("xp", "0"))
                
                # Load attributes
                for attr, var in self.attributes.items():
                    var.set(str(data.get("attributes", {}).get(attr, "2")))
                    
                # Load skills
                for skill, var in self.skills.items():
                    var.set(str(data.get("skills", {}).get(skill, "0")))
                    
                # Update character selection
                character_name = data.get("name", "")
                self.character_var.set(character_name)
                
                messagebox.showinfo("Success", f"Character '{character_name}' loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load character: {str(e)}")
                
    def delete_character(self):
        character_name = self.character_var.get()
        if not character_name:
            messagebox.showwarning("No Selection", "Please select a character to delete")
            return
            
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete '{character_name}'?")
        if confirm:
            try:
                os.remove(os.path.join(self.characters_dir, f"{character_name}.json"))
                messagebox.showinfo("Success", f"Character '{character_name}' deleted successfully!")
                self.refresh_characters()
                self.new_character()  # Clear the form
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete character: {str(e)}")
                
    def get_frame(self):
        return self.frame

