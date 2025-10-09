import json
import os
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class CharacterManager:
    def __init__(self, data_dir: str = "bot/data"):
        self.data_dir = data_dir
        self.characters_file = os.path.join(data_dir, "characters.json")
        self.characters = {}
        self._ensure_data_dir()
        self.load_characters()
        
    def _ensure_data_dir(self):
        """Ensure the data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory: {self.data_dir}")
            
    def load_characters(self):
        """Load characters from JSON file"""
        try:
            if os.path.exists(self.characters_file):
                with open(self.characters_file, 'r') as f:
                    self.characters = json.load(f)
                logger.info(f"Loaded {len(self.characters)} characters")
            else:
                self.characters = {}
                self.save_characters()
        except Exception as e:
            logger.error(f"Error loading characters: {e}")
            self.characters = {}
            
    def save_characters(self):
        """Save characters to JSON file"""
        try:
            with open(self.characters_file, 'w') as f:
                json.dump(self.characters, f, indent=2)
            logger.debug("Characters saved successfully")
        except Exception as e:
            logger.error(f"Error saving characters: {e}")
            
    def create_character(self, name: str, player_id: str, attributes: Dict[str, int] = None, 
                        skills: Dict[str, int] = None) -> bool:
        """
        Create a new character
        
        Args:
            name: Character name
            player_id: Discord user ID of the player
            attributes: Dict with Body, Wits, Spirit, Presence values
            skills: Dict of skill names and levels
            
        Returns:
            bool: True if successful, False if character already exists
        """
        # Check if character already exists
        if name.lower() in [c.get('name', '').lower() for c in self.characters.values()]:
            return False
            
        # Default attributes if not provided
        if attributes is None:
            attributes = {
                "Body": 2,
                "Wits": 2, 
                "Spirit": 2,
                "Presence": 2
            }
            
        # Default skills if not provided
        if skills is None:
            skills = {}
            
        character = {
            "name": name,
            "player_id": player_id,
            "attributes": attributes,
            "skills": skills,
            "harm": 0,
            "fatigue": 0,
            "boons": 0,
            "story_beats": 0,
            "obligation": {},  # Patron: segments
            "assets": [],
            "followers": [],
            "bonds": [],
            "created_at": self._get_timestamp()
        }
        
        self.characters[name.lower()] = character
        self.save_characters()
        logger.info(f"Created character: {name} for player {player_id}")
        return True
        
    def get_character(self, name: str) -> Optional[Dict[str, Any]]:
        """Get character by name (case insensitive)"""
        return self.characters.get(name.lower())
        
    def get_player_characters(self, player_id: str) -> List[Dict[str, Any]]:
        """Get all characters belonging to a player"""
        return [char for char in self.characters.values() if char.get('player_id') == player_id]
        
    def update_character(self, name: str, updates: Dict[str, Any]) -> bool:
        """Update character fields"""
        char = self.get_character(name)
        if not char:
            return False
            
        for key, value in updates.items():
            char[key] = value
            
        self.characters[name.lower()] = char
        self.save_characters()
        return True
        
    def delete_character(self, name: str) -> bool:
        """Delete a character"""
        if name.lower() in self.characters:
            del self.characters[name.lower()]
            self.save_characters()
            logger.info(f"Deleted character: {name}")
            return True
        return False
        
    def list_characters(self) -> List[Dict[str, Any]]:
        """Get list of all characters"""
        return list(self.characters.values())
        
    def add_skill(self, character_name: str, skill_name: str, level: int) -> bool:
        """Add or update a skill for a character"""
        char = self.get_character(character_name)
        if not char:
            return False
            
        char['skills'][skill_name] = level
        self.characters[character_name.lower()] = char
        self.save_characters()
        return True
        
    def get_dice_pool(self, character_name: str, attribute: str, skill_name: str = None) -> int:
        """Calculate dice pool for a roll"""
        char = self.get_character(character_name)
        if not char:
            return 0
            
        # Start with attribute
        dice_pool = char['attributes'].get(attribute, 0)
        
        # Add skill if provided
        if skill_name and skill_name in char['skills']:
            dice_pool += char['skills'].get(skill_name, 0)
            
        return dice_pool
        
    def add_boon(self, character_name: str, amount: int = 1) -> bool:
        """Add boons to character (max 5)"""
        char = self.get_character(character_name)
        if not char:
            return False
            
        current_boons = char.get('boons', 0)
        new_boons = min(5, current_boons + amount)
        char['boons'] = new_boons
        self.characters[character_name.lower()] = char
        self.save_characters()
        return True
        
    def spend_boon(self, character_name: str, amount: int = 1) -> bool:
        """Spend boons from character"""
        char = self.get_character(character_name)
        if not char:
            return False
            
        current_boons = char.get('boons', 0)
        if current_boons >= amount:
            char['boons'] = current_boons - amount
            self.characters[character_name.lower()] = char
            self.save_characters()
            return True
        return False
        
    def add_story_beat(self, character_name: str, amount: int = 1) -> bool:
        """Add story beats to character"""
        char = self.get_character(character_name)
        if not char:
            return False
            
        current_sb = char.get('story_beats', 0)
        char['story_beats'] = current_sb + amount
        self.characters[character_name.lower()] = char
        self.save_characters()
        return True
        
    def set_harm(self, character_name: str, level: int) -> bool:
        """Set character harm level"""
        char = self.get_character(character_name)
        if not char:
            return False
            
        char['harm'] = max(0, min(3, level))  # Harm 0-3
        self.characters[character_name.lower()] = char
        self.save_characters()
        return True
        
    def add_fatigue(self, character_name: str, level: int = 1) -> bool:
        """Add fatigue to character"""
        char = self.get_character(character_name)
        if not char:
            return False
            
        current_fatigue = char.get('fatigue', 0)
        char['fatigue'] = current_fatigue + level
        self.characters[character_name.lower()] = char
        self.save_characters()
        return True
        
    def clear_fatigue(self, character_name: str, amount: int = None) -> bool:
        """Clear fatigue from character"""
        char = self.get_character(character_name)
        if not char:
            return False
            
        current_fatigue = char.get('fatigue', 0)
        if amount is None:
            char['fatigue'] = 0
        else:
            char['fatigue'] = max(0, current_fatigue - amount)
            
        self.characters[character_name.lower()] = char
        self.save_characters()
        return True
        
    def add_asset(self, character_name: str, asset_name: str, condition: str = "Maintained") -> bool:
        """Add an asset to character"""
        char = self.get_character(character_name)
        if not char:
            return False
            
        asset = {
            "name": asset_name,
            "condition": condition
        }
        char['assets'].append(asset)
        self.characters[character_name.lower()] = char
        self.save_characters()
        return True
        
    def add_follower(self, character_name: str, follower_name: str, cap: int, 
                    condition: str = "Steady") -> bool:
        """Add a follower to character"""
        char = self.get_character(character_name)
        if not char:
            return False
            
        follower = {
            "name": follower_name,
            "cap": cap,
            "condition": condition
        }
        char['followers'].append(follower)
        self.characters[character_name.lower()] = char
        self.save_characters()
        return True
        
    def add_bond(self, character_name: str, bond_name: str, description: str = "") -> bool:
        """Add a bond to character"""
        char = self.get_character(character_name)
        if not char:
            return False
            
        bond = {
            "name": bond_name,
            "description": description
        }
        char['bonds'].append(bond)
        self.characters[character_name.lower()] = char
        self.save_characters()
        return True
        
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
        
    def character_exists(self, name: str) -> bool:
        """Check if character exists"""
        return name.lower() in self.characters

