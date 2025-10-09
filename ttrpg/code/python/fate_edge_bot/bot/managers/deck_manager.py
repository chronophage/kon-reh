import random
import json
import os
import logging
from typing import Dict, Any, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class Suit(Enum):
    SPADE = "Spade"
    HEART = "Heart"
    CLUB = "Club"
    DIAMOND = "Diamond"

class DeckType(Enum):
    TRAVEL = "Travel"
    CONSEQUENCES = "Consequences"
    NPC = "NPC"

class DeckManager:
    def __init__(self, data_dir: str = "bot/data"):
        self.data_dir = data_dir
        self.decks_file = os.path.join(data_dir, "decks.json")
        self.deck_state = {
            "active_decks": {},  # deck_name: {cards_drawn, reshuffle_needed}
            "last_draws": {},    # channel_id: {deck_type, cards, timestamp}
        }
        
        # Regional travel decks data
        self.travel_decks = {
            "Acasia": {
                "theme": "Broken Marches",
                "spades": self._load_acasia_spades(),
                "hearts": self._load_acasia_hearts(),
                "clubs": self._load_acasia_clubs(),
                "diamonds": self._load_acasia_diamonds()
            },
            "Aelaerem": {
                "theme": "Hearth & Hollow",
                "spades": self._load_aelaerem_spades(),
                "hearts": self._load_aelaerem_hearts(),
                "clubs": self._load_aelaerem_clubs(),
                "diamonds": self._load_aelaerem_diamonds()
            },
            "Aeler": {
                "theme": "Crowns & Under-Vaults",
                "spades": self._load_aeler_spades(),
                "hearts": self._load_aeler_hearts(),
                "clubs": self._load_aeler_clubs(),
                "diamonds": self._load_aeler_diamonds()
            },
            "Aelinnel": {
                "theme": "Stone, Bough, and Bright Things",
                "spades": self._load_aelinnel_spades(),
                "hearts": self._load_aelinnel_hearts(),
                "clubs": self._load_aelinnel_clubs(),
                "diamonds": self._load_aelinnel_diamonds()
            },
            "Black_Banners": {
                "theme": "Condotta & Crowns",
                "spades": self._load_black_banners_spades(),
                "hearts": self._load_black_banners_hearts(),
                "clubs": self._load_black_banners_clubs(),
                "diamonds": self._load_black_banners_diamonds()
            },
            "Ecktoria": {
                "theme": "Marble & Fire",
                "spades": self._load_ecktoria_spades(),
                "hearts": self._load_ecktoria_hearts(),
                "clubs": self._load_ecktoria_clubs(),
                "diamonds": self._load_ecktoria_diamonds()
            },
            "Mistlands": {
                "theme": "Bells, Salt, and Breath",
                "spades": self._load_mistlands_spades(),
                "hearts": self._load_mistlands_hearts(),
                "clubs": self._load_mistlands_clubs(),
                "diamonds": self._load_mistlands_diamonds()
            },
            "Valewood": {
                "theme": "Empire Under Leaves",
                "spades": self._load_valewood_spades(),
                "hearts": self._load_valewood_hearts(),
                "clubs": self._load_valewood_clubs(),
                "diamonds": self._load_valewood_diamonds()
            },
            "Wilds": {
                "theme": "Roads, Ruins, and Weather",
                "spades": self._load_wilds_spades(),
                "hearts": self._load_wilds_hearts(),
                "clubs": self._load_wilds_clubs(),
                "diamonds": self._load_wilds_diamonds()
            }
        }
        
        # Consequences deck
        self.consequences_deck = {
            "hearts": self._load_consequences_hearts(),
            "spades": self._load_consequences_spades(),
            "clubs": self._load_consequences_clubs(),
            "diamonds": self._load_consequences_diamonds()
        }
        
        # NPC Generator deck
        self.npc_deck = {
            "ambitions": self._load_npc_ambitions(),
            "beliefs": self._load_npc_beliefs(),
            "attitudes": self._load_npc_attitudes(),
            "twists": self._load_npc_twists()
        }
        
        self._ensure_data_dir()
        self.load_deck_state()
        
    def _ensure_data_dir(self):
        """Ensure the data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory: {self.data_dir}")
            
    def load_deck_state(self):
        """Load deck state from JSON file"""
        try:
            if os.path.exists(self.decks_file):
                with open(self.decks_file, 'r') as f:
                    self.deck_state = json.load(f)
                logger.info("Loaded deck state")
        except Exception as e:
            logger.error(f"Error loading deck state: {e}")
            
    def save_deck_state(self):
        """Save deck state to JSON file"""
        try:
            with open(self.decks_file, 'w') as f:
                json.dump(self.deck_state, f, indent=2)
            logger.debug("Deck state saved successfully")
        except Exception as e:
            logger.error(f"Error saving deck state: {e}")
            
    # Travel Deck Drawing
    def draw_travel_card(self, region: str, suit: str) -> Optional[Dict[str, Any]]:
        """Draw a single card from a travel deck"""
        region_key = region.replace(" ", "_")
        if region_key not in self.travel_decks:
            return None
            
        deck = self.travel_decks[region_key]
        suit_key = suit.capitalize()
        
        if suit_key not in deck:
            return None
            
        cards = deck[suit_key]
        if not cards:
            return None
            
        # Draw a random card
        card = random.choice(cards)
        rank = self._get_card_rank(card)
        
        return {
            "region": region,
            "theme": deck["theme"],
            "suit": suit_key,
            "card": card,
            "rank": rank,
            "rank_name": self._get_rank_name(rank),
            "clock_size": self._get_clock_size(rank)
        }
        
    def draw_quick_hook(self, region: str) -> Dict[str, Any]:
        """Draw a Quick Hook (2 cards) for travel"""
        region_key = region.replace(" ", "_")
        if region_key not in self.travel_decks:
            return {"error": f"Region '{region}' not found"}
            
        # Draw one Spade and one Heart
        spade_card = self.draw_travel_card(region, "spade")
        heart_card = self.draw_travel_card(region, "heart")
        
        if not spade_card or not heart_card:
            return {"error": "Failed to draw cards"}
            
        # Determine clock size from highest rank
        highest_rank = max(spade_card["rank"], heart_card["rank"])
        clock_size = self._get_clock_size(highest_rank)
        
        return {
            "type": "Quick Hook",
            "region": region,
            "theme": self.travel_decks[region_key]["theme"],
            "cards": [spade_card, heart_card],
            "clock_size": clock_size,
            "clock_description": f"{clock_size}-segment clock",
            "highest_rank": highest_rank
        }
        
    def draw_full_seed(self, region: str) -> Dict[str, Any]:
        """Draw a Full Seed (4 cards) for travel"""
        region_key = region.replace(" ", "_")
        if region_key not in self.travel_decks:
            return {"error": f"Region '{region}' not found"}
            
        # Draw one card of each suit
        spade_card = self.draw_travel_card(region, "spade")
        heart_card = self.draw_travel_card(region, "heart")
        club_card = self.draw_travel_card(region, "club")
        diamond_card = self.draw_travel_card(region, "diamond")
        
        if not all([spade_card, heart_card, club_card, diamond_card]):
            return {"error": "Failed to draw all cards"}
            
        # Determine clock size from highest rank
        ranks = [spade_card["rank"], heart_card["rank"], club_card["rank"], diamond_card["rank"]]
        highest_rank = max(ranks)
        clock_size = self._get_clock_size(highest_rank)
        
        # Check for special combinations
        combo_info = self._check_combinations([spade_card, heart_card, club_card, diamond_card])
        
        return {
            "type": "Full Seed",
            "region": region,
            "theme": self.travel_decks[region_key]["theme"],
            "cards": [spade_card, heart_card, club_card, diamond_card],
            "clock_size": clock_size,
            "clock_description": f"{clock_size}-segment clock",
            "highest_rank": highest_rank,
            "combo": combo_info
        }
        
    def _check_combinations(self, cards: List[Dict]) -> Dict[str, Any]:
        """Check for special card combinations"""
        ranks = [card["rank"] for card in cards]
        suits = [card["suit"] for card in cards]
        
        combo_info = {"type": "None", "description": "No special combination"}
        
        # Check for pairs (same rank)
        rank_counts = {}
        for rank in ranks:
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
            
        pairs = [rank for rank, count in rank_counts.items() if count >= 2]
        if pairs:
            combo_info = {
                "type": "Pair",
                "description": f"Recurring motif with rank {self._get_rank_name(pairs[0])}"
            }
            
        # Check for runs (3+ sequential ranks)
        sorted_ranks = sorted(set(ranks))
        if len(sorted_ranks) >= 3:
            is_run = True
            for i in range(1, len(sorted_ranks)):
                if sorted_ranks[i] != sorted_ranks[i-1] + 1:
                    is_run = False
                    break
            if is_run:
                combo_info = {
                    "type": "Run",
                    "description": "Momentum - reduce the main Clock by 1 segment"
                }
                
        # Check for flushes (3+ same suit)
        suit_counts = {}
        for suit in suits:
            suit_counts[suit] = suit_counts.get(suit, 0) + 1
            
        flushes = [suit for suit, count in suit_counts.items() if count >= 3]
        if flushes:
            combo_info = {
                "type": "Flush",
                "description": f"Strongly theme the act toward {flushes[0]} suit"
            }
            
        # Check for face cards or aces
        face_cards = [card for card in cards if card["rank"] >= 11 or card["rank"] == 1]
        if face_cards:
            if len([c for c in face_cards if c["rank"] == 1]) > 0:
                combo_info = {
                    "type": "Ace",
                    "description": "Reveal a hidden patron or power behind the element"
                }
            elif len([c for c in face_cards if c["rank"] >= 11]) > 0:
                combo_info = {
                    "type": "Face Cards",
                    "description": "Significant complication or opportunity"
                }
                
        return combo_info
        
    # Consequences Deck Drawing
    def draw_consequence_card(self, severity: str = "moderate") -> Dict[str, Any]:
        """Draw a card from the Deck of Consequences"""
        # Determine how many cards to draw based on severity
        draw_count = {
            "minor": 1,
            "moderate": 2,
            "major": 3
        }.get(severity.lower(), 2)
        
        suits = ["hearts", "spades", "clubs", "diamonds"]
        drawn_cards = []
        
        for _ in range(draw_count):
            suit = random.choice(suits)
            cards = self.consequences_deck[suit]
            if cards:
                card_text = random.choice(cards)
                drawn_cards.append({
                    "suit": suit.capitalize(),
                    "effect": card_text
                })
                
        return {
            "type": "Consequence Draw",
            "severity": severity,
            "cards_drawn": draw_count,
            "cards": drawn_cards,
            "description": f"Drawing {draw_count} consequence card(s) for {severity} severity"
        }
        
    # NPC Generator
    def generate_npc(self) -> Dict[str, Any]:
        """Generate a random NPC using the NPC deck"""
        ambition = random.choice(self.npc_deck["ambitions"])
        belief = random.choice(self.npc_deck["beliefs"])
        attitude = random.choice(self.npc_deck["attitudes"])
        twist = random.choice(self.npc_deck["twists"])
        
        return {
            "type": "NPC Generation",
            "npc": {
                "ambition": ambition,
                "belief": belief,
                "attitude": attitude,
                "twist": twist
            },
            "description": "Generated NPC profile with ambition, belief, attitude, and twist"
        }
        
    # Utility Functions
    def _get_card_rank(self, card_text: str) -> int:
        """Extract rank from card text (simplified)"""
        # This is a simplified approach - in a real implementation, you'd have
        # the actual card data with ranks
        card_text_lower = card_text.lower()
        if "ace" in card_text_lower or "a " in card_text_lower:
            return 1
        elif "king" in card_text_lower or "k " in card_text_lower:
            return 13
        elif "queen" in card_text_lower or "q " in card_text_lower:
            return 12
        elif "jack" in card_text_lower or "j " in card_text_lower:
            return 11
        elif "10" in card_text_lower:
            return 10
        elif "9" in card_text_lower:
            return 9
        elif "8" in card_text_lower:
            return 8
        elif "7" in card_text_lower:
            return 7
        elif "6" in card_text_lower:
            return 6
        elif "5" in card_text_lower:
            return 5
        elif "4" in card_text_lower:
            return 4
        elif "3" in card_text_lower:
            return 3
        elif "2" in card_text_lower:
            return 2
        else:
            return 7  # Default
            
    def _get_rank_name(self, rank: int) -> str:
        """Convert rank number to name"""
        rank_names = {
            1: "Ace",
            11: "Jack",
            12: "Queen",
            13: "King"
        }
        return rank_names.get(rank, str(rank))
        
    def _get_clock_size(self, rank: int) -> int:
        """Determine clock size based on card rank"""
        if 2 <= rank <= 5:
            return 4  # Minor
        elif 6 <= rank <= 10:
            return 6  # Standard
        elif 11 <= rank <= 13 or rank == 1:  # Face cards or Ace
            return 8  # Major
        else:
            return 6  # Default
            
    def list_regions(self) -> Dict[str, Any]:
        """List all available travel regions"""
        regions = []
        for region_key, region_data in self.travel_decks.items():
            regions.append({
                "name": region_key.replace("_", " "),
                "theme": region_data["theme"]
            })
            
        return {
            "status": "success",
            "regions": regions,
            "count": len(regions)
        }
        
    def get_region_info(self, region: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific region"""
        region_key = region.replace(" ", "_")
        if region_key in self.travel_decks:
            deck = self.travel_decks[region_key]
            return {
                "name": region,
                "theme": deck["theme"],
                "suits": {
                    "spades": len(deck["spades"]),
                    "hearts": len(deck["hearts"]),
                    "clubs": len(deck["clubs"]),
                    "diamonds": len(deck["diamonds"])
                }
            }
        return None
        
    # Format output for Discord
    def format_travel_draw(self, draw_result: Dict[str, Any]) -> str:
        """Format travel card draw for Discord display"""
        if "error" in draw_result:
            return f"❌ **Error**: {draw_result['error']}"
            
        result = f"🃏 **{draw_result['type']}** - {draw_result['region']}\n"
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"**Theme**: {draw_result['theme']}\n"
        result += f"**Clock**: {draw_result['clock_description']}\n\n"
        
        for card in draw_result["cards"]:
            suit_symbol = {"Spade": "♠", "Heart": "♥", "Club": "♣", "Diamond": "♦"}[card["suit"]]
            result += f"{suit_symbol} **{card['suit']}**: {card['card']}\n"
            result += f"   Rank: {card['rank_name']} | Clock: {card['clock_size']}-segment\n\n"
            
        if "combo" in draw_result and draw_result["combo"]["type"] != "None":
            result += f"✨ **Special Combo**: {draw_result['combo']['type']}\n"
            result += f"   {draw_result['combo']['description']}\n"
            
        return result
        
    def format_consequence_draw(self, draw_result: Dict[str, Any]) -> str:
        """Format consequence draw for Discord display"""
        result = f"🃏 **{draw_result['type']}** ({draw_result['severity'].title()} Severity)\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"**Cards Drawn**: {draw_result['cards_drawn']}\n\n"
        
        for i, card in enumerate(draw_result["cards"], 1):
            suit_symbol = {"Hearts": "♥", "Spades": "♠", "Clubs": "♣", "Diamonds": "♦"}[card["suit"]]
            result += f"{i}. {suit_symbol} **{card['suit']} Effect**:\n"
            result += f"   {card['effect']}\n\n"
            
        return result
        
    def format_npc_generation(self, npc_result: Dict[str, Any]) -> str:
        """Format NPC generation for Discord display"""
        npc = npc_result["npc"]
        result = f"👤 **{npc_result['type']}**\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"**Ambition**: {npc['ambition']}\n"
        result += f"**Belief**: {npc['belief']}\n"
        result += f"**Attitude**: {npc['attitude']}\n"
        result += f"**Twist**: {npc['twist']}\n\n"
        result += "Consider the frictions between public ambition, private belief, surface attitude, and the twist."
        return result
        
    # Card Data (Simplified versions - in a real implementation, these would be more detailed)
    def _load_acasia_spades(self) -> List[str]:
        return [
            "Broken milestone on the old Imperial Road",
            "Vine-terrace hillside with an abandoned press",
            "Toll-bridge town over a cold river",
            "Wolfstairs Pass switchbacks",
            "Sootfall Abbey ruins",
            "Hill-motte with fresh palisade",
            "Border-stone ring carved with seven crowns",
            "Blackwood charcoalers' hollow",
            "Salt-road ford with bones in chalk banks",
            "Iron mine adits held by miners' commune",
            "Margravine's hunting lodge",
            "War-camp city with banners claiming throne",
            "The Pale Causeway"
        ]
        
    def _load_acasia_hearts(self) -> List[str]:
        return [
            "Tithe-collector's runner with tally-rod",
            "Roadside prior and lay brothers",
            "Hedge-witch who knows bridge-eating",
            "Free Company captain between contracts",
            "River reeve who rents every boat twice",
            "Salt-Baron with hired blades",
            "Blackwood matriarch tending feud",
            "Ex-imperial surveyor with map",
            "King of three villages with iron taxes",
            "Bride with daggers in wedding chest",
            "Margravine of the Broken March",
            "The Lame King on traveling throne",
            "The Cursed Child of Silkstrand"
        ]
        
    def _load_acasia_clubs(self) -> List[str]:
        return [
            "Peat-fog with calling voices",
            "Sudden levy for day's service",
            "Bridge feud with rival banners",
            "Grain blight doubling tithe",
            "Scree slide sealing pass",
            "Wedding turns ambush",
            "Witch's tithe night with moving lights",
            "Pox sign on village gate",
            "Condotta breaks mid-march",
            "Heretic preacher sparks march",
            "Imperial pretender arrives",
            "River overruns levee",
            "The Curse stirs crossroads"
        ]
        
    def _load_acasia_diamonds(self) -> List[str]:
        return [
            "Toll-exemption plaque for bridge",
            "Monastery letter for bed-and-bread",
            "Wine-right on abandoned terrace",
            "Condotta pike contract",
            "Tithe-remission writ for village",
            "Border-stone adjustment",
            "Pass-key charm for Watchmen",
            "Sealed dowry chest of claims",
            "Mine-share in commune",
            "Blood-peace charter",
            "Marriage proxy from Margravine",
            "The Lame King's traveling writ",
            "Curse-redemption rite"
        ]
        
    # Additional regional card data would go here...
    # For brevity, I'll provide simplified versions of the other regions
    
    def _load_aelaerem_spades(self) -> List[str]:
        return [
            "Willow ford with flat stones",
            "Cider-press barn with sweet reek",
            "Chalk sheep-downs with turf maze",
            "Millpond under alders",
            "Bluebell wood path with rabbit-gates",
            "Hedge-tunnel lane between fields",
            "Cup-mark stone on the verge",
            "Barrow-by-the-beech where bees go quiet",
            "Market green with maypole",
            "Dovecote hill with scarecrow",
            "Mother's Orchard with curving rows",
            "Moot Oak with lantern nails",
            "Hollow Field with plow-line refusal"
        ]
        
    def _load_aelaerem_hearts(self) -> List[str]:
        return [
            "Hedge-witch midwife with red thread",
            "Miller with watch-geese sentries",
            "Orchard reeve with tally-stick",
            "Beekeeper with odd honey",
            "Shepherd with bone whistle",
            "Lantern-warden who trims lamps",
            "Mummers' captain with mask chest",
            "Traveling tinker with bright kettles",
            "Bailiff of the Moot Oak",
            "Wold-Wardens elders",
            "Apple-Matron hostess",
            "Thresher-King in harvest robes",
            "The Pale Shepherd"
        ]
        
    def _load_aelaerem_clubs(self) -> List[str]:
        return [
            "Unseasonal fog walking you back",
            "Scarecrow turns watching lane",
            "Soured wassail giving back names",
            "Black sow through orchard",
            "Hive-swarm at dusk with wrong smoke",
            "Old song taken by children",
            "Lanterns burn blue at ford",
            "Out-of-season mumming",
            "Chalk maze fills with mist",
            "Church bell rings thirteen",
            "Harvest tithe from leaf-gloved hands",
            "Moot Oak bleeds wine-colored sap",
            "The Hollow opens with burrow connection"
        ]
        
    def _load_aelaerem_diamonds(self) -> List[str]:
        return [
            "Guest-loaf & salt for red door board",
            "Cider-mark for free cup on green",
            "Hedge-pass ribbon for thicket step",
            "Bee-queen share with honey-warning",
            "Shepherd's whistle for dogs-bolts",
            "Lantern-writ for path lamps",
            "Mummers' license for feast day",
            "Orchard right for Mother's fruit",
            "Mill token for wheel at any hour",
            "Apple-Matron's blessing",
            "Private moot under the Oak",
            "Thresher-King's red-hooded guard",
            "Pale Shepherd's clause for unseen passing"
        ]
        
    def _load_consequences_hearts(self) -> List[str]:
        return [
            "Social complication with lasting fallout",
            "Emotional vulnerability exposed",
            "Relationship strained or broken",
            "Reputation damaged among peers",
            "Personal secret revealed",
            "Trust betrayed by close ally",
            "Romantic entanglement turns sour",
            "Family obligation creates conflict",
            "Moral compromise affects future choices",
            "Public humiliation or embarrassment"
        ]
        
    def _load_consequences_spades(self) -> List[str]:
        return [
            "Physical injury requiring treatment",
            "Equipment damaged or broken",
            "Environmental hazard escalates",
            "Structural collapse or barrier breach",
            "Ambush or surprise attack",
            "Hostile creature or enemy appears",
            "Resource depletion or supply loss",
            "Time pressure intensifies situation",
            "Escape route blocked or compromised",
            "Catastrophic failure of plan"
        ]
        
    def _load_consequences_clubs(self) -> List[str]:
        return [
            "Material cost depletes resources",
            "Financial burden creates debt",
            "Supply chain disruption",
            "Property damage requiring repair",
            "Time investment delays other plans",
            "Energy expenditure causes fatigue",
            "Opportunity cost of chosen action",
            "Political capital or favor spent",
            "Alliance strained or broken",
            "Legal or bureaucratic entanglement"
        ]
        
    def _load_consequences_diamonds(self) -> List[str]:
        return [
            "Magical disturbance or resonance",
            "Supernatural entity takes notice",
            "Mystical bargain or geas invoked",
            "Arcane knowledge proves dangerous",
            "Spiritual or religious taboo violated",
            "Psychic or mental intrusion",
            "Temporal or reality distortion",
            "Divine or otherworldly intervention",
            "Cursed or blessed with side effects",
            "Mystical energy leaves lingering traces"
        ]
        
    def _load_npc_ambitions(self) -> List[str]:
        return [
            "Power", "Wealth", "Love", "Knowledge", "Revenge", "Honor above all",
            "Survival", "Fame", "Freedom", "Protection", "Control", "Recognition"
        ]
        
    def _load_npc_beliefs(self) -> List[str]:
        return [
            "Might makes right", "Ends justify means", "Truth is sacred",
            "Loyalty is paramount", "Family above all", "Justice must prevail",
            "Fate can be changed", "Tradition must be upheld", "Change is necessary",
            "The system works"
        ]
        
    def _load_npc_attitudes(self) -> List[str]:
        return [
            "Arrogant", "Charismatic", "Cold", "Friendly", "Paranoid",
            "Pious", "Optimistic", "Pessimistic", "Calculating", "Naive"
        ]
        
    def _load_npc_twists(self) -> List[str]:
        return [
            "Secretly insecure", "Betraying their allies", "Working for their enemy",
            "Hiding a dark past", "Actually an impostor", "Deeply compassionate",
            "Corrupted by power", "Hopelessly cynical", "Revolutionary at heart",
            "Acts on impulse", "Cynical manipulator"
        ]
        
    # Additional regional decks would be implemented similarly...
    # For brevity, I'll just provide the function signatures
    
    def _load_aeler_spades(self) -> List[str]: return []
    def _load_aeler_hearts(self) -> List[str]: return []
    def _load_aeler_clubs(self) -> List[str]: return []
    def _load_aeler_diamonds(self) -> List[str]: return []
    
    def _load_aelinnel_spades(self) -> List[str]: return []
    def _load_aelinnel_hearts(self) -> List[str]: return []
    def _load_aelinnel_clubs(self) -> List[str]: return []
    def _load_aelinnel_diamonds(self) -> List[str]: return []
    
    def _load_black_banners_spades(self) -> List[str]: return []
    def _load_black_banners_hearts(self) -> List[str]: return []
    def _load_black_banners_clubs(self) -> List[str]: return []
    def _load_black_banners_diamonds(self) -> List[str]: return []
    
    def _load_ecktoria_spades(self) -> List[str]: return []
    def _load_ecktoria_hearts(self) -> List[str]: return []
    def _load_ecktoria_clubs(self) -> List[str]: return []
    def _load_ecktoria_diamonds(self) -> List[str]: return []
    
    def _load_mistlands_spades(self) -> List[str]: return []
    def _load_mistlands_hearts(self) -> List[str]: return []
    def _load_mistlands_clubs(self) -> List[str]: return []
    def _load_mistlands_diamonds(self) -> List[str]: return []
    
    def _load_valewood_spades(self) -> List[str]: return []
    def _load_valewood_hearts(self) -> List[str]: return []
    def _load_valewood_clubs(self) -> List[str]: return []
    def _load_valewood_diamonds(self) -> List[str]: return []
    
    def _load_wilds_spades(self) -> List[str]: return []
    def _load_wilds_hearts(self) -> List[str]: return []
    def _load_wilds_clubs(self) -> List[str]: return []
    def _load_wilds_diamonds(self) -> List[str]: return []

