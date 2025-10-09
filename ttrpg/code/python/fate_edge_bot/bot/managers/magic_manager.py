import json
import os
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class MagicManager:
    def __init__(self, data_dir: str = "bot/data"):
        self.data_dir = data_dir
        self.magic_file = os.path.join(data_dir, "magic.json")
        self.magic_data = {
            "characters": {},  # character_name: {patron_obligations, capacity, fatigue}
            "patrons": {
                "Sealed Gate": {"thematic_skill": "Tinker", "gift": "Boundary/ Closure"},
                "Ikasha": {"thematic_skill": "Stealth", "gift": "Shadow/ Penumbra"},
                "Oath of Flame": {"thematic_skill": "Command", "gift": "Dawn/ Vows"},
                "Raéyn": {"thematic_skill": "Skirmish", "gift": "Storm/ Tides"},
                "The Witness": {"thematic_skill": "Notice", "gift": "Truth/ Revelation"},
                "Carrion King": {"thematic_skill": "Skirmish", "gift": "Carrion/ Renewal"},
                "Varnek Karn": {"thematic_skill": "Notice", "gift": "Ossuary/ Dominion of the Dead"},
                "Maelstraeus": {"thematic_skill": "Persuade", "gift": "Infernal Bargainer"},
                "Clockwork Monad": {"thematic_skill": "Tinker", "gift": "Iteration/ Process"},
                "Gallows Bell": {"thematic_skill": "Command", "gift": "Doom/ Last Rites"}
            },
            "summons": {}  # character_name: [{entity, cap, leash, status}]
        }
        self._ensure_data_dir()
        self.load_magic_data()
        
    def _ensure_data_dir(self):
        """Ensure the data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory: {self.data_dir}")
            
    def load_magic_data(self):
        """Load magic data from JSON file"""
        try:
            if os.path.exists(self.magic_file):
                with open(self.magic_file, 'r') as f:
                    loaded_data = json.load(f)
                    # Merge with default structure to ensure all keys exist
                    self._merge_defaults(loaded_data)
                    self.magic_data = loaded_data
                logger.info("Loaded magic data")
            else:
                self.save_magic_data()
        except Exception as e:
            logger.error(f"Error loading magic data: {e}")
            
    def _merge_defaults(self, loaded_data: Dict):
        """Merge loaded data with default structure"""
        # Ensure patrons structure exists
        if "patrons" not in loaded_data:
            loaded_data["patrons"] = self.magic_data["patrons"]
        else:
            # Add any missing default patrons
            for patron, data in self.magic_data["patrons"].items():
                if patron not in loaded_data["patrons"]:
                    loaded_data["patrons"][patron] = data
                    
    def save_magic_data(self):
        """Save magic data to JSON file"""
        try:
            with open(self.magic_file, 'w') as f:
                json.dump(self.magic_data, f, indent=2)
            logger.debug("Magic data saved successfully")
        except Exception as e:
            logger.error(f"Error saving magic data: {e}")
            
    # Character Magic Tracking
    def initialize_character(self, character_name: str, spirit: int, presence: int) -> Dict[str, Any]:
        """Initialize magic tracking for a character"""
        capacity = spirit + presence
        self.magic_data["characters"][character_name] = {
            "patron_obligations": {},  # patron_name: segments
            "capacity": capacity,
            "spirit": spirit,
            "presence": presence,
            "fatigue": 0,
            "backlash_sb": 0
        }
        self.save_magic_data()
        
        return {
            "status": "success",
            "message": f"Initialized magic tracking for {character_name}",
            "capacity": capacity,
            "spirit": spirit,
            "presence": presence
        }
        
    def get_character_magic(self, character_name: str) -> Optional[Dict[str, Any]]:
        """Get character's magic status"""
        return self.magic_data["characters"].get(character_name)
        
    def get_all_characters(self) -> Dict[str, Any]:
        """Get all characters with magic tracking"""
        return self.magic_data["characters"]
        
    # Obligation Management
    def add_obligation(self, character_name: str, patron: str, segments: int = 1) -> Dict[str, Any]:
        """Add obligation segments to a character for a specific patron"""
        if character_name not in self.magic_data["characters"]:
            return {"status": "error", "message": f"Character {character_name} not found"}
            
        char_data = self.magic_data["characters"][character_name]
        
        # Add patron if not exists
        if patron not in char_data["patron_obligations"]:
            char_data["patron_obligations"][patron] = 0
            
        char_data["patron_obligations"][patron] += segments
        self.save_magic_data()
        
        # Check for capacity overflow
        total_obligation = sum(char_data["patron_obligations"].values())
        capacity = char_data["capacity"]
        fatigue = 0
        
        if total_obligation > capacity:
            fatigue = total_obligation - capacity
            
        char_data["fatigue"] = max(0, fatigue)  # Update fatigue
        self.save_magic_data()
        
        return {
            "status": "success",
            "message": f"Added {segments} obligation segment(s) to {character_name} for {patron}",
            "patron": patron,
            "segments_added": segments,
            "total_segments": char_data["patron_obligations"][patron],
            "total_obligation": total_obligation,
            "capacity": capacity,
            "fatigue": fatigue,
            "capacity_exceeded": total_obligation > capacity
        }
        
    def clear_obligation(self, character_name: str, patron: str, segments: int = 1) -> Dict[str, Any]:
        """Clear obligation segments for a character and patron"""
        if character_name not in self.magic_data["characters"]:
            return {"status": "error", "message": f"Character {character_name} not found"}
            
        char_data = self.magic_data["characters"][character_name]
        
        if patron not in char_data["patron_obligations"]:
            return {"status": "error", "message": f"Patron {patron} not found for {character_name}"}
            
        current_segments = char_data["patron_obligations"][patron]
        cleared_segments = min(segments, current_segments)
        char_data["patron_obligations"][patron] = max(0, current_segments - cleared_segments)
        
        # Remove patron if no segments left
        if char_data["patron_obligations"][patron] == 0:
            del char_data["patron_obligations"][patron]
            
        # Recalculate total obligation and fatigue
        total_obligation = sum(char_data["patron_obligations"].values())
        capacity = char_data["capacity"]
        
        # Update fatigue based on new obligation level
        if total_obligation <= capacity:
            char_data["fatigue"] = 0
        else:
            char_data["fatigue"] = total_obligation - capacity
            
        self.save_magic_data()
        
        return {
            "status": "success",
            "message": f"Cleared {cleared_segments} obligation segment(s) for {patron}",
            "patron": patron,
            "segments_cleared": cleared_segments,
            "remaining_segments": char_data["patron_obligations"].get(patron, 0),
            "total_obligation": total_obligation,
            "capacity": capacity,
            "fatigue": char_data["fatigue"]
        }
        
    def get_obligation_status(self, character_name: str) -> Dict[str, Any]:
        """Get detailed obligation status for a character"""
        if character_name not in self.magic_data["characters"]:
            return {"status": "error", "message": f"Character {character_name} not found"}
            
        char_data = self.magic_data["characters"][character_name]
        total_obligation = sum(char_data["patron_obligations"].values())
        capacity = char_data["capacity"]
        fatigue = char_data["fatigue"]
        
        # Determine obligation level
        if total_obligation == 0:
            obligation_status = "None"
        elif total_obligation <= capacity:
            obligation_status = "Within Capacity"
        else:
            excess = total_obligation - capacity
            if excess <= 2:
                obligation_status = "Overloaded (Low)"
            elif excess <= 5:
                obligation_status = "Overloaded (Moderate)"
            else:
                obligation_status = "Overloaded (Severe)"
                
        return {
            "status": "success",
            "character": character_name,
            "total_obligation": total_obligation,
            "capacity": capacity,
            "fatigue": fatigue,
            "obligation_status": obligation_status,
            "patron_breakdown": char_data["patron_obligations"],
            "capacity_percentage": min(100, int((total_obligation / max(1, capacity)) * 100)),
            "danger_level": self._get_danger_level(total_obligation, capacity, fatigue)
        }
        
    def _get_danger_level(self, obligation: int, capacity: int, fatigue: int) -> str:
        """Get danger level based on obligation and fatigue"""
        if obligation <= capacity and fatigue == 0:
            return "Safe"
        elif obligation <= capacity + 2 and fatigue <= 1:
            return "Caution"
        elif obligation <= capacity + 5 and fatigue <= 2:
            return "Warning"
        else:
            return "Danger"
            
    # Patron Management
    def get_patron_info(self, patron_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific patron"""
        return self.magic_data["patrons"].get(patron_name)
        
    def list_patrons(self) -> Dict[str, Any]:
        """List all available patrons"""
        return {
            "status": "success",
            "patrons": list(self.magic_data["patrons"].keys()),
            "count": len(self.magic_data["patrons"])
        }
        
    def add_custom_patron(self, patron_name: str, thematic_skill: str, gift: str) -> Dict[str, Any]:
        """Add a custom patron"""
        self.magic_data["patrons"][patron_name] = {
            "thematic_skill": thematic_skill,
            "gift": gift
        }
        self.save_magic_data()
        
        return {
            "status": "success",
            "message": f"Added custom patron {patron_name}",
            "patron": {
                "name": patron_name,
                "thematic_skill": thematic_skill,
                "gift": gift
            }
        }
        
    # Fatigue and Backlash Management
    def add_fatigue(self, character_name: str, amount: int = 1) -> Dict[str, Any]:
        """Add fatigue to a character from magical sources"""
        if character_name not in self.magic_data["characters"]:
            return {"status": "error", "message": f"Character {character_name} not found"}
            
        char_data = self.magic_data["characters"][character_name]
        char_data["fatigue"] += amount
        self.save_magic_data()
        
        return {
            "status": "success",
            "message": f"Added {amount} fatigue to {character_name}",
            "character": character_name,
            "fatigue": char_data["fatigue"],
            "fatigue_effects": self._get_fatigue_effects(char_data["fatigue"])
        }
        
    def clear_fatigue(self, character_name: str, amount: int = None) -> Dict[str, Any]:
        """Clear fatigue from a character"""
        if character_name not in self.magic_data["characters"]:
            return {"status": "error", "message": f"Character {character_name} not found"}
            
        char_data = self.magic_data["characters"][character_name]
        
        if amount is None:
            char_data["fatigue"] = 0
            cleared_amount = "all"
        else:
            previous_fatigue = char_data["fatigue"]
            char_data["fatigue"] = max(0, char_data["fatigue"] - amount)
            cleared_amount = min(amount, previous_fatigue)
            
        self.save_magic_data()
        
        return {
            "status": "success",
            "message": f"Cleared {cleared_amount} fatigue from {character_name}",
            "character": character_name,
            "fatigue": char_data["fatigue"]
        }
        
    def _get_fatigue_effects(self, fatigue_level: int) -> str:
        """Get fatigue effects description"""
        if fatigue_level == 0:
            return "No fatigue effects"
        elif fatigue_level == 1:
            return "Re-roll one success on next action"
        elif fatigue_level == 2:
            return "Re-roll one success on each significant roll"
        elif fatigue_level == 3:
            return "Re-roll two successes on each significant roll"
        else:
            return "Collapse/KO/spiritual break - out of scene until treated"
            
    def add_backlash_sb(self, character_name: str, sb_amount: int = 1) -> Dict[str, Any]:
        """Add Story Beats from magical backlash"""
        if character_name not in self.magic_data["characters"]:
            return {"status": "error", "message": f"Character {character_name} not found"}
            
        char_data = self.magic_data["characters"][character_name]
        char_data["backlash_sb"] += sb_amount
        self.save_magic_data()
        
        return {
            "status": "success",
            "message": f"Added {sb_amount} Story Beat(s) from backlash to {character_name}",
            "character": character_name,
            "backlash_sb": char_data["backlash_sb"]
        }
        
    def clear_backlash_sb(self, character_name: str, sb_amount: int = None) -> Dict[str, Any]:
        """Clear Story Beats from magical backlash"""
        if character_name not in self.magic_data["characters"]:
            return {"status": "error", "message": f"Character {character_name} not found"}
            
        char_data = self.magic_data["characters"][character_name]
        
        if sb_amount is None:
            char_data["backlash_sb"] = 0
            cleared_amount = "all"
        else:
            previous_sb = char_data["backlash_sb"]
            char_data["backlash_sb"] = max(0, char_data["backlash_sb"] - sb_amount)
            cleared_amount = min(sb_amount, previous_sb)
            
        self.save_magic_data()
        
        return {
            "status": "success",
            "message": f"Cleared {cleared_amount} backlash Story Beat(s) from {character_name}",
            "character": character_name,
            "backlash_sb": char_data["backlash_sb"]
        }
        
    # Summoning Management
    def summon_entity(self, character_name: str, entity_name: str, cap: int) -> Dict[str, Any]:
        """Summon an entity/outsider"""
        if character_name not in self.magic_data["summons"]:
            self.magic_data["summons"][character_name] = []
            
        # Calculate leash (Cap + 2)
        leash = cap + 2
        
        summon = {
            "entity": entity_name,
            "cap": cap,
            "leash": leash,
            "current_leash": 0,
            "status": "active",
            "summoned_at": "current_scene"  # This would be more detailed in a real implementation
        }
        
        self.magic_data["summons"][character_name].append(summon)
        self.save_magic_data()
        
        return {
            "status": "success",
            "message": f"{character_name} summoned {entity_name}",
            "entity": entity_name,
            "cap": cap,
            "leash": leash,
            "summon": summon
        }
        
    def advance_leash(self, character_name: str, entity_name: str, segments: int = 1) -> Dict[str, Any]:
        """Advance the leash on a summoned entity"""
        if character_name not in self.magic_data["summons"]:
            return {"status": "error", "message": f"No summons found for {character_name}"}
            
        summon_list = self.magic_data["summons"][character_name]
        summon = None
        index = -1
        
        for i, s in enumerate(summon_list):
            if s["entity"] == entity_name and s["status"] == "active":
                summon = s
                index = i
                break
                
        if not summon:
            return {"status": "error", "message": f"Active summon {entity_name} not found for {character_name}"}
            
        summon["current_leash"] += segments
        departed = False
        
        # Check if leash is filled
        if summon["current_leash"] >= summon["leash"]:
            summon["status"] = "departed"
            departed = True
            
        self.save_magic_data()
        
        return {
            "status": "success",
            "message": f"Advanced leash for {entity_name} by {segments} segment(s)",
            "entity": entity_name,
            "previous_leash": summon["current_leash"] - segments,
            "current_leash": summon["current_leash"],
            "leash_limit": summon["leash"],
            "departed": departed,
            "progress_bar": self._create_progress_bar(summon["current_leash"], summon["leash"])
        }
        
    def get_summons(self, character_name: str) -> Dict[str, Any]:
        """Get all summons for a character"""
        if character_name not in self.magic_data["summons"]:
            return {"status": "success", "summons": []}
            
        return {
            "status": "success",
            "character": character_name,
            "summons": self.magic_data["summons"][character_name]
        }
        
    def dismiss_summon(self, character_name: str, entity_name: str) -> Dict[str, Any]:
        """Dismiss a summoned entity"""
        if character_name not in self.magic_data["summons"]:
            return {"status": "error", "message": f"No summons found for {character_name}"}
            
        summon_list = self.magic_data["summons"][character_name]
        dismissed = False
        dismissed_summon = None
        
        # Find and remove the summon
        for i, summon in enumerate(summon_list):
            if summon["entity"] == entity_name:
                dismissed_summon = summon_list.pop(i)
                dismissed = True
                break
                
        if dismissed:
            self.save_magic_data()
            return {
                "status": "success",
                "message": f"Dismissed {entity_name}",
                "summon": dismissed_summon
            }
        else:
            return {"status": "error", "message": f"Summon {entity_name} not found for {character_name}"}
            
    # Utility Functions
    def _create_progress_bar(self, current: int, max_value: int, length: int = 10) -> str:
        """Create a visual progress bar"""
        if max_value == 0:
            return "[" + "□" * length + "]"
            
        filled = int((current / max_value) * length)
        empty = length - filled
        return "[" + "■" * filled + "□" * empty + f"] ({current}/{max_value})"
        
    def get_magic_status(self, character_name: str) -> Dict[str, Any]:
        """Get comprehensive magic status for a character"""
        if character_name not in self.magic_data["characters"]:
            return {"status": "error", "message": f"Character {character_name} not found"}
            
        char_magic = self.get_character_magic(character_name)
        obligation_status = self.get_obligation_status(character_name)
        summons = self.get_summons(character_name)
        
        return {
            "status": "success",
            "character": character_name,
            "capacity": char_magic["capacity"],
            "spirit": char_magic["spirit"],
            "presence": char_magic["presence"],
            "obligation": obligation_status,
            "fatigue": char_magic["fatigue"],
            "fatigue_effects": self._get_fatigue_effects(char_magic["fatigue"]),
            "backlash_sb": char_magic["backlash_sb"],
            "summons": summons.get("summons", []),
            "danger_level": self._get_danger_level(
                obligation_status["total_obligation"],
                char_magic["capacity"],
                char_magic["fatigue"]
            )
        }
        
    def get_all_magic_status(self) -> Dict[str, Any]:
        """Get magic status for all characters"""
        all_status = {}
        for character_name in self.magic_data["characters"]:
            status = self.get_magic_status(character_name)
            if status["status"] == "success":
                all_status[character_name] = status
                
        return {
            "status": "success",
            "characters": all_status,
            "count": len(all_status)
        }

