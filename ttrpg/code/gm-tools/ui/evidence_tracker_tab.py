# ui/evidence_tracker_tab.py
import tkinter as tk
from tkinter import ttk

class EvidenceTrackerTab:
    def __init__(self, parent):
        self.parent = parent
        self.evidence_items = []  # List of evidence dictionaries
        self.create_ui()
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Evidence Tracker", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Add Evidence Section
        add_frame = ttk.LabelFrame(self.parent, text="Add Evidence", padding="10")
        add_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(add_frame, text="Description:").grid(row=0, column=0, sticky="w", padx=5)
        self.desc_entry = ttk.Entry(add_frame, width=30)
        self.desc_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(add_frame, text="Type:").grid(row=0, column=2, sticky="w", padx=5)
        self.type_var = tk.StringVar(value="Immaculate")
        type_combo = ttk.Combobox(add_frame, textvariable=self.type_var, 
                                 values=["Immaculate", "Scorched"], width=12, state="readonly")
        type_combo.grid(row=0, column=3, padx=5)
        
        ttk.Button(add_frame, text="Add Evidence", command=self.add_evidence).grid(row=0, column=4, padx=10)
        
        # Evidence Controls
        control_frame = ttk.Frame(self.parent)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(control_frame, text="Clear All Evidence", command=self.clear_evidence).pack(side="left", padx=5)
        
        # Evidence Summary
        summary_frame = ttk.LabelFrame(self.parent, text="Evidence Summary", padding="10")
        summary_frame.pack(fill="x", padx=20, pady=10)
        
        self.summary_label = ttk.Label(summary_frame, text="", font=("Arial", 12))
        self.summary_label.pack()
        
        # Evidence Display
        self.evidence_frame = ttk.Frame(self.parent)
        self.evidence_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Evidence Info
        info_frame = ttk.LabelFrame(self.parent, text="Evidence Information", padding="10")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
Evidence Types:
• Immaculate: Clean, uncontested evidence that strengthens your position
• Scorched: Evidence obtained through questionable means or that has negative consequences

Effects on Finale:
• Immaculate evidence can be "Immaculate defended" for Mandate advancement
• Scorched evidence can become "Scorched" for Crisis advancement
• Mix of both creates nuanced finale outcomes

Usage:
• Track evidence collected during investigations
• Note how evidence was obtained (affects type)
• Use for finale preparation and positioning
        """.strip()
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left")
        info_label.pack()
        
        self.refresh_display()
        
    def add_evidence(self):
        description = self.desc_entry.get().strip()
        if description:
            evidence = {
                "description": description,
                "type": self.type_var.get(),
                "added": len(self.evidence_items) + 1
            }
            self.evidence_items.append(evidence)
            self.desc_entry.delete(0, tk.END)
            self.refresh_display()
            
    def clear_evidence(self):
        self.evidence_items = []
        self.refresh_display()
        
    def remove_evidence(self, index):
        if 0 <= index < len(self.evidence_items):
            del self.evidence_items[index]
            self.refresh_display()
            
    def toggle_evidence_type(self, index):
        if 0 <= index < len(self.evidence_items):
            current_type = self.evidence_items[index]["type"]
            new_type = "Scorched" if current_type == "Immaculate" else "Immaculate"
            self.evidence_items[index]["type"] = new_type
            self.refresh_display()
            
    def refresh_display(self):
        # Clear existing widgets
        for widget in self.evidence_frame.winfo_children():
            widget.destroy()
            
        # Update summary
        immaculate_count = sum(1 for e in self.evidence_items if e["type"] == "Immaculate")
        scorched_count = sum(1 for e in self.evidence_items if e["type"] == "Scorched")
        total_count = len(self.evidence_items)
        
        summary_text = f"Total Evidence: {total_count} | Immaculate: {immaculate_count} | Scorched: {scorched_count}"
        self.summary_label.config(text=summary_text)
        
        if not self.evidence_items:
            ttk.Label(self.evidence_frame, text="No evidence added").pack(pady=20)
            return
            
        # Create evidence items
        for i, evidence in enumerate(self.evidence_items):
            evidence_frame = ttk.Frame(self.evidence_frame, relief="solid", borderwidth=1)
            evidence_frame.pack(fill="x", pady=2, padx=5)
            
            # Type indicator
            type_color = "green" if evidence["type"] == "Immaculate" else "red"
            type_label = ttk.Label(evidence_frame, text=evidence["type"], 
                                 foreground=type_color, font=("Arial", 10, "bold"), width=12)
            type_label.pack(side="left", padx=10, pady=5)
            
            # Description
            desc_label = ttk.Label(evidence_frame, text=evidence["description"], wraplength=400)
            desc_label.pack(side="left", padx=10, pady=5, fill="x", expand=True)
            
            # Controls
            btn_frame = ttk.Frame(evidence_frame)
            btn_frame.pack(side="right", padx=10)
            
            ttk.Button(btn_frame, text="Toggle", command=lambda idx=i: self.toggle_evidence_type(idx)).pack(side="left", padx=2)
            ttk.Button(btn_frame, text="Remove", command=lambda idx=i: self.remove_evidence(idx)).pack(side="left", padx=2)
