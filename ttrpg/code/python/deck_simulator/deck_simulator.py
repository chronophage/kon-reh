#!/usr/bin/env python3
"""
Fate's Edge Deck Simulator with Die Roller
Enhanced version with integrated dice rolling and consequence management
"""

import json
import random
import os
from typing import Dict, List, Any, Optional
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import webbrowser

class FateDeckSimulator:
    def __init__(self):
        self.generators = {}
        self.current_deck = []
        self.drawn_cards = []
        self.load_generators()
        
    def load_generators(self):
        """Load all generator JSON files from the generators directory"""
        if not os.path.exists('generators'):
            os.makedirs('generators')
            return
            
        for filename in os.listdir('generators'):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join('generators', filename), 'r') as f:
                        generator_data = json.load(f)
                        generator_name = generator_data.get('name', filename.replace('.json', ''))
                        self.generators[generator_name] = generator_data
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    def save_generator(self, name: str, generator_data: Dict):
        """Save a generator to JSON file"""
        if not os.path.exists('generators'):
            os.makedirs('generators')
            
        filename = f"generators/{name.lower().replace(' ', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(generator_data, f, indent=2)
        
        self.generators[name] = generator_data
    
    def create_deck(self, generator_name: str) -> List[Dict]:
        """Create a 52-card deck from generator data"""
        if generator_name not in self.generators:
            return []
            
        generator = self.generators[generator_name]
        deck = []
        
        # Standard 52-card deck structure
        suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        ranks = list(range(2, 11)) + ['J', 'Q', 'K', 'A']
        
        for suit in suits:
            for rank in ranks:
                card = {
                    'suit': suit,
                    'rank': rank,
                    'color': 'black' if suit in ['Spades', 'Clubs'] else 'red'
                }
                
                # Add generator-specific content
                suit_key = suit.lower().replace(' ', '_')
                if suit_key in generator:
                    options = generator[suit_key]
                    # Find option matching the rank
                    card_content = None
                    for option in options:
                        if option.get('rank') == rank:
                            card_content = option
                            break
                        elif isinstance(option.get('rank'), list) and rank in option.get('rank', []):
                            card_content = option
                            break
                    
                    if card_content:
                        card.update(card_content)
                
                deck.append(card)
        
        return deck
    
    def draw_cards(self, deck: List[Dict], count: int = 4) -> List[Dict]:
        """Draw specified number of cards from deck"""
        if len(deck) < count:
            return []
        
        drawn = random.sample(deck, count)
        return drawn
    
    def get_clock_size(self, cards: List[Dict]) -> int:
        """Determine clock size based on highest rank"""
        rank_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
            'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }
        
        max_rank_value = 0
        for card in cards:
            rank_val = rank_values.get(str(card['rank']), 0)
            if rank_val > max_rank_value:
                max_rank_value = rank_val
        
        # Convert to clock size
        if max_rank_value <= 5:
            return 4  # Minor
        elif max_rank_value <= 10:
            return 6  # Standard
        elif max_rank_value <= 13:
            return 8  # Major
        else:
            return 10  # Pivotal
    
    def get_combo_effects(self, cards: List[Dict]) -> List[str]:
        """Get combo effects from drawn cards"""
        effects = []
        ranks = [str(card['rank']) for card in cards]
        suits = [card['suit'] for card in cards]
        
        # Pair detection
        rank_counts = defaultdict(int)
        for rank in ranks:
            rank_counts[rank] += 1
        
        for rank, count in rank_counts.items():
            if count >= 2:
                effects.append(f"Pair: Recurring motif with a twist ({rank})")
        
        # Run detection (sequential ranks)
        rank_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        numeric_ranks = []
        for rank in ranks:
            if rank in rank_order:
                numeric_ranks.append(rank_order.index(rank))
        
        numeric_ranks.sort()
        if len(numeric_ranks) >= 3:
            consecutive = 1
            for i in range(1, len(numeric_ranks)):
                if numeric_ranks[i] == numeric_ranks[i-1] + 1:
                    consecutive += 1
                else:
                    if consecutive >= 3:
                        effects.append("Run: Momentum—reduce the main Clock by 1 segment")
                        break
                    consecutive = 1
            if consecutive >= 3:
                effects.append("Run: Momentum—reduce the main Clock by 1 segment")
        
        # Flush detection (same suit)
        suit_counts = defaultdict(int)
        for suit in suits:
            suit_counts[suit] += 1
        
        for suit, count in suit_counts.items():
            if count >= 3:
                effects.append(f"Flush: Strongly theme the act toward {suit}")
        
        # Face + Ace detection
        has_face = any(rank in ['J', 'Q', 'K'] for rank in ranks)
        has_ace = 'A' in ranks
        if has_face and has_ace:
            effects.append("Face + Ace: Reveal a hidden patron or power behind the drawn element")
        
        # All same color
        colors = [card['color'] for card in cards]
        if len(set(colors)) == 1:
            effects.append(f"All {colors[0]}: GM gains 1 free Complication Point in that scene")
        
        return effects

