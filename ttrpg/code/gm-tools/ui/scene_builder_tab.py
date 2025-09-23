# ui/scene_builder_tab.py
import tkinter as tk
from tkinter import ttk

class SceneBuilderTab:
    def __init__(self, parent):
        self.parent = parent
        self.scenes = []  # List of scene dictionaries
        self.active_scene = None
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Scene Builder & Tracker", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Main Notebook for different sections
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scene Builder Tab
        self.builder_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.builder_frame, text="Build Scene")
        self.create_builder_ui()
        
        # Active Scenes Tab
        self.active_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.active_frame, text="Active Scenes")
        self.create_active_scenes_ui()
        
        # Scene Templates Tab
        self.templates_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.templates_frame, text="Templates")
        self.create_templates_ui()
        
        # Scene Info
        info_frame = ttk.LabelFrame(self.parent, text="Scene Building Principles", padding="10")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
Scene Building in Fate's Edge:
• Set clear stakes: What changes if this goes right/wrong?
• Establish position: Controlled (advantage), Risky (standard), Dangerous (disadvantage)
• Define complications: What could go wrong beyond simple failure?
• Identify rails: Social (Crowd/Sanctity/Curfew) and Kinetic (Hunt/Escape/Hazard)
• Consider player archetypes: How does this scene engage Solos, Mixed, and Masterminds?

Position Effects:
• Controlled: +1 die on all rolls
• Risky: Standard positioning
• Dangerous: -1 die on all rolls

Stakes Questions:
• If this goes right, what changes? (Position, time, access, consent)
• If this goes wrong, what bites back? (Noise, harm, debt, clocks)

