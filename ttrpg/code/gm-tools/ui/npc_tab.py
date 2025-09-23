import tkinter as tk
from tkinter import ttk
import random
from data.database import Database
from utils.card_utils import get_unicode_card

class NPCTab:
    def __init__(self, parent):
        self.parent = parent
        self.db = Database()
        self.decks = self.initialize_decks()
        self.discards = {category: [] for category in self.decks}
        self.create_ui()
        
    def initialize_decks(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = list(range(2, 11)) + ["Jack", "Queen", "King", "Ace"]
        
        return {
            "Ambition": [(suit, rank) for suit, rank in [(s, r) for s in ["Hearts"] for r in ranks]],
            "Beliefs": [(suit, rank) for suit, rank in [(s, r) for s in ["Clubs"] for r in ranks]],
            "Personality": [(suit, rank) for suit, rank in [(s, r) for s in ["Diamonds"] for r in ranks]],
            "Twist": [(suit, rank) for suit, rank in [(s, r) for s in ["Spades"] for r in ranks]]
        }
        
    def draw_cards(self):
        cards = []
        suit_mapping = {
            "Ambition": "Hearts",
            "Beliefs": "Clubs", 
            "Personality": "Diamonds",
            "Twist": "Spades"
        }
        
        categories = ["Ambition", "Beliefs", "Personality", "Twist"]
        
        for category in categories:
            suit = suit_mapping[category]
            deck = self.decks[category]
            discard = self.discards[category]
            
            available_cards = deck + discard
            
            if not available_cards:
                # Reshuffle
                self.decks[category] = discard
                self.discards[category] = []
                random.shuffle(self.decks[category])
                available_cards = self.decks[category]
            
            if available_cards:
                card = random.choice(available_cards)
                if card in self.decks[category]:
                    self.decks[category].remove(card)
                else:
                    self.discards[category].remove(card)
                self.discards[category].append(card)
                cards.append((category, card))
        
        if len(cards) == 4:
            self.display_npc_info(cards)
            
    def display_npc_info(self, cards):
        # Get descriptors
        ambition_desc, ambition_hook = self.db.get_npc_descriptor("Ambition", cards[0][1][0], cards[0][1][1])
        beliefs_desc, beliefs_hook = self.db.get_npc_descriptor("Beliefs", cards[1][1][0], cards[1][1][1])
        personality_desc, personality_hook = self.db.get_npc_descriptor("Personality", cards[2][1][0], cards[2][1][1])
        twist_desc, twist_hook = self.db.get_npc_descriptor("Twist", cards[3][1][0], cards[3][1][1])
        
        # Unicode cards
        ambition_unicode = get_unicode_card(cards[0][1][0], cards[0][1][1])
        beliefs_unicode = get_unicode_card(cards[1][1][0], cards[1][1][1])
        personality_unicode = get_unicode_card(cards[2][1][0], cards[2][1][1])
        twist_unicode = get_unicode_card(cards[3][1][0], cards[3][1][1])
        
        # Update display
        self.ambition_var.set(f"{ambition_unicode} Ambition: {ambition_desc}")
        self.beliefs_var.set(f"{beliefs_unicode} Beliefs: {beliefs_desc}")
        self.personality_var.set(f"{personality_unicode} Personality: {personality_desc}")
        self.twist_var.set(f"{twist_unicode} Twist: {twist_desc}")
        
        # Full description
        description = f"{ambition_unicode} Ambition: {ambition_desc}\n"
        if ambition_hook:
            description += f"  ↳ Hook: {ambition_hook}\n"
        
        description += f"\n{beliefs_unicode} Beliefs: {beliefs_desc}\n"
        if beliefs_hook:
            description += f"  ↳ Hook: {beliefs_hook}\n"
        
        description += f"\n{personality_unicode} Personality: {personality_desc}\n"
        if personality_hook:
            description += f"  ↳ Hook: {personality_hook}\n"
        
        description += f"\n{twist_unicode} Twist: {twist_desc}\n"
        if twist_hook:
            description += f"  ↳ Hook: {twist_hook}\n"
        
        self.description_text.config(state=tk.NORMAL)
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(tk.END, description)
        self.description_text.config(state=tk.DISABLED)
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="NPC Motive Generator", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Draw button
        draw_btn = ttk.Button(self.parent, text="Generate NPC Motives", 
                             command=self.draw_cards, style="Huge.TButton")
        draw_btn.pack(pady=20)
        
        # Card displays
        self.ambition_var = tk.StringVar()
        ambition_label = ttk.Label(self.parent, textvariable=self.ambition_var, font=("Arial", 18))
        ambition_label.pack(pady=12, anchor="w", padx=40)
        
        self.beliefs_var = tk.StringVar()
        beliefs_label = ttk.Label(self.parent, textvariable=self.beliefs_var, font=("Arial", 18))
        beliefs_label.pack(pady=12, anchor="w", padx=40)
        
        self.personality_var = tk.StringVar()
        personality_label = ttk.Label(self.parent, textvariable=self.personality_var, font=("Arial", 18))
        personality_label.pack(pady=12, anchor="w", padx=40)
        
        self.twist_var = tk.StringVar()
        twist_label = ttk.Label(self.parent, textvariable=self.twist_var, font=("Arial", 18))
        twist_label.pack(pady=12, anchor="w", padx=40)
        
        # Description
        ttk.Label(self.parent, text="Full NPC Description:", font=("Arial", 20, "bold")).pack(pady=(30,15))
        self.description_text = tk.Text(self.parent, height=18, width=95, wrap=tk.WORD, 
                                       font=("Arial", 16), bg="#f0f0f0", fg="#000000", 
                                       padx=15, pady=15, relief="solid", bd=1)
        self.description_text.pack(pady=20, padx=40)
        self.description_text.config(state=tk.DISABLED)