class ConsequencesDeck:
    def __init__(self):
        self.create_deck()
    
    def create_deck(self):
        """Create the Deck of Consequences"""
        self.deck = []
        suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
        ranks = list(range(1, 11)) + ['J', 'Q', 'K', 'A']
        
        for suit in suits:
            for rank in ranks:
                card = {
                    'suit': suit,
                    'rank': rank,
                    'color': 'red' if suit in ['Hearts', 'Diamonds'] else 'black'
                }
                
                # Add consequence descriptions
                if suit == 'Hearts':
                    card['type'] = 'Social Fallout'
                    if rank in [1, 2, 3]:
                        card['description'] = 'Minor social embarrassment or awkward moment'
                    elif rank in [4, 5, 6]:
                        card['description'] = 'Moderate social setback, damaged reputation'
                    elif rank in [7, 8, 9]:
                        card['description'] = 'Significant social consequence, public humiliation'
                    elif rank == 10:
                        card['description'] = 'Major social disaster, loss of social standing'
                    elif rank in ['J', 'Q', 'K']:
                        card['description'] = 'Catastrophic social failure, complete ostracization'
                    elif rank == 'A':
                        card['description'] = 'Legendary social disaster, becomes a cautionary tale'
                        
                elif suit == 'Spades':
                    card['type'] = 'Physical Harm/Obstacles'
                    if rank in [1, 2, 3]:
                        card['description'] = 'Minor physical inconvenience or small injury'
                    elif rank in [4, 5, 6]:
                        card['description'] = 'Moderate physical setback, noticeable injury'
                    elif rank in [7, 8, 9]:
                        card['description'] = 'Significant physical harm, major obstacle'
                    elif rank == 10:
                        card['description'] = 'Major physical trauma, severe injury'
                    elif rank in ['J', 'Q', 'K']:
                        card['description'] = 'Catastrophic physical damage, life-threatening'
                    elif rank == 'A':
                        card['description'] = 'Legendary physical catastrophe, permanent disability'
                        
                elif suit == 'Clubs':
                    card['type'] = 'Material Cost'
                    if rank in [1, 2, 3]:
                        card['description'] = 'Minor material loss or expense'
                    elif rank in [4, 5, 6]:
                        card['description'] = 'Moderate material setback, significant expense'
                    elif rank in [7, 8, 9]:
                        card['description'] = 'Significant material loss, major financial impact'
                    elif rank == 10:
                        card['description'] = 'Major material disaster, bankruptcy risk'
                    elif rank in ['J', 'Q', 'K']:
                        card['description'] = 'Catastrophic material failure, total loss'
                    elif rank == 'A':
                        card['description'] = 'Legendary material catastrophe, generational ruin'
                        
                elif suit == 'Diamonds':
                    card['type'] = 'Mystical/Spiritual Disturbance'
                    if rank in [1, 2, 3]:
                        card['description'] = 'Minor mystical anomaly or spiritual unease'
                    elif rank in [4, 5, 6]:
                        card['description'] = 'Moderate mystical setback, supernatural attention'
                    elif rank in [7, 8, 9]:
                        card['description'] = 'Significant mystical disturbance, spiritual threat'
                    elif rank == 10:
                        card['description'] = 'Major mystical catastrophe, supernatural intervention'
                    elif rank in ['J', 'Q', 'K']:
                        card['description'] = 'Catastrophic mystical failure, otherworldly invasion'
                    elif rank == 'A':
                        card['description'] = 'Legendary mystical disaster, reality fracture'
                
                self.deck.append(card)
    
    def draw_cards(self, count: int) -> List[Dict]:
        """Draw specified number of consequence cards"""
        if len(self.deck) < count:
            return []
        
        drawn = random.sample(self.deck, count)
        return drawn

