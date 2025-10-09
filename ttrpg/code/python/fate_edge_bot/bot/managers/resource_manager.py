import json
import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class ResourceManager:
    def __init__(self, data_dir: str = "bot/data"):
        self.data_dir = data_dir
        self.resources_file = os.path.join(data_dir, "resources.json")
        self.resources = {
            "party": {
                "supply_clock": 0,  # 0-4 segments
                "story_beats": 4,   # Starting budget
                "active_clocks": {}, # Tactical clocks
                "conditions": {}    # Party-wide conditions
            },
            "sessions": [],
            "campaign": {
                "tactical_clocks": {
                    "Mob Overwhelm": {"size": 6, "current": 0},
                    "Fatigue Spiral": {"size": 4, "current": 0},
                    "Morale Collapse": {"size": 6, "current": 0},
                    "Environmental Collapse": {"size": 8, "current": 0},
                    "Reinforcement Arrival": {"size": 4, "current": 0}
                }
            }
        }
        self._ensure_data_dir()
        self.load_resources()
        
    def _ensure_data_dir(self):
        """Ensure the data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory: {self.data_dir}")
            
    def load_resources(self):
        """Load resources from JSON file"""
        try:
            if os.path.exists(self.resources_file):
                with open(self.resources_file, 'r') as f:
                    loaded_data = json.load(f)
                    # Merge with default structure to ensure all keys exist
                    self._merge_defaults(loaded_data)
                    self.resources = loaded_data
                logger.info("Loaded resources")
            else:
                self.save_resources()
        except Exception as e:
            logger.error(f"Error loading resources: {e}")
            
    def _merge_defaults(self, loaded_data: Dict):
        """Merge loaded data with default structure"""
        # Ensure party structure exists
        if "party" not in loaded_data:
            loaded_data["party"] = self.resources["party"]
        else:
            for key, value in self.resources["party"].items():
                if key not in loaded_data["party"]:
                    loaded_data["party"][key] = value
                    
        # Ensure campaign structure exists
        if "campaign" not in loaded_data:
            loaded_data["campaign"] = self.resources["campaign"]
        elif "tactical_clocks" not in loaded_data["campaign"]:
            loaded_data["campaign"]["tactical_clocks"] = self.resources["campaign"]["tactical_clocks"]
            
    def save_resources(self):
        """Save resources to JSON file"""
        try:
            with open(self.resources_file, 'w') as f:
                json.dump(self.resources, f, indent=2, default=str)
            logger.debug("Resources saved successfully")
        except Exception as e:
            logger.error(f"Error saving resources: {e}")
            
    # Supply Clock Management
    def get_supply_status(self) -> Dict[str, Any]:
        """Get current supply status"""
        supply = self.resources["party"]["supply_clock"]
        statuses = {
            0: {"name": "Full Supply", "effect": "No penalties or complications"},
            1: {"name": "Low Supply", "effect": "Minor narrative complications"},
            2: {"name": "Low Supply", "effect": "Minor narrative complications"},
            3: {"name": "Dangerously Low", "effect": "Each character gains Fatigue 1"},
            4: {"name": "Out of Supply", "effect": "Severe penalties; starvation risk"}
        }
        
        return {
            "level": supply,
            "status": statuses.get(supply, {"name": "Unknown", "effect": "Unknown"}),
            "segments": f"{supply}/4",
            "progress_bar": self._create_progress_bar(supply, 4)
        }
        
    def advance_supply_clock(self, reason: str = "") -> Dict[str, Any]:
        """Advance supply clock"""
        current = self.resources["party"]["supply_clock"]
        if current < 4:
            self.resources["party"]["supply_clock"] = current + 1
            self.save_resources()
            
        status = self.get_supply_status()
        status["reason"] = reason
        status["changed"] = current < 4
        
        if current == 3:  # Was dangerously low, now out
            status["warning"] = "PARTY IS NOW OUT OF SUPPLY - SEVERE PENALTIES APPLY"
        elif current == 2:  # Was low, now dangerously low
            status["warning"] = "PARTY IS NOW DANGEROUSLY LOW - EACH CHARACTER GAINS FATIGUE 1"
            
        return status
        
    def clear_supply_clock(self, segments: int = 1) -> Dict[str, Any]:
        """Clear segments from supply clock"""
        current = self.resources["party"]["supply_clock"]
        new_value = max(0, current - segments)
        self.resources["party"]["supply_clock"] = new_value
        self.save_resources()
        
        return {
            "previous": current,
            "current": new_value,
            "cleared": segments,
            "status": self.get_supply_status()
        }
        
    def reset_supply_clock(self) -> Dict[str, Any]:
        """Reset supply clock to full"""
        self.resources["party"]["supply_clock"] = 0
        self.save_resources()
        
        return {
            "previous": "Unknown",
            "current": 0,
            "status": self.get_supply_status(),
            "message": "Supply clock reset to Full Supply"
        }
        
    # Story Beat Management
    def get_story_beat_budget(self) -> int:
        """Get current story beat budget"""
        return self.resources["party"]["story_beats"]
        
    def add_story_beats(self, amount: int = 1) -> int:
        """Add story beats to party budget"""
        self.resources["party"]["story_beats"] += amount
        self.save_resources()
        return self.resources["party"]["story_beats"]
        
    def spend_story_beats(self, amount: int = 1) -> bool:
        """Spend story beats from party budget"""
        if self.resources["party"]["story_beats"] >= amount:
            self.resources["party"]["story_beats"] -= amount
            self.save_resources()
            return True
        return False
        
    def reset_story_beat_budget(self, base_budget: int = 4) -> int:
        """Reset story beat budget (typically at start of session)"""
        self.resources["party"]["story_beats"] = base_budget
        self.save_resources()
        return base_budget
        
    # Character Resource Management
    def get_character_conditions(self, character_name: str) -> Dict[str, Any]:
        """Get conditions for a specific character"""
        character_name = character_name.lower()
        if character_name not in self.resources["party"]["conditions"]:
            self.resources["party"]["conditions"][character_name] = {
                "harm": 0,
                "fatigue": 0,
                "boons": 0,
                "story_beats": 0
            }
            self.save_resources()
            
        return self.resources["party"]["conditions"][character_name]
        
    def set_character_harm(self, character_name: str, level: int) -> bool:
        """Set character harm level (0-3)"""
        character_name = character_name.lower()
        if character_name not in self.resources["party"]["conditions"]:
            self.get_character_conditions(character_name)
            
        self.resources["party"]["conditions"][character_name]["harm"] = max(0, min(3, level))
        self.save_resources()
        return True
        
    def add_character_fatigue(self, character_name: str, amount: int = 1) -> bool:
        """Add fatigue to character"""
        character_name = character_name.lower()
        if character_name not in self.resources["party"]["conditions"]:
            self.get_character_conditions(character_name)
            
        current = self.resources["party"]["conditions"][character_name]["fatigue"]
        self.resources["party"]["conditions"][character_name]["fatigue"] = current + amount
        self.save_resources()
        return True
        
    def clear_character_fatigue(self, character_name: str, amount: int = None) -> bool:
        """Clear fatigue from character"""
        character_name = character_name.lower()
        if character_name not in self.resources["party"]["conditions"]:
            return False
            
        if amount is None:
            self.resources["party"]["conditions"][character_name]["fatigue"] = 0
        else:
            current = self.resources["party"]["conditions"][character_name]["fatigue"]
            self.resources["party"]["conditions"][character_name]["fatigue"] = max(0, current - amount)
            
        self.save_resources()
        return True
        
    def set_character_boons(self, character_name: str, amount: int) -> bool:
        """Set character boons (0-5)"""
        character_name = character_name.lower()
        if character_name not in self.resources["party"]["conditions"]:
            self.get_character_conditions(character_name)
            
        self.resources["party"]["conditions"][character_name]["boons"] = max(0, min(5, amount))
        self.save_resources()
        return True
        
    def add_character_story_beats(self, character_name: str, amount: int = 1) -> bool:
        """Add story beats to character"""
        character_name = character_name.lower()
        if character_name not in self.resources["party"]["conditions"]:
            self.get_character_conditions(character_name)
            
        current = self.resources["party"]["conditions"][character_name]["story_beats"]
        self.resources["party"]["conditions"][character_name]["story_beats"] = current + amount
        self.save_resources()
        return True
        
    # Tactical Clocks
    def get_tactical_clocks(self) -> Dict[str, Any]:
        """Get all tactical clocks"""
        return self.resources["campaign"]["tactical_clocks"]
        
    def get_tactical_clock(self, clock_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific tactical clock"""
        return self.resources["campaign"]["tactical_clocks"].get(clock_name)
        
    def advance_tactical_clock(self, clock_name: str, segments: int = 1) -> Dict[str, Any]:
        """Advance a tactical clock"""
        if clock_name not in self.resources["campaign"]["tactical_clocks"]:
            return {"error": f"Clock '{clock_name}' not found"}
            
        clock = self.resources["campaign"]["tactical_clocks"][clock_name]
        current = clock["current"]
        size = clock["size"]
        new_value = min(size, current + segments)
        clock["current"] = new_value
        self.save_resources()
        
        return {
            "name": clock_name,
            "previous": current,
            "current": new_value,
            "size": size,
            "progress_bar": self._create_progress_bar(new_value, size),
            "completed": new_value >= size,
            "segments_advanced": segments
        }
        
    def clear_tactical_clock(self, clock_name: str, segments: int = 1) -> Dict[str, Any]:
        """Clear segments from a tactical clock"""
        if clock_name not in self.resources["campaign"]["tactical_clocks"]:
            return {"error": f"Clock '{clock_name}' not found"}
            
        clock = self.resources["campaign"]["tactical_clocks"][clock_name]
        current = clock["current"]
        new_value = max(0, current - segments)
        clock["current"] = new_value
        self.save_resources()
        
        return {
            "name": clock_name,
            "previous": current,
            "current": new_value,
            "size": clock["size"],
            "progress_bar": self._create_progress_bar(new_value, clock["size"]),
            "segments_cleared": segments
        }
        
    def reset_tactical_clock(self, clock_name: str) -> Dict[str, Any]:
        """Reset a tactical clock to 0"""
        if clock_name not in self.resources["campaign"]["tactical_clocks"]:
            return {"error": f"Clock '{clock_name}' not found"}
            
        clock = self.resources["campaign"]["tactical_clocks"][clock_name]
        previous = clock["current"]
        clock["current"] = 0
        self.save_resources()
        
        return {
            "name": clock_name,
            "previous": previous,
            "current": 0,
            "size": clock["size"],
            "progress_bar": self._create_progress_bar(0, clock["size"]),
            "message": f"{clock_name} reset"
        }
        
    def create_custom_clock(self, clock_name: str, size: int) -> bool:
        """Create a custom tactical clock"""
        self.resources["campaign"]["tactical_clocks"][clock_name] = {
            "size": size,
            "current": 0
        }
        self.save_resources()
        return True
        
    def remove_custom_clock(self, clock_name: str) -> bool:
        """Remove a custom tactical clock"""
        if clock_name in self.resources["campaign"]["tactical_clocks"]:
            del self.resources["campaign"]["tactical_clocks"][clock_name]
            self.save_resources()
            return True
        return False
        
    # Session Management
    def start_session(self, session_name: str = None) -> Dict[str, Any]:
        """Start a new session"""
        if not session_name:
            session_name = f"Session {len(self.resources['sessions']) + 1}"
            
        session = {
            "name": session_name,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "events": [],
            "story_beats_generated": 0,
            "supply_start": self.resources["party"]["supply_clock"]
        }
        
        self.resources["sessions"].append(session)
        self.reset_story_beat_budget()  # Reset to base budget
        self.save_resources()
        
        return {
            "session_name": session_name,
            "message": f"Session '{session_name}' started",
            "story_beat_budget": self.get_story_beat_budget(),
            "supply_status": self.get_supply_status()
        }
        
    def end_session(self) -> Dict[str, Any]:
        """End the current session"""
        if not self.resources["sessions"]:
            return {"error": "No active session"}
            
        current_session = self.resources["sessions"][-1]
        current_session["end_time"] = datetime.now().isoformat()
        self.save_resources()
        
        return {
            "session_name": current_session["name"],
            "duration": "Calculated from start/end times",
            "supply_change": self.resources["party"]["supply_clock"] - current_session["supply_start"],
            "message": f"Session '{current_session['name']}' ended"
        }
        
    def log_event(self, event: str) -> bool:
        """Log an event in the current session"""
        if not self.resources["sessions"]:
            return False
            
        current_session = self.resources["sessions"][-1]
        current_session["events"].append({
            "time": datetime.now().isoformat(),
            "event": event
        })
        self.save_resources()
        return True
        
    # Utility Functions
    def _create_progress_bar(self, current: int, max_value: int, length: int = 10) -> str:
        """Create a visual progress bar"""
        if max_value == 0:
            return "[" + "□" * length + "]"
            
        filled = int((current / max_value) * length)
        empty = length - filled
        return "[" + "■" * filled + "□" * empty + f"] ({current}/{max_value})"
        
    def get_party_status(self) -> Dict[str, Any]:
        """Get overall party status"""
        supply = self.get_supply_status()
        sb_budget = self.get_story_beat_budget()
        clocks = self.get_tactical_clocks()
        
        # Get active clocks (those with progress)
        active_clocks = {name: clock for name, clock in clocks.items() if clock["current"] > 0}
        
        return {
            "supply": supply,
            "story_beat_budget": sb_budget,
            "active_clocks": active_clocks,
            "character_conditions": self.resources["party"]["conditions"]
        }