Rail Types:
• Social: Crowd (mob mentality), Sanctity (ritual pressure), Curfew (time constraints)
• Kinetic: Hunt (pursuit), Escape (evasion), Hazard (environmental danger)
        """.strip()
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack()
        
    def create_builder_ui(self):
        # Scene Details
        details_frame = ttk.LabelFrame(self.builder_frame, text="Scene Details", padding="15")
        details_frame.pack(fill="x", padx=10, pady=10)
        
        # Scene Name
        name_frame = ttk.Frame(details_frame)
        name_frame.pack(fill="x", pady=5)
        ttk.Label(name_frame, text="Scene Name:").pack(side="left")
        self.scene_name_entry = ttk.Entry(name_frame, width=30)
        self.scene_name_entry.pack(side="left", padx=10)
        
        # Scene Type
        type_frame = ttk.Frame(details_frame)
        type_frame.pack(fill="x", pady=5)
        ttk.Label(type_frame, text="Scene Type:").pack(side="left")
        self.scene_type_var = tk.StringVar(value="Exploration")
        type_combo = ttk.Combobox(type_frame, textvariable=self.scene_type_var,
                                values=["Exploration", "Social", "Combat", "Intrigue", "Mystical", "Downtime"],
                                width=15, state="readonly")
        type_combo.pack(side="left", padx=10)
        
        # Position
        pos_frame = ttk.Frame(details_frame)
        pos_frame.pack(fill="x", pady=5)
        ttk.Label(pos_frame, text="Starting Position:").pack(side="left")
        self.position_var = tk.StringVar(value="Risky")
        pos_combo = ttk.Combobox(pos_frame, textvariable=self.position_var,
                               values=["Controlled", "Risky", "Dangerous"],
                               width=12, state="readonly")
        pos_combo.pack(side="left", padx=10)
        
        # Stakes Section
        stakes_frame = ttk.LabelFrame(self.builder_frame, text="Stakes", padding="15")
        stakes_frame.pack(fill="x", padx=10, pady=10)
        
        # Success Stakes
        success_frame = ttk.Frame(stakes_frame)
        success_frame.pack(fill="x", pady=5)
        ttk.Label(success_frame, text="If Successful:").pack(anchor="w")
        self.success_text = tk.Text(success_frame, height=3, width=70)
        self.success_text.pack(fill="x", pady=5)
        
        # Failure Complications
        failure_frame = ttk.Frame(stakes_frame)
        failure_frame.pack(fill="x", pady=5)
        ttk.Label(failure_frame, text="If Failed:").pack(anchor="w")
        self.failure_text = tk.Text(failure_frame, height=3, width=70)
        self.failure_text.pack(fill="x", pady=5)
        
        # Rails Section
        rails_frame = ttk.LabelFrame(self.builder_frame, text="Scene Rails", padding="15")
        rails_frame.pack(fill="x", padx=10, pady=10)
        
        # Social Rail
        social_frame = ttk.Frame(rails_frame)
        social_frame.pack(fill="x", pady=5)
        ttk.Label(social_frame, text="Social Rail:").pack(side="left")
        self.social_rail_var = tk.StringVar(value="None")
        social_combo = ttk.Combobox(social_frame, textvariable=self.social_rail_var,
                                  values=["None", "Crowd", "Sanctity", "Curfew"],
                                  width=12, state="readonly")
        social_combo.pack(side="left", padx=10)
        
        # Kinetic Rail
        kinetic_frame = ttk.Frame(rails_frame)
        kinetic_frame.pack(fill="x", pady=5)
        ttk.Label(kinetic_frame, text="Kinetic Rail:").pack(side="left")
        self.kinetic_rail_var = tk.StringVar(value="None")
        kinetic_combo = ttk.Combobox(kinetic_frame, textvariable=self.kinetic_rail_var,
                                   values=["None", "Hunt", "Escape", "Hazard"],
                                   width=12, state="readonly")
        kinetic_combo.pack(side="left", padx=10)
        
        # Notes Section
        notes_frame = ttk.LabelFrame(self.builder_frame, text="Notes", padding="15")
        notes_frame.pack(fill="x", padx=10, pady=10)
        
        self.notes_text = tk.Text(notes_frame, height=4, width=70)
        self.notes_text.pack(fill="x")
        
        # Action Buttons
        action_frame = ttk.Frame(self.builder_frame)
        action_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(action_frame, text="Save Scene", command=self.save_scene).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Clear Form", command=self.clear_form).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Load Template", command=self.load_template_dialog).pack(side="left", padx=5)
        
    def create_active_scenes_ui(self):
        # Scene Controls
        control_frame = ttk.Frame(self.active_frame)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(control_frame, text="Activate Scene", command=self.activate_scene_dialog).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Deactivate Scene", command=self.deactivate_scene).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Clear All Scenes", command=self.clear_all_scenes).pack(side="left", padx=5)
        
        # Active Scene Display
        self.active_display_frame = ttk.Frame(self.active_frame)
        self.active_display_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scenes List
        self.scenes_list_frame = ttk.Frame(self.active_frame)
        self.scenes_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_scenes_display()
        
    def create_templates_ui(self):
        # Template Controls
        template_control_frame = ttk.Frame(self.templates_frame)
        template_control_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(template_control_frame, text="Save as Template", command=self.save_template).pack(side="left", padx=5)
        ttk.Button(template_control_frame, text="Delete Template", command=self.delete_template_dialog).pack(side="left", padx=5)
        
        # Templates List
        templates_list_frame = ttk.LabelFrame(self.templates_frame, text="Saved Templates", padding="10")
        templates_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sample templates
        sample_templates = [
            {
                "name": "Noble Parlor Intrigue",
                "type": "Social",
                "position": "Risky",
                "success": "Gain favor with the host, access to private information",
                "failure": "Offend a guest, create enemy, rumors spread",
                "social_rail": "Crowd",
                "kinetic_rail": "None",
                "notes": "High society event with multiple factions present"
            },
            {
                "name": "Dungeon Escape",
                "type": "Exploration",
                "position": "Dangerous",
                "success": "Find exit, avoid/defeat guards, secure treasure",
                "failure": "Alert more guards, trigger traps, lose equipment",
                "social_rail": "None",
                "kinetic_rail": "Escape",
                "notes": "Time pressure, multiple exits, hidden dangers"
            },
            {
                "name": "Street Chase",
                "type": "Combat",
                "position": "Risky",
                "success": "Lose pursuers, reach safe house, gather intelligence",
                "failure": "Cornered, separated from allies, evidence lost",
                "social_rail": "Crowd",
                "kinetic_rail": "Hunt",
                "notes": "Urban environment, civilian bystanders, multiple routes"
            }
        ]
        
        # Display templates
        for i, template in enumerate(sample_templates):
            template_frame = ttk.LabelFrame(templates_list_frame, text=template["name"], padding="10")
            template_frame.pack(fill="x", pady=5, padx=5)
            
            # Template details
            details_frame = ttk.Frame(template_frame)
            details_frame.pack(fill="x", pady=2)
            
            ttk.Label(details_frame, text=f"Type: {template['type']}").pack(side="left", padx=10)
            ttk.Label(details_frame, text=f"Position: {template['position']}").pack(side="left", padx=10)
            ttk.Label(details_frame, text=f"Rails: {template['social_rail']}/{template['kinetic_rail']}").pack(side="left", padx=10)
            
            # Template controls
            control_frame = ttk.Frame(template_frame)
            control_frame.pack(fill="x", pady=5)
            
            ttk.Button(control_frame, text="Load", 
                      command=lambda t=template: self.load_template(t)).pack(side="left", padx=5)
            ttk.Button(control_frame, text="Delete", 
                      command=lambda idx=i: self.delete_template(idx)).pack(side="left", padx=5)
            
    def save_scene(self):
        name = self.scene_name_entry.get().strip()
        if name:
            scene = {
                "name": name,
                "type": self.scene_type_var.get(),
                "position": self.position_var.get(),
                "success": self.success_text.get("1.0", tk.END).strip(),
                "failure": self.failure_text.get("1.0", tk.END).strip(),
                "social_rail": self.social_rail_var.get(),
                "kinetic_rail": self.kinetic_rail_var.get(),
                "notes": self.notes_text.get("1.0", tk.END).strip()
            }
            self.scenes.append(scene)
            self.refresh_scenes_display()
            self.clear_form()
            
    def clear_form(self):
        self.scene_name_entry.delete(0, tk.END)
        self.scene_type_var.set("Exploration")
        self.position_var.set("Risky")
        self.success_text.delete("1.0", tk.END)
        self.failure_text.delete("1.0", tk.END)
        self.social_rail_var.set("None")
        self.kinetic_rail_var.set("None")
        self.notes_text.delete("1.0", tk.END)
        
    def load_template(self, template):
        self.scene_name_entry.delete(0, tk.END)
        self.scene_name_entry.insert(0, template["name"])
        self.scene_type_var.set(template["type"])
        self.position_var.set(template["position"])
        self.success_text.delete("1.0", tk.END)
        self.success_text.insert("1.0", template["success"])
        self.failure_text.delete("1.0", tk.END)
        self.failure_text.insert("1.0", template["failure"])
        self.social_rail_var.set(template["social_rail"])
        self.kinetic_rail_var.set(template["kinetic_rail"])
        self.notes_text.delete("1.0", tk.END)
        self.notes_text.insert("1.0", template["notes"])
        
    def load_template_dialog(self):
        if not self.scenes:
            return
            
        dialog = tk.Toplevel(self.parent)
        dialog.title("Load Scene Template")
        dialog.geometry("400x300")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select Scene to Load:").pack(pady=10)
        
        # Listbox for scenes
        list_frame = ttk.Frame(dialog)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        
        for scene in self.scenes:
            listbox.insert(tk.END, f"{scene['name']} ({scene['type']})")
            
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def load_selected():
            selection = listbox.curselection()
            if selection:
                scene = self.scenes[selection[0]]
                self.load_template(scene)
                dialog.destroy()
                
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Load", command=load_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def save_template(self):
        # This would save the current form as a reusable template
        # For now, we'll just show a message
        dialog = tk.Toplevel(self.parent)
        dialog.title("Save Template")
        dialog.geometry("300x150")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Template Name:").pack(pady=10)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=5)
        name_entry.focus()
        
        def save_and_close():
            name = name_entry.get().strip()
            if name:
                # In a full implementation, this would save to a templates database
                ttk.Label(dialog, text="Template saved!", foreground="green").pack(pady=10)
                dialog.after(1500, dialog.destroy)
            else:
                ttk.Label(dialog, text="Please enter a name", foreground="red").pack()
                
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Save", command=save_and_close).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def delete_template(self, index):
        # Placeholder for template deletion
        pass
        
    def delete_template_dialog(self):
        # Placeholder for template deletion dialog
        pass
        
    def activate_scene_dialog(self):
        if not self.scenes:
            return
            
        dialog = tk.Toplevel(self.parent)
        dialog.title("Activate Scene")
        dialog.geometry("400x300")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select Scene to Activate:").pack(pady=10)
        
        # Listbox for scenes
        list_frame = ttk.Frame(dialog)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        
        for scene in self.scenes:
            listbox.insert(tk.END, f"{scene['name']} ({scene['type']})")
            
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def activate_selected():
            selection = listbox.curselection()
            if selection:
                self.active_scene = self.scenes[selection[0]]
                self.refresh_active_scene_display()
                dialog.destroy()
                
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Activate", command=activate_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)
        
    def deactivate_scene(self):
        self.active_scene = None
        self.refresh_active_scene_display()
        
    def clear_all_scenes(self):
        self.scenes = []
        self.active_scene = None
        self.refresh_scenes_display()
        self.refresh_active_scene_display()
        
    def refresh_scenes_display(self):
        # Clear existing widgets
        for widget in self.scenes_list_frame.winfo_children():
            widget.destroy()
            
        if not self.scenes:
            ttk.Label(self.scenes_list_frame, text="No scenes created").pack(pady=20)
            return
            
        # Create scrollable area
        canvas = tk.Canvas(self.scenes_list_frame)
        scrollbar = ttk.Scrollbar(self.scenes_list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display scenes
        for i, scene in enumerate(self.scenes):
            scene_frame = ttk.LabelFrame(scrollable_frame, text=scene["name"], padding="10")
            scene_frame.pack(fill="x", pady=5, padx=5)
            
            # Scene details
            details_frame = ttk.Frame(scene_frame)
            details_frame.pack(fill="x", pady=2)
            
            ttk.Label(details_frame, text=f"Type: {scene['type']}").pack(side="left", padx=10)
            ttk.Label(details_frame, text=f"Position: {scene['position']}").pack(side="left", padx=10)
            ttk.Label(details_frame, text=f"Rails: {scene['social_rail']}/{scene['kinetic_rail']}").pack(side="left", padx=10)
            
            # Scene controls
            control_frame = ttk.Frame(scene_frame)
            control_frame.pack(fill="x", pady=5)
            
            ttk.Button(control_frame, text="Activate", 
                      command=lambda s=scene: self.activate_scene(s)).pack(side="left", padx=5)
            ttk.Button(control_frame, text="Load", 
                      command=lambda s=scene: self.load_scene(s)).pack(side="left", padx=5)
            ttk.Button(control_frame, text="Delete", 
                      command=lambda idx=i: self.delete_scene(idx)).pack(side="left", padx=5)
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def refresh_active_scene_display(self):
        # Clear existing widgets
        for widget in self.active_display_frame.winfo_children():
            widget.destroy()
            
        if not self.active_scene:
            ttk.Label(self.active_display_frame, text="No active scene", 
                     font=("Arial", 14, "bold")).pack(pady=50)
            return
            
        # Active scene display
        active_frame = ttk.LabelFrame(self.active_display_frame, text="ACTIVE SCENE", padding="15")
        active_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scene header
        header_frame = ttk.Frame(active_frame)
        header_frame.pack(fill="x", pady=5)
        
        ttk.Label(header_frame, text=self.active_scene["name"], 
                 font=("Arial", 16, "bold")).pack(side="left")
        
        position_color = "green" if self.active_scene["position"] == "Controlled" else \
                        "orange" if self.active_scene["position"] == "Risky" else "red"
        ttk.Label(header_frame, text=self.active_scene["position"], 
                 foreground=position_color, font=("Arial", 12, "bold")).pack(side="right")
        
        # Scene details
        details_frame = ttk.Frame(active_frame)
        details_frame.pack(fill="x", pady=10)
        
        ttk.Label(details_frame, text=f"Type: {self.active_scene['type']}").pack(side="left", padx=20)
        ttk.Label(details_frame, text=f"Social Rail: {self.active_scene['social_rail']}").pack(side="left", padx=20)
        ttk.Label(details_frame, text=f"Kinetic Rail: {self.active_scene['kinetic_rail']}").pack(side="left", padx=20)
        
        # Stakes
        stakes_frame = ttk.LabelFrame(active_frame, text="Stakes", padding="10")
        stakes_frame.pack(fill="x", pady=10)
        
        ttk.Label(stakes_frame, text="If Successful:", font=("Arial", 10, "bold")).pack(anchor="w")
        ttk.Label(stakes_frame, text=self.active_scene["success"], wraplength=700).pack(anchor="w", pady=(0,10))
        
        ttk.Label(stakes_frame, text="If Failed:", font=("Arial", 10, "bold")).pack(anchor="w")
        ttk.Label(stakes_frame, text=self.active_scene["failure"], wraplength=700).pack(anchor="w", pady=(0,10))
        
        # Notes
        if self.active_scene["notes"]:
            notes_frame = ttk.LabelFrame(active_frame, text="Notes", padding="10")
            notes_frame.pack(fill="x", pady=10)
            ttk.Label(notes_frame, text=self.active_scene["notes"], wraplength=700).pack(anchor="w")
            
    def activate_scene(self, scene):
        self.active_scene = scene
        self.refresh_active_scene_display()
        
    def load_scene(self, scene):
        self.load_template(scene)
        
    def delete_scene(self, index):
        if 0 <= index < len(self.scenes):
            del self.scenes[index]
            if self.active_scene and self.active_scene == self.scenes[index if index < len(self.scenes) else -1 if self.scenes else None]:
                self.active_scene = None
            self.refresh_scenes_display()
            self.refresh_active_scene_display()