class GeneratorEditor:
    def __init__(self, parent, simulator):
        self.parent = parent
        self.simulator = simulator
        self.generator_data = {
            "name": "",
            "theme": "",
            "special_mechanics": [],
            "spades": [],  # Places
            "hearts": [],  # People & Factions
            "clubs": [],   # Complications/Threats
            "diamonds": [] # Rewards/Leverage
        }
        
    def create_editor_window(self):
        editor_window = tk.Toplevel(self.parent)
        editor_window.title("Generator Editor")
        editor_window.geometry("800x600")
        
        # Main frame
        main_frame = ttk.Frame(editor_window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        editor_window.columnconfigure(0, weight=1)
        editor_window.rowconfigure(0, weight=1)
        
        # Generator info
        info_frame = ttk.LabelFrame(main_frame, text="Generator Information", padding="5")
        info_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)
        
        ttk.Label(info_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.name_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(info_frame, text="Theme:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.theme_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.theme_var, width=30).grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        # Suit editors
        suits = ['spades', 'hearts', 'clubs', 'diamonds']
        suit_labels = ['Places', 'People & Factions', 'Complications/Threats', 'Rewards/Leverage']
        
        self.suit_frames = {}
        self.suit_entries = {}
        
        for i, (suit, label) in enumerate(zip(suits, suit_labels)):
            frame = ttk.LabelFrame(main_frame, text=label, padding="5")
            frame.grid(row=i+1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(1, weight=1)
            main_frame.rowconfigure(i+1, weight=1)
            
            # Add card button
            add_btn = ttk.Button(frame, text="Add Card", command=lambda s=suit: self.add_card(s))
            add_btn.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
            
            # Card list
            list_frame = ttk.Frame(frame)
            list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            list_frame.columnconfigure(0, weight=1)
            list_frame.rowconfigure(0, weight=1)
            
            listbox = tk.Listbox(list_frame, height=6)
            listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
            scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            listbox.configure(yscrollcommand=scrollbar.set)
            
            self.suit_frames[suit] = frame
            self.suit_entries[suit] = listbox
        
        # Save button
        save_btn = ttk.Button(main_frame, text="Save Generator", command=self.save_generator)
        save_btn.grid(row=len(suits)+1, column=0, columnspan=2, pady=(10, 0))
        
        return editor_window
    
    def add_card(self, suit):
        # Simple dialog for adding a card
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Add Card to {suit.title()}")
        dialog.geometry("400x300")
        
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(0, weight=1)
        
        # Rank entry
        ttk.Label(main_frame, text="Rank (2-10, J, Q, K, A):").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        rank_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=rank_var).grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Content entry
        ttk.Label(main_frame, text="Content:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        content_text = ScrolledText(main_frame, height=8, width=40)
        content_text.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(3, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        def save_card():
            rank = rank_var.get().strip()
            content = content_text.get("1.0", tk.END).strip()
            if rank and content:
                card_data = {
                    "rank": rank,
                    "content": content
                }
                self.suit_entries[suit].insert(tk.END, f"{rank}: {content}")
                # Store in generator data
                if suit not in self.generator_data:
                    self.generator_data[suit] = []
                self.generator_data[suit].append(card_data)
            dialog.destroy()
        
        ttk.Button(main_frame, text="Add Card", command=save_card).grid(row=4, column=0)
    
    def save_generator(self):
        name = self.name_var.get().strip()
        theme = self.theme_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Generator name is required")
            return
        
        self.generator_data["name"] = name
        self.generator_data["theme"] = theme
        
        try:
            self.simulator.save_generator(name, self.generator_data)
            messagebox.showinfo("Success", f"Generator '{name}' saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save generator: {e}")

class DieRoller:
    def __init__(self):
        self.consequences_deck = ConsequencesDeck()
        self.last_roll_result = None
    
    def roll_dice(self, dice_count: int, dv: int, is_detailed: bool = False, is_intricate: bool = False) -> Dict:
        """Roll dice and calculate results"""
        if dice_count <= 0:
            return {"error": "Invalid dice count"}
        
        # Roll the dice
        rolls = [random.randint(1, 10) for _ in range(dice_count)]
        
        # Count successes and complications
        successes = sum(1 for roll in rolls if roll >= 6)
        complications = sum(1 for roll in rolls if roll == 1)
        
        # Apply description ladder modifiers
        if is_intricate:
            # Re-roll all 1s and add flourish
            new_rolls = []
            for roll in rolls:
                if roll == 1:
                    new_roll = random.randint(1, 10)
                    new_rolls.append(new_roll)
                    if new_roll >= 6:
                        successes += 1
                    elif new_roll == 1:
                        complications += 1
                else:
                    new_rolls.append(roll)
            rolls = new_rolls
        elif is_detailed:
            # Re-roll one 1
            if 1 in rolls:
                first_one_index = rolls.index(1)
                new_roll = random.randint(1, 10)
                rolls[first_one_index] = new_roll
                if new_roll >= 6:
                    successes += 1
                elif new_roll == 1:
                    complications += 1
        
        # Determine outcome
        if successes >= dv:
            if complications == 0:
                outcome = "Clean Success"
            else:
                outcome = "Success & Cost"
        elif successes > 0:
            outcome = "Partial"
        else:
            outcome = "Miss"
        
        result = {
            "rolls": rolls,
            "successes": successes,
            "complications": complications,
            "dv": dv,
            "outcome": outcome,
            "is_detailed": is_detailed,
            "is_intricate": is_intricate
        }
        
        self.last_roll_result = result
        return result
    
    def reroll_ones(self, current_rolls: List[int], boon_count: int) -> Dict:
        """Reroll 1s at the cost of boons"""
        if boon_count <= 0:
            return {"error": "No boons available"}
        
        rerolled_rolls = current_rolls.copy()
        boons_used = 0
        
        # Reroll 1s, one boon per 1
        for i, roll in enumerate(rerolled_rolls):
            if roll == 1 and boons_used < boon_count:
                new_roll = random.randint(1, 10)
                rerolled_rolls[i] = new_roll
                boons_used += 1
        
        # Recalculate successes and complications
        successes = sum(1 for roll in rerolled_rolls if roll >= 6)
        complications = sum(1 for roll in rerolled_rolls if roll == 1)
        
        return {
            "original_rolls": current_rolls,
            "rerolled_rolls": rerolled_rolls,
            "boons_used": boons_used,
            "successes": successes,
            "complications": complications
        }
    
    def draw_consequences(self, cp_count: int) -> List[Dict]:
        """Draw consequences based on CP count"""
        draw_count = min(cp_count, 3)  # Draw up to min(CP, 3)
        return self.consequences_deck.draw_cards(draw_count)

class FateDeckGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fate's Edge Deck Simulator & Die Roller")
        self.root.geometry("1200x800")
        
        self.simulator = FateDeckSimulator()
        self.die_roller = DieRoller()
        self.current_generator = None
        self.current_deck = []
        self.player_boons = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Campaign Generator tab
        self.generator_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.generator_frame, text="Campaign Generator")
        
        # Die Roller tab
        self.die_roller_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.die_roller_frame, text="Die Roller")
        
        self.setup_generator_ui()
        self.setup_die_roller_ui()
        
    def setup_generator_ui(self):
        # Main menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Generator", command=self.open_generator_editor)
        file_menu.add_command(label="Load Generator Deck", command=self.load_generator_deck)
        file_menu.add_command(label="Refresh Generators", command=self.refresh_generators)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Main frame
        main_frame = ttk.Frame(self.generator_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Generator selection
        gen_frame = ttk.LabelFrame(main_frame, text="Generator Selection", padding="5")
        gen_frame.pack(fill=tk.X, pady=(0, 10))
        gen_frame.columnconfigure(1, weight=1)
        
        ttk.Label(gen_frame, text="Select Generator:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.generator_var = tk.StringVar()
        self.generator_combo = ttk.Combobox(gen_frame, textvariable=self.generator_var, width=30)
        self.generator_combo.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.generator_combo.bind('<<ComboboxSelected>>', self.on_generator_selected)
        
        ttk.Button(gen_frame, text="Refresh", command=self.refresh_generators).grid(row=0, column=2, padx=(5, 0))
        ttk.Button(gen_frame, text="Load Deck", command=self.load_generator_deck).grid(row=0, column=3, padx=(5, 0))
        ttk.Button(gen_frame, text="Create New", command=self.open_generator_editor).grid(row=0, column=4, padx=(5, 0))
        
        # Deck controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(control_frame, text="Create Deck", command=self.create_deck).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Draw 4 Cards", command=self.draw_cards).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Quick Hook (2 Cards)", command=self.quick_hook).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Clear Results", command=self.clear_results).pack(side=tk.LEFT)
        
        # Results area
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="5")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results notebook
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cards tab
        self.cards_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.cards_frame, text="Drawn Cards")
        self.cards_frame.columnconfigure(0, weight=1)
        self.cards_frame.rowconfigure(0, weight=1)
        
        self.cards_text = ScrolledText(self.cards_frame, wrap=tk.WORD)
        self.cards_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Seed tab
        self.seed_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.seed_frame, text="Generated Seed")
        self.seed_frame.columnconfigure(0, weight=1)
        self.seed_frame.rowconfigure(0, weight=1)
        
        self.seed_text = ScrolledText(self.seed_frame, wrap=tk.WORD)
        self.seed_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Combos tab
        self.combos_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.combos_frame, text="Combo Effects")
        self.combos_frame.columnconfigure(0, weight=1)
        self.combos_frame.rowconfigure(0, weight=1)
        
        self.combos_text = ScrolledText(self.combos_frame, wrap=tk.WORD)
        self.combos_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Initialize
        self.refresh_generators()
    
    def setup_die_roller_ui(self):
        main_frame = ttk.Frame(self.die_roller_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Player resources
        resources_frame = ttk.LabelFrame(main_frame, text="Player Resources", padding="5")
        resources_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(resources_frame, text="Boons:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.boons_var = tk.StringVar(value="0")
        ttk.Entry(resources_frame, textvariable=self.boons_var, width=5).grid(row=0, column=1, sticky=tk.W)
        ttk.Button(resources_frame, text="+", command=self.add_boon, width=3).grid(row=0, column=2, padx=(2, 0))
        ttk.Button(resources_frame, text="-", command=self.remove_boon, width=3).grid(row=0, column=3, padx=(2, 0))
        
        # Roll controls
        roll_frame = ttk.LabelFrame(main_frame, text="Die Roll", padding="5")
        roll_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Dice pool
        dice_frame = ttk.Frame(roll_frame)
        dice_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(dice_frame, text="Dice Pool:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.dice_count_var = tk.StringVar(value="4")
        ttk.Entry(dice_frame, textvariable=self.dice_count_var, width=5).grid(row=0, column=1, sticky=tk.W)
        
        # DV
        ttk.Label(dice_frame, text="DV:").grid(row=0, column=2, sticky=tk.W, padx=(10, 5))
        self.dv_var = tk.StringVar(value="2")
        ttk.Entry(dice_frame, textvariable=self.dv_var, width=5).grid(row=0, column=3, sticky=tk.W)
        
        # Description ladder
        ladder_frame = ttk.Frame(roll_frame)
        ladder_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.detailed_var = tk.BooleanVar()
        ttk.Checkbutton(ladder_frame, text="Detailed", variable=self.detailed_var).grid(row=0, column=0, sticky=tk.W)
        
        self.intricate_var = tk.BooleanVar()
        ttk.Checkbutton(ladder_frame, text="Intricate", variable=self.intricate_var).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Roll button
        ttk.Button(roll_frame, text="Roll Dice", command=self.roll_dice).pack(pady=(10, 0))
        
        # Re-roll controls
        reroll_frame = ttk.LabelFrame(main_frame, text="Re-roll Options", padding="5")
        reroll_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(reroll_frame, text="Re-roll 1s (1 Boon per 1)", command=self.reroll_ones).pack()
        ttk.Label(reroll_frame, text="Note: This re-rolls any 1s in your last roll at the cost of 1 Boon per 1").pack(pady=(5, 0))
        
        # Results area
        results_frame = ttk.LabelFrame(main_frame, text="Roll Results", padding="5")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        self.roll_results_text = ScrolledText(results_frame, wrap=tk.WORD, height=15)
        self.roll_results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.die_status_var = tk.StringVar()
        self.die_status_var.set("Ready to roll")
        status_bar = ttk.Label(main_frame, textvariable=self.die_status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X)
    
    def refresh_generators(self):
        self.simulator.load_generators()
        generator_names = list(self.simulator.generators.keys())
        self.generator_combo['values'] = generator_names
        if generator_names:
            self.generator_var.set(generator_names[0])
            self.on_generator_selected()
        self.status_var.set(f"Loaded {len(generator_names)} generators")
    
    def load_generator_deck(self):
        """Load a generator deck from JSON file"""
        filename = filedialog.askopenfilename(
            title="Load Generator Deck",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    generator_data = json.load(f)
                    generator_name = generator_data.get('name', os.path.basename(filename).replace('.json', ''))
                    self.simulator.generators[generator_name] = generator_data
                    self.refresh_generators()
                    self.generator_var.set(generator_name)
                    self.status_var.set(f"Loaded generator: {generator_name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load generator: {e}")
    
    def on_generator_selected(self, event=None):
        selected = self.generator_var.get()
        if selected in self.simulator.generators:
            self.current_generator = selected
            self.status_var.set(f"Selected generator: {selected}")
    
    def create_deck(self):
        if not self.current_generator:
            messagebox.showwarning("Warning", "Please select a generator first")
            return
        
        self.current_deck = self.simulator.create_deck(self.current_generator)
        self.status_var.set(f"Created deck with {len(self.current_deck)} cards")
    
    def draw_cards(self):
        if not self.current_deck:
            messagebox.showwarning("Warning", "Please create a deck first")
            return
        
        drawn = self.simulator.draw_cards(self.current_deck, 4)
        if not drawn:
            messagebox.showerror("Error", "Not enough cards in deck")
            return
        
        self.simulator.drawn_cards = drawn
        
        # Display cards
        self.cards_text.delete(1.0, tk.END)
        for i, card in enumerate(drawn, 1):
            suit_symbol = {'Spades': '♠', 'Hearts': '♥', 'Clubs': '♣', 'Diamonds': '♦'}.get(card['suit'], card['suit'])
            self.cards_text.insert(tk.END, f"Card {i}: {card['rank']} of {suit_symbol}\n")
            if 'content' in card:
                self.cards_text.insert(tk.END, f"  {card['content']}\n")
            self.cards_text.insert(tk.END, "\n")
        
        # Generate seed
        self.generate_seed(drawn)
        
        # Show combo effects
        self.show_combos(drawn)
        
        self.status_var.set(f"Drew {len(drawn)} cards")
    
    def quick_hook(self):
        if not self.current_deck:
            messagebox.showwarning("Warning", "Please create a deck first")
            return
        
        drawn = self.simulator.draw_cards(self.current_deck, 2)
        if not drawn:
            messagebox.showerror("Error", "Not enough cards in deck")
            return
        
        self.simulator.drawn_cards = drawn
        
        # Display cards
        self.cards_text.delete(1.0, tk.END)
        self.cards_text.insert(tk.END, "QUICK HOOK (2 Cards)\n")
        self.cards_text.insert(tk.END, "=" * 30 + "\n\n")
        
        for i, card in enumerate(drawn, 1):
            suit_symbol = {'Spades': '♠', 'Hearts': '♥', 'Clubs': '♣', 'Diamonds': '♦'}.get(card['suit'], card['suit'])
            self.cards_text.insert(tk.END, f"Card {i}: {card['rank']} of {suit_symbol}\n")
            if 'content' in card:
                self.cards_text.insert(tk.END, f"  {card['content']}\n")
            self.cards_text.insert(tk.END, "\n")
        
        # Simple seed for quick hook
        clock_size = self.simulator.get_clock_size(drawn)
        self.seed_text.delete(1.0, tk.END)
        self.seed_text.insert(tk.END, "QUICK SEED\n")
        self.seed_text.insert(tk.END, "=" * 20 + "\n\n")
        self.seed_text.insert(tk.END, f"Clock Size: {clock_size} segments\n\n")
        self.seed_text.insert(tk.END, "Elements:\n")
        for card in drawn:
            suit_name = card['suit'].lower()
            if suit_name == 'spades':
                self.seed_text.insert(tk.END, f"• Place: {card.get('content', 'Unknown')}\n")
            elif suit_name == 'hearts':
                self.seed_text.insert(tk.END, f"• Actor: {card.get('content', 'Unknown')}\n")
        
        # Show combo effects
        self.show_combos(drawn)
        
        self.status_var.set("Quick hook generated")
    
    def generate_seed(self, cards):
        self.seed_text.delete(1.0, tk.END)
        
        # Clock size
        clock_size = self.simulator.get_clock_size(cards)
        
        # Organize cards by suit
        suit_cards = {'spades': [], 'hearts': [], 'clubs': [], 'diamonds': []}
        for card in cards:
            suit_key = card['suit'].lower()
            suit_cards[suit_key].append(card)
        
        self.seed_text.insert(tk.END, "FULL SEED GENERATION\n")
        self.seed_text.insert(tk.END, "=" * 30 + "\n\n")
        self.seed_text.insert(tk.END, f"Primary Clock: {clock_size} segments\n\n")
        
        # Elements
        self.seed_text.insert(tk.END, "SCENE ELEMENTS:\n")
        self.seed_text.insert(tk.END, "-" * 20 + "\n")
        
        if suit_cards['spades']:
            spade = suit_cards['spades'][0]
            self.seed_text.insert(tk.END, f"Place (♠): {spade.get('content', 'Unknown')}\n")
        
        if suit_cards['hearts']:
            heart = suit_cards['hearts'][0]
            self.seed_text.insert(tk.END, f"Actor (♥): {heart.get('content', 'Unknown')}\n")
        
        if suit_cards['clubs']:
            club = suit_cards['clubs'][0]
            self.seed_text.insert(tk.END, f"Pressure (♣): {club.get('content', 'Unknown')}\n")
        
        if suit_cards['diamonds']:
            diamond = suit_cards['diamonds'][0]
            self.seed_text.insert(tk.END, f"Leverage (♦): {diamond.get('content', 'Unknown')}\n")
        
        # Additional elements if more cards
        additional_count = len(cards) - 4
        if additional_count > 0:
            self.seed_text.insert(tk.END, f"\nADDITIONAL ELEMENTS ({additional_count}):\n")
            self.seed_text.insert(tk.END, "-" * 25 + "\n")
            for i, card in enumerate(cards[4:], 1):
                suit_symbol = {'Spades': '♠', 'Hearts': '♥', 'Clubs': '♣', 'Diamonds': '♦'}.get(card['suit'], card['suit'])
                self.seed_text.insert(tk.END, f"{i}. {suit_symbol} {card['rank']}: {card.get('content', 'Unknown')}\n")
    
    def show_combos(self, cards):
        self.combos_text.delete(1.0, tk.END)
        effects = self.simulator.get_combo_effects(cards)
        
        if effects:
            self.combos_text.insert(tk.END, "COMBO EFFECTS DETECTED:\n")
            self.combos_text.insert(tk.END, "=" * 30 + "\n\n")
            for effect in effects:
                self.combos_text.insert(tk.END, f"• {effect}\n")
        else:
            self.combos_text.insert(tk.END, "No combo effects detected.\n\n")
        
        # Color coding
        self.combos_text.insert(tk.END, "\nCOLOR CODING:\n")
        self.combos_text.insert(tk.END, "-" * 15 + "\n")
        red_count = sum(1 for card in cards if card['color'] == 'red')
        black_count = sum(1 for card in cards if card['color'] == 'black')
        self.combos_text.insert(tk.END, f"Red cards: {red_count} ")
        if red_count >= 3:
            self.combos_text.insert(tk.END, "(Social/Intrigue focus)\n")
        else:
            self.combos_text.insert(tk.END, "\n")
        self.combos_text.insert(tk.END, f"Black cards: {black_count} ")
        if black_count >= 3:
            self.combos_text.insert(tk.END, "(Physical/Threat focus)\n")
        else:
            self.combos_text.insert(tk.END, "\n")
    
    def clear_results(self):
        self.cards_text.delete(1.0, tk.END)
        self.seed_text.delete(1.0, tk.END)
        self.combos_text.delete(1.0, tk.END)
        self.simulator.drawn_cards = []
        self.status_var.set("Results cleared")
    
    def open_generator_editor(self):
        editor = GeneratorEditor(self.root, self.simulator)
        editor_window = editor.create_editor_window()
        editor_window.transient(self.root)
        editor_window.grab_set()
    
    def show_about(self):
        about_text = """
Fate's Edge Deck Simulator v1.0

A Python application for simulating Fate's Edge card-based generators.
Create, edit, and simulate deck draws for campaign generation.

Features:
• Load and simulate any Fate's Edge generator
• Create custom generators with the built-in editor
• Generate full seeds with clock sizes
• Detect combo effects and special rules
• Integrated die roller with consequence management
• Player resource tracking (Boons)

Based on the Fate's Edge RPG system.
        """
        messagebox.showinfo("About Fate's Edge Deck Simulator", about_text)
    
    # Die Roller Methods
    def add_boon(self):
        current = int(self.boons_var.get())
        self.boons_var.set(str(current + 1))
        self.die_status_var.set(f"Boons: {current + 1}")
    
    def remove_boon(self):
        current = int(self.boons_var.get())
        if current > 0:
            self.boons_var.set(str(current - 1))
            self.die_status_var.set(f"Boons: {current - 1}")
    
    def roll_dice(self):
        try:
            dice_count = int(self.dice_count_var.get())
            dv = int(self.dv_var.get())
            is_detailed = self.detailed_var.get()
            is_intricate = self.intricate_var.get()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for dice pool and DV")
            return
        
        if dice_count <= 0 or dv <= 0:
            messagebox.showerror("Error", "Dice pool and DV must be positive numbers")
            return
        
        result = self.die_roller.roll_dice(dice_count, dv, is_detailed, is_intricate)
        
        if "error" in result:
            messagebox.showerror("Error", result["error"])
            return
        
        self.display_roll_result(result)
        
        # Handle complications
        if result["complications"] > 0:
            self.handle_complications(result["complications"])
    
    def reroll_ones(self):
        """Re-roll 1s at the cost of boons"""
        if not self.die_roller.last_roll_result:
            messagebox.showerror("Error", "No previous roll to re-roll")
            return
        
        current_boons = int(self.boons_var.get())
        current_rolls = self.die_roller.last_roll_result["rolls"]
        
        # Count 1s in current rolls
        ones_count = current_rolls.count(1)
        if ones_count == 0:
            messagebox.showinfo("Info", "No 1s to re-roll in the last roll")
            return
        
        if current_boons < ones_count:
            messagebox.showerror("Error", f"Not enough Boons! You have {current_boons}, need {ones_count} to re-roll all 1s")
            return
        
        # Perform re-roll
        reroll_result = self.die_roller.reroll_ones(current_rolls, ones_count)
        
        if "error" in reroll_result:
            messagebox.showerror("Error", reroll_result["error"])
            return
        
        # Update boons
        new_boons = current_boons - reroll_result["boons_used"]
        self.boons_var.set(str(new_boons))
        
        # Display re-roll results
        self.display_reroll_result(reroll_result)
        
        # Handle new complications
        if reroll_result["complications"] > 0:
            self.handle_complications(reroll_result["complications"])
    
    def display_roll_result(self, result):
        self.roll_results_text.delete(1.0, tk.END)
        
        self.roll_results_text.insert(tk.END, "DIE ROLL RESULTS\n")
        self.roll_results_text.insert(tk.END, "=" * 30 + "\n\n")
        
        self.roll_results_text.insert(tk.END, f"Dice Pool: {len(result['rolls'])}d10\n")
        self.roll_results_text.insert(tk.END, f"Rolls: {result['rolls']}\n")
        self.roll_results_text.insert(tk.END, f"Successes: {result['successes']}\n")
        self.roll_results_text.insert(tk.END, f"Complications: {result['complications']}\n")
        self.roll_results_text.insert(tk.END, f"DV: {result['dv']}\n\n")
        
        # Description ladder info
        if result['is_intricate']:
            self.roll_results_text.insert(tk.END, "Description: Intricate (re-rolled all 1s + flourish)\n")
        elif result['is_detailed']:
            self.roll_results_text.insert(tk.END, "Description: Detailed (re-rolled one 1)\n")
        else:
            self.roll_results_text.insert(tk.END, "Description: Basic\n")
        self.roll_results_text.insert(tk.END, "\n")
        
        # Outcome
        self.roll_results_text.insert(tk.END, f"OUTCOME: {result['outcome']}\n")
        self.roll_results_text.insert(tk.END, "-" * 20 + "\n")
        
        if result['outcome'] == "Clean Success":
            self.roll_results_text.insert(tk.END, "Intent achieved crisply with no complications.\n")
        elif result['outcome'] == "Success & Cost":
            self.roll_results_text.insert(tk.END, "Intent achieved, but GM spends CP for consequences.\n")
        elif result['outcome'] == "Partial":
            self.roll_results_text.insert(tk.END, "Progress with tactical fork - accept cost OR concede ground.\n")
        elif result['outcome'] == "Miss":
            self.roll_results_text.insert(tk.END, "No progress; GM spends CP for consequences OR offers tactical bargain.\n")
        
        self.die_status_var.set(f"Rolled {len(result['rolls'])} dice - {result['outcome']}")
    
    def display_reroll_result(self, reroll_result):
        self.roll_results_text.insert(tk.END, f"\nRE-ROLL RESULTS\n")
        self.roll_results_text.insert(tk.END, "=" * 30 + "\n\n")
        
        self.roll_results_text.insert(tk.END, f"Original Rolls: {reroll_result['original_rolls']}\n")
        self.roll_results_text.insert(tk.END, f"Re-rolled Rolls: {reroll_result['rerolled_rolls']}\n")
        self.roll_results_text.insert(tk.END, f"Boons Used: {reroll_result['boons_used']}\n")
        self.roll_results_text.insert(tk.END, f"New Successes: {reroll_result['successes']}\n")
        self.roll_results_text.insert(tk.END, f"New Complications: {reroll_result['complications']}\n\n")
        
        # Recalculate outcome
        if reroll_result['successes'] >= self.die_roller.last_roll_result['dv']:
            if reroll_result['complications'] == 0:
                new_outcome = "Clean Success"
            else:
                new_outcome = "Success & Cost"
        elif reroll_result['successes'] > 0:
            new_outcome = "Partial"
        else:
            new_outcome = "Miss"
        
        self.roll_results_text.insert(tk.END, f"NEW OUTCOME: {new_outcome}\n")
        self.die_status_var.set(f"Re-rolled {reroll_result['boons_used']} dice - {new_outcome}")
    
    def handle_complications(self, cp_count):
        self.roll_results_text.insert(tk.END, f"\nCOMPLICATIONS DETECTED: {cp_count} CP\n")
        self.roll_results_text.insert(tk.END, "=" * 40 + "\n")
        
        # Option 1: Direct spend
        self.roll_results_text.insert(tk.END, "Option 1: Direct Spend\n")
        self.roll_results_text.insert(tk.END, "-" * 20 + "\n")
        self.roll_results_text.insert(tk.END, "GM can spend CP immediately for consequences.\n\n")
        
        # Option 2: Deck draw
        self.roll_results_text.insert(tk.END, "Option 2: Deck Draw\n")
        self.roll_results_text.insert(tk.END, "-" * 20 + "\n")
        draw_count = min(cp_count, 3)
        self.roll_results_text.insert(tk.END, f"Draw {draw_count} cards from Consequences Deck:\n")
        
        consequences = self.die_roller.draw_consequences(cp_count)
        for i, card in enumerate(consequences, 1):
            suit_symbol = {'Hearts': '♥', 'Spades': '♠', 'Clubs': '♣', 'Diamonds': '♦'}.get(card['suit'], card['suit'])
            self.roll_results_text.insert(tk.END, f"{i}. {card['rank']} of {suit_symbol} - {card['type']}\n")
            self.roll_results_text.insert(tk.END, f"   {card['description']}\n\n")

def create_sample_generators():
    """Create sample generator files if they don't exist"""
    if not os.path.exists('generators'):
        os.makedirs('generators')
    
    # Acasia sample generator
    acasia_generator = {
        "name": "Acasia",
        "theme": "Broken Marches",
        "special_mechanics": ["Curse mechanics; every A adds lingering omen"],
        "spades": [
            {"rank": 2, "content": "Broken milestone on the old Imperial Road; borders 'moved' overnight"},
            {"rank": "A", "content": "The Pale Causeway: the last high road that survives spring thaws"}
        ],
        "hearts": [
            {"rank": 2, "content": "Tithe-collector's runner with tally-rod and empty stomach"},
            {"rank": "A", "content": "The Cursed Child of Silkstrand (a rumor more than a person) whose laughter ends sieges"}
        ],
        "clubs": [
            {"rank": 2, "content": "Peat-fog; all horns sound like someone calling your name"},
            {"rank": "A", "content": "The Curse stirs: no matter the road, you return to the same crossroads"}
        ],
        "diamonds": [
            {"rank": 2, "content": "Toll-exemption plaque for one bridge (once)"},
            {"rank": "A", "content": "Curse-redemption rite (temporary): for one night no crossroads can hold you"}
        ]
    }
    
    with open('generators/acasia.json', 'w') as f:
        json.dump(acasia_generator, f, indent=2)

def main():
    # Create sample generators if needed
    create_sample_generators()
    
    # Create and run the GUI
    root = tk.Tk()
    app = FateDeckGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
