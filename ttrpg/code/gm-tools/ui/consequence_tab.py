import tkinter as tk
from tkinter import ttk
from data.database import Database
from utils.card_utils import get_unicode_card

class ConsequenceTab:
    def __init__(self, parent):
        self.parent = parent
        self.db = Database()
        self.deck = self.initialize_deck()
        self.discard = []
        self.create_ui()
        
    def initialize_deck(self):
        import random
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = list(range(2, 11)) + ["Jack", "Queen", "King", "Ace"]
        deck = [(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck
        
    def draw_card(self):
        import random
        if not self.deck:
            self.deck = self.discard
            self.discard = []
            random.shuffle(self.deck)
            
        if self.deck:
            card = self.deck.pop()
            self.discard.append(card)
            suit, rank = card
            domain, severity = self.db.get_consequence_meaning(suit, rank)
            unicode_card = get_unicode_card(suit, rank)
            self.result_var.set(f"{unicode_card} ({suit} {rank})")
            self.meaning_var.set(f"Domain: {domain}\nSeverity: {severity}")
            
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Deck of Consequences", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Draw button
        draw_btn = ttk.Button(self.parent, text="Draw Consequence Card", 
                             command=self.draw_card, style="Huge.TButton")
        draw_btn.pack(pady=20)
        
        # Result display
        self.result_var = tk.StringVar()
        self.result_var.set("Click 'Draw Consequence Card' to begin")
        result_label = ttk.Label(self.parent, textvariable=self.result_var, 
                                font=("Arial", 20, "bold"))
        result_label.pack(pady=20)
        
        # Meaning display
        self.meaning_var = tk.StringVar()
        meaning_label = ttk.Label(self.parent, textvariable=self.meaning_var, 
                                 font=("Arial", 18), wraplength=1000, justify="center")
        meaning_label.pack(pady=30)
        
        # Deck info
        deck_info = ttk.Label(self.parent, 
                             text="Suits: ♥ Hearts (Emotional/Social), ♦ Diamonds (Resources), ♣ Clubs (Physical), ♠ Spades (Mystical/Narrative)\n" +
                                  "Ranks: 2-5 (Minor), 6-10 (Moderate), J/Q/K (Severe), A (Catastrophic)",
                             font=("Arial", 16), wraplength=1000)
        deck_info.pack(pady=20, side=tk.BOTTOM)
