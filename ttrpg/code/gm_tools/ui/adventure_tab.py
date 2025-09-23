import tkinter as tk
from tkinter import ttk
import random
from data.database import Database
from utils.card_utils import get_unicode_card

class AdventureTab:
    def __init__(self, parent):
        self.parent = parent
        self.db = Database()
        self.encounter_mode = tk.BooleanVar(value=False)
        self.last_adventure = None
        self.decks = self.initialize_decks()
        self.discards = {category: [] for category in self.decks}
        self.create_ui()
        
    def initialize_decks(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = list(range(2, 11)) + ["Jack", "Queen", "King", "Ace"]
        
        return {
            "Place": [(suit, rank) for suit, rank in [(s, r) for s in ["Spades"] for r in ranks]],
            "People": [(suit, rank) for suit, rank in [(s, r) for s in ["Hearts"] for r in ranks]],
            "Complication": [(suit, rank) for suit, rank in [(s, r) for s in ["Clubs"] for r in ranks]],
            "Reward": [(suit, rank) for suit, rank in [(s, r) for s in ["Diamonds"] for r in ranks]]
        }
        
    def draw_cards(self):
        cards = []
        suit_mapping = {
            "Place": "Spades",
            "People": "Hearts", 
            "Complication": "Clubs",
            "Reward": "Diamonds"
        }
        
        categories = ["Place", "People", "Complication", "Reward"]
        
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
            self.display_adventure_info(cards)
            
    def determine_clock(self, cards):
        if self.encounter_mode.get():
            return "4-segment Clock (Encounter)"
            
        ranks = [card[1][1] for card in cards]
        rank_values = []
        for rank in ranks:
            if rank in ["Jack", "Queen", "King", "Ace"]:
                rank_values.append({"Jack": 11, "Queen": 12, "King": 13, "Ace": 14}[rank])
            else:
                try:
                    rank_values.append(int(rank))
                except ValueError:
                    rank_values.append(0)
                    
        max_rank = max(rank_values) if rank_values else 0
        if max_rank <= 5:
            return "4-segment Clock (Minor)"
        elif max_rank <= 10:
            return "6-segment Clock (Standard)"
        elif max_rank <= 13:
            return "8-segment Clock (Major)"
        else:
            return "10-segment Clock (Pivotal)"
            
    def display_adventure_info(self, cards):
        # Get descriptors
        place_desc = self.db.get_adventure_descriptor("Place", cards[0][1][0], cards[0][1][1])
        people_desc = self.db.get_adventure_descriptor("People", cards[1][1][0], cards[1][1][1])
        complication_desc = self.db.get_adventure_descriptor("Complication", cards[2][1][0], cards[2][1][1])
        reward_desc = self.db.get_adventure_descriptor("Reward", cards[3][1][0], cards[3][1][1])
        
        # Unicode cards
        place_unicode = get_unicode_card(cards[0][1][0], cards[0][1][1])
        people_unicode = get_unicode_card(cards[1][1][0], cards[1][1][1])
        complication_unicode = get_unicode_card(cards[2][1][0], cards[2][1][1])
        reward_unicode = get_unicode_card(cards[3][1][0], cards[3][1][1])
        
        # Update display
        self.place_var.set(f"{place_unicode} Place: {place_desc}")
        self.people_var.set(f"{people_unicode} People: {people_desc}")
        self.complication_var.set(f"{complication_unicode} Complication: {complication_desc}")
        self.reward_var.set(f"{reward_unicode} Reward: {reward_desc}")
        
        clock_size = self.determine_clock(cards)
        self.clock_var.set(f"Clock Size: {clock_size}")
        
        # Store for import
        self.last_adventure = (place_desc, people_desc, complication_desc, reward_desc, clock_size)
        
    def create_ui(self):
        # Title
        title = ttk.Label(self.parent, text="Adventure Generator", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Mode toggle
        mode_frame = ttk.Frame(self.parent)
        mode_frame.pack(pady=10)
        
        encounter_check = ttk.Checkbutton(mode_frame, text="Encounter Mode (4-segment clocks)", 
                                         variable=self.encounter_mode, style="Large.TCheckbutton")
        encounter_check.pack()
        
        # Draw button
        draw_btn = ttk.Button(self.parent, text="Generate Adventure Seed", 
                             command=self.draw_cards, style="Huge.TButton")
        draw_btn.pack(pady=20)
        
        # Card displays
        self.place_var = tk.StringVar()
        place_label = ttk.Label(self.parent, textvariable=self.place_var, font=("Arial", 18))
        place_label.pack(pady=12, anchor="w", padx=40)
        
        self.people_var = tk.StringVar()
        people_label = ttk.Label(self.parent, textvariable=self.people_var, font=("Arial", 18))
        people_label.pack(pady=12, anchor="w", padx=40)
        
        self.complication_var = tk.StringVar()
        complication_label = ttk.Label(self.parent, textvariable=self.complication_var, font=("Arial", 18))
        complication_label.pack(pady=12, anchor="w", padx=40)
        
        self.reward_var = tk.StringVar()
        reward_label = ttk.Label(self.parent, textvariable=self.reward_var, font=("Arial", 18))
        reward_label.pack(pady=12, anchor="w", padx=40)
        
        # Clock size
        self.clock_var = tk.StringVar()
        clock_label = ttk.Label(self.parent, textvariable=self.clock_var, font=("Arial", 20, "bold"))
        clock_label.pack(pady=25)
        
        # Instructions
        instructions = ttk.Label(self.parent, 
                                text="♠ Places | ♥ People/Factions | ♣ Complications | ♦ Rewards/Leverage",
                                font=("Arial", 16), wraplength=1000)
        instructions.pack(pady=25, side=tk.BOTTOM)
