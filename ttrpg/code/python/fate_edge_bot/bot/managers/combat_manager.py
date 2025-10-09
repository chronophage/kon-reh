import json
import os
import logging
from typing import Dict, Any, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)

class PositionState(Enum):
    CONTROLLED = "Controlled"
    RISKY = "Risky"
    DESPERATE = "Desperate"

class RangeBand(Enum):
    CLOSE = "Close"
    NEAR = "Near"
    FAR = "Far"
    ABSENT = "Absent"

class CombatManager:
    def __init__(self, data_dir: str = "bot/data"):
        self.data_dir = data_dir
        self.combat_file = os.path.join(data_dir, "combat.json")
        self.combat_state = {
            "active": False,
            "scene_name": "",
            "participants": {},  # character_name: {position, range, conditions, initiative}
            "tactical_clocks": {},
            "round": 0,
            "turn_order": [],
            "current_turn": 0
        }
        self._ensure_data_dir()
        self.load_combat_state()
        
    def _ensure_data_dir(self):
        """Ensure the data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory: {self.data_dir}")
            
    def load_combat_state(self):
        """Load combat state from JSON file"""
        try:
            if os.path.exists(self.combat_file):
                with open(self.combat_file, 'r') as f:
                    self.combat_state = json.load(f)
                logger.info("Loaded combat state")
        except Exception as e:
            logger.error(f"Error loading combat state: {e}")
            
    def save_combat_state(self):
        """Save combat state to JSON file"""
        try:
            with open(self.combat_file, 'w') as f:
                json.dump(self.combat_state, f, indent=2)
            logger.debug("Combat state saved successfully")
        except Exception as e:
            logger.error(f"Error saving combat state: {e}")
            
    # Combat Session Management
    def start_combat(self, scene_name: str = "Combat") -> Dict[str, Any]:
        """Start a new combat session"""
        self.combat_state = {
            "active": True,
            "scene_name": scene_name,
            "participants": {},
            "tactical_clocks": {},
            "round": 1,
            "turn_order": [],
            "current_turn": 0
        }
        self.save_combat_state()
        
        return {
            "status": "success",
            "message": f"Combat session '{scene_name}' started",
            "scene_name": scene_name,
            "round": 1
        }
        
    def end_combat(self) -> Dict[str, Any]:
        """End the current combat session"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        scene_name = self.combat_state["scene_name"]
        self.combat_state["active"] = False
        self.save_combat_state()
        
        return {
            "status": "success",
            "message": f"Combat session '{scene_name}' ended",
            "scene_name": scene_name,
            "rounds": self.combat_state["round"]
        }
        
    def is_active(self) -> bool:
        """Check if combat is currently active"""
        return self.combat_state["active"]
        
    # Participant Management
    def add_participant(self, name: str, is_character: bool = True, 
                       position: str = "Risky", range_band: str = "Near") -> Dict[str, Any]:
        """Add a participant to combat"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        participant = {
            "name": name,
            "is_character": is_character,
            "position": position,
            "range_band": range_band,
            "conditions": {
                "harm": 0,
                "fatigue": 0,
                "entangled": False,
                "blinded": False,
                "silenced": False
            },
            "initiative": 0
        }
        
        self.combat_state["participants"][name] = participant
        self._update_turn_order()
        self.save_combat_state()
        
        return {
            "status": "success",
            "message": f"Added {name} to combat",
            "participant": participant
        }
        
    def remove_participant(self, name: str) -> Dict[str, Any]:
        """Remove a participant from combat"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        if name in self.combat_state["participants"]:
            del self.combat_state["participants"][name]
            self._update_turn_order()
            self.save_combat_state()
            return {"status": "success", "message": f"Removed {name} from combat"}
        else:
            return {"status": "error", "message": f"{name} not found in combat"}
            
    def get_participants(self) -> Dict[str, Any]:
        """Get all combat participants"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        return {
            "status": "success",
            "participants": self.combat_state["participants"],
            "count": len(self.combat_state["participants"])
        }
        
    def get_participant(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific participant"""
        if not self.combat_state["active"]:
            return None
            
        return self.combat_state["participants"].get(name)
        
    # Position and Range Management
    def set_position(self, participant_name: str, position: str) -> Dict[str, Any]:
        """Set a participant's position state"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        if participant_name not in self.combat_state["participants"]:
            return {"status": "error", "message": f"{participant_name} not in combat"}
            
        valid_positions = ["Controlled", "Risky", "Desperate"]
        if position not in valid_positions:
            return {"status": "error", "message": f"Invalid position. Valid: {valid_positions}"}
            
        self.combat_state["participants"][participant_name]["position"] = position
        self.save_combat_state()
        
        return {
            "status": "success",
            "message": f"{participant_name} position set to {position}",
            "position": position,
            "effects": self._get_position_effects(position)
        }
        
    def set_range(self, participant_name: str, range_band: str) -> Dict[str, Any]:
        """Set a participant's range band"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        if participant_name not in self.combat_state["participants"]:
            return {"status": "error", "message": f"{participant_name} not in combat"}
            
        valid_ranges = ["Close", "Near", "Far", "Absent"]
        if range_band not in valid_ranges:
            return {"status": "error", "message": f"Invalid range. Valid: {valid_ranges}"}
            
        self.combat_state["participants"][participant_name]["range_band"] = range_band
        self.save_combat_state()
        
        return {
            "status": "success",
            "message": f"{participant_name} range set to {range_band}",
            "range_band": range_band
        }
        
    def move_participant(self, participant_name: str, direction: str) -> Dict[str, Any]:
        """Move a participant one range band closer or farther"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        if participant_name not in self.combat_state["participants"]:
            return {"status": "error", "message": f"{participant_name} not in combat"}
            
        current_range = self.combat_state["participants"][participant_name]["range_band"]
        range_order = ["Close", "Near", "Far", "Absent"]
        current_index = range_order.index(current_range)
        
        if direction.lower() == "closer":
            new_index = max(0, current_index - 1)
        elif direction.lower() == "farther":
            new_index = min(len(range_order) - 1, current_index + 1)
        else:
            return {"status": "error", "message": "Direction must be 'closer' or 'farther'"}
            
        new_range = range_order[new_index]
        self.combat_state["participants"][participant_name]["range_band"] = new_range
        self.save_combat_state()
        
        return {
            "status": "success",
            "message": f"{participant_name} moved {direction} to {new_range}",
            "from": current_range,
            "to": new_range
        }
        
    # Combat Conditions
    def add_condition(self, participant_name: str, condition: str, value: Any = True) -> Dict[str, Any]:
        """Add a condition to a participant"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        if participant_name not in self.combat_state["participants"]:
            return {"status": "error", "message": f"{participant_name} not in combat"}
            
        if condition not in self.combat_state["participants"][participant_name]["conditions"]:
            return {"status": "error", "message": f"Invalid condition: {condition}"}
            
        self.combat_state["participants"][participant_name]["conditions"][condition] = value
        self.save_combat_state()
        
        return {
            "status": "success",
            "message": f"Added condition '{condition}' to {participant_name}",
            "condition": condition,
            "value": value
        }
        
    def remove_condition(self, participant_name: str, condition: str) -> Dict[str, Any]:
        """Remove a condition from a participant"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        if participant_name not in self.combat_state["participants"]:
            return {"status": "error", "message": f"{participant_name} not in combat"}
            
        if condition not in self.combat_state["participants"][participant_name]["conditions"]:
            return {"status": "error", "message": f"Condition '{condition}' not found"}
            
        # Reset condition to default value based on type
        default_values = {
            "harm": 0,
            "fatigue": 0,
            "entangled": False,
            "blinded": False,
            "silenced": False
        }
        
        default_value = default_values.get(condition, False)
        self.combat_state["participants"][participant_name]["conditions"][condition] = default_value
        self.save_combat_state()
        
        return {
            "status": "success",
            "message": f"Removed condition '{condition}' from {participant_name}",
            "condition": condition,
            "reset_to": default_value
        }
        
    def set_harm(self, participant_name: str, level: int) -> Dict[str, Any]:
        """Set harm level for a participant"""
        return self.add_condition(participant_name, "harm", max(0, min(3, level)))
        
    def add_fatigue(self, participant_name: str, amount: int = 1) -> Dict[str, Any]:
        """Add fatigue to a participant"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        if participant_name not in self.combat_state["participants"]:
            return {"status": "error", "message": f"{participant_name} not in combat"}
            
        current_fatigue = self.combat_state["participants"][participant_name]["conditions"]["fatigue"]
        new_fatigue = current_fatigue + amount
        return self.add_condition(participant_name, "fatigue", new_fatigue)
        
    # Tactical Clocks
    def add_tactical_clock(self, clock_name: str, size: int = 6) -> Dict[str, Any]:
        """Add a tactical clock to the combat"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        self.combat_state["tactical_clocks"][clock_name] = {
            "size": size,
            "current": 0
        }
        self.save_combat_state()
        
        return {
            "status": "success",
            "message": f"Added tactical clock '{clock_name}'",
            "clock": self.combat_state["tactical_clocks"][clock_name]
        }
        
    def advance_clock(self, clock_name: str, segments: int = 1) -> Dict[str, Any]:
        """Advance a tactical clock"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        if clock_name not in self.combat_state["tactical_clocks"]:
            return {"status": "error", "message": f"Clock '{clock_name}' not found"}
            
        clock = self.combat_state["tactical_clocks"][clock_name]
        current = clock["current"]
        size = clock["size"]
        new_value = min(size, current + segments)
        clock["current"] = new_value
        self.save_combat_state()
        
        return {
            "status": "success",
            "message": f"Advanced '{clock_name}' by {segments} segment(s)",
            "clock_name": clock_name,
            "previous": current,
            "current": new_value,
            "size": size,
            "progress_bar": self._create_progress_bar(new_value, size),
            "completed": new_value >= size
        }
        
    def clear_clock(self, clock_name: str, segments: int = 1) -> Dict[str, Any]:
        """Clear segments from a tactical clock"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        if clock_name not in self.combat_state["tactical_clocks"]:
            return {"status": "error", "message": f"Clock '{clock_name}' not found"}
            
        clock = self.combat_state["tactical_clocks"][clock_name]
        current = clock["current"]
        new_value = max(0, current - segments)
        clock["current"] = new_value
        self.save_combat_state()
        
        return {
            "status": "success",
            "message": f"Cleared {segments} segment(s) from '{clock_name}'",
            "clock_name": clock_name,
            "previous": current,
            "current": new_value,
            "size": size,
            "progress_bar": self._create_progress_bar(new_value, clock["size"])
        }
        
    # Turn Management
    def next_turn(self) -> Dict[str, Any]:
        """Advance to the next turn"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        if not self.combat_state["turn_order"]:
            self._update_turn_order()
            
        if not self.combat_state["turn_order"]:
            return {"status": "error", "message": "No participants in combat"}
            
        # Advance turn
        self.combat_state["current_turn"] += 1
        if self.combat_state["current_turn"] >= len(self.combat_state["turn_order"]):
            self.combat_state["current_turn"] = 0
            self.combat_state["round"] += 1
            
        current_participant = self.combat_state["turn_order"][self.combat_state["current_turn"]]
        self.save_combat_state()
        
        return {
            "status": "success",
            "message": f"Round {self.combat_state['round']}, Turn {self.combat_state['current_turn'] + 1}",
            "current_participant": current_participant,
            "round": self.combat_state["round"],
            "turn": self.combat_state["current_turn"] + 1
        }
        
    def get_turn_status(self) -> Dict[str, Any]:
        """Get current turn status"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        if not self.combat_state["turn_order"]:
            return {"status": "error", "message": "No participants in combat"}
            
        current_participant = self.combat_state["turn_order"][self.combat_state["current_turn"]]
        
        return {
            "status": "success",
            "scene_name": self.combat_state["scene_name"],
            "round": self.combat_state["round"],
            "turn": self.combat_state["current_turn"] + 1,
            "current_participant": current_participant,
            "total_participants": len(self.combat_state["turn_order"])
        }
        
    # Utility Functions
    def _update_turn_order(self):
        """Update the turn order based on initiative"""
        if not self.combat_state["active"]:
            return
            
        # Sort participants by initiative (higher first)
        sorted_participants = sorted(
            self.combat_state["participants"].items(),
            key=lambda x: x[1].get("initiative", 0),
            reverse=True
        )
        self.combat_state["turn_order"] = [name for name, _ in sorted_participants]
        
    def _create_progress_bar(self, current: int, max_value: int, length: int = 10) -> str:
        """Create a visual progress bar"""
        if max_value == 0:
            return "[" + "□" * length + "]"
            
        filled = int((current / max_value) * length)
        empty = length - filled
        return "[" + "■" * filled + "□" * empty + f"] ({current}/{max_value})"
        
    def _get_position_effects(self, position: str) -> str:
        """Get descriptive effects for position states"""
        effects = {
            "Controlled": "Advantageous position, minor consequences",
            "Risky": "Even footing, moderate consequences",
            "Desperate": "Disadvantaged, severe consequences"
        }
        return effects.get(position, "Unknown position effects")
        
    def get_combat_status(self) -> Dict[str, Any]:
        """Get comprehensive combat status"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        turn_status = self.get_turn_status()
        participants = self.get_participants()
        clocks = self.combat_state["tactical_clocks"]
        
        # Get active clocks (those with progress)
        active_clocks = {name: clock for name, clock in clocks.items() if clock["current"] > 0}
        
        return {
            "status": "success",
            "scene_name": self.combat_state["scene_name"],
            "round": self.combat_state["round"],
            "turn_status": turn_status,
            "participants": participants["participants"] if participants["status"] == "success" else {},
            "active_clocks": active_clocks,
            "total_participants": len(self.combat_state["participants"])
        }
        
    def set_initiative(self, participant_name: str, initiative: int) -> Dict[str, Any]:
        """Set initiative for a participant"""
        if not self.combat_state["active"]:
            return {"status": "error", "message": "No active combat session"}
            
        if participant_name not in self.combat_state["participants"]:
            return {"status": "error", "message": f"{participant_name} not in combat"}
            
        self.combat_state["participants"][participant_name]["initiative"] = initiative
        self._update_turn_order()
        self.save_combat_state()
        
        return {
            "status": "success",
            "message": f"Set initiative for {participant_name} to {initiative}",
            "participant": participant_name,
            "initiative": initiative
        }

