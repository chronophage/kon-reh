import json
import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class TravelManager:
    def __init__(self, data_dir: str = "bot/data"):
        self.data_dir = data_dir
        self.travel_file = os.path.join(data_dir, "travel.json")
        self.travel_data = {
            "active_journeys": {},  # channel_id: {party, legs, current_leg, status}
            "party_resources": {},  # party_name: {supply, fatigue, conditions}
            "completed_legs": [],   # Historical journey data
            "waypoints": {}         # Custom waypoints
        }
        self._ensure_data_dir()
        self.load_travel_data()
        
    def _ensure_data_dir(self):
        """Ensure the data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory: {self.data_dir}")
            
    def load_travel_data(self):
        """Load travel data from JSON file"""
        try:
            if os.path.exists(self.travel_file):
                with open(self.travel_file, 'r') as f:
                    self.travel_data = json.load(f)
                logger.info("Loaded travel data")
        except Exception as e:
            logger.error(f"Error loading travel data: {e}")
            
    def save_travel_data(self):
        """Save travel data to JSON file"""
        try:
            with open(self.travel_file, 'w') as f:
                json.dump(self.travel_data, f, indent=2, default=str)
            logger.debug("Travel data saved successfully")
        except Exception as e:
            logger.error(f"Error saving travel data: {e}")
            
    # Journey Management
    def start_journey(self, party_name: str, channel_id: str, 
                     starting_region: str = "Civilization") -> Dict[str, Any]:
        """Start a new journey for a party"""
        self.travel_data["active_journeys"][channel_id] = {
            "party_name": party_name,
            "starting_region": starting_region,
            "current_leg": 0,
            "legs": [],
            "status": "planning",
            "start_time": datetime.now().isoformat()
        }
        
        # Initialize party resources
        self.travel_data["party_resources"][party_name] = {
            "supply_clock": 0,
            "fatigue": {},
            "conditions": {},
            "waypoints": []
        }
        
        self.save_travel_data()
        
        return {
            "status": "success",
            "message": f"Journey started for party '{party_name}' in {starting_region}",
            "party_name": party_name,
            "channel_id": channel_id,
            "status": "planning"
        }
        
    def end_journey(self, channel_id: str) -> Dict[str, Any]:
        """End the current journey"""
        if channel_id not in self.travel_data["active_journeys"]:
            return {"status": "error", "message": "No active journey in this channel"}
            
        journey = self.travel_data["active_journeys"][channel_id]
        party_name = journey["party_name"]
        
        # Move to completed legs
        journey["end_time"] = datetime.now().isoformat()
        journey["status"] = "completed"
        self.travel_data["completed_legs"].append(journey)
        
        # Remove from active journeys
        del self.travel_data["active_journeys"][channel_id]
        
        self.save_travel_data()
        
        return {
            "status": "success",
            "message": f"Journey for party '{party_name}' completed",
            "party_name": party_name,
            "legs_completed": len(journey["legs"])
        }
        
    # Leg Management
    def add_travel_leg(self, channel_id: str, destination: str, 
                      clock_size: int = 6) -> Dict[str, Any]:
        """Add a travel leg to the current journey"""
        if channel_id not in self.travel_data["active_journeys"]:
            return {"status": "error", "message": "No active journey in this channel"}
            
        journey = self.travel_data["active_journeys"][channel_id]
        leg_number = len(journey["legs"]) + 1
        
        leg = {
            "leg_number": leg_number,
            "destination": destination,
            "clock_size": clock_size,
            "current_progress": 0,
            "complications": [],
            "waypoints": [],
            "status": "pending"
        }
        
        journey["legs"].append(leg)
        self.save_travel_data()
        
        return {
            "status": "success",
            "message": f"Added travel leg #{leg_number} to {destination}",
            "leg": leg,
            "total_legs": len(journey["legs"])
        }
        
    def advance_travel_leg(self, channel_id: str, segments: int = 1, 
                          complication: str = None) -> Dict[str, Any]:
        """Advance progress on the current travel leg"""
        if channel_id not in self.travel_data["active_journeys"]:
            return {"status": "error", "message": "No active journey in this channel"}
            
        journey = self.travel_data["active_journeys"][channel_id]
        if not journey["legs"]:
            return {"status": "error", "message": "No travel legs defined"}
            
        current_leg = journey["legs"][-1]  # Last leg is current
        current_progress = current_leg["current_progress"]
        clock_size = current_leg["clock_size"]
        
        # Advance progress
        new_progress = min(clock_size, current_progress + segments)
        current_leg["current_progress"] = new_progress
        current_leg["status"] = "in_progress"
        
        # Add complication if provided
        if complication:
            current_leg["complications"].append({
                "description": complication,
                "timestamp": datetime.now().isoformat()
            })
            
        # Check if leg is completed
        leg_completed = new_progress >= clock_size
        
        if leg_completed:
            current_leg["status"] = "completed"
            current_leg["completion_time"] = datetime.now().isoformat()
            
        self.save_travel_data()
        
        return {
            "status": "success",
            "message": f"Advanced travel by {segments} segment(s)",
            "leg_number": current_leg["leg_number"],
            "destination": current_leg["destination"],
            "progress": new_progress,
            "clock_size": clock_size,
            "progress_bar": self._create_progress_bar(new_progress, clock_size),
            "completed": leg_completed,
            "complication": complication
        }
        
    def get_current_leg(self, channel_id: str) -> Dict[str, Any]:
        """Get the current travel leg status"""
        if channel_id not in self.travel_data["active_journeys"]:
            return {"status": "error", "message": "No active journey in this channel"}
            
        journey = self.travel_data["active_journeys"][channel_id]
        if not journey["legs"]:
            return {"status": "error", "message": "No travel legs defined"}
            
        current_leg = journey["legs"][-1]
        
        return {
            "status": "success",
            "journey_status": journey["status"],
            "leg": current_leg,
            "progress_bar": self._create_progress_bar(
                current_leg["current_progress"], 
                current_leg["clock_size"]
            ),
            "party_name": journey["party_name"]
        }
        
    # Party Resource Management
    def get_party_resources(self, party_name: str) -> Dict[str, Any]:
        """Get resources for a traveling party"""
        if party_name not in self.travel_data["party_resources"]:
            return {"status": "error", "message": f"Party '{party_name}' not found"}
            
        return {
            "status": "success",
            "party_name": party_name,
            "resources": self.travel_data["party_resources"][party_name]
        }
        
    def update_supply(self, party_name: str, change: int) -> Dict[str, Any]:
        """Update supply clock for a party"""
        if party_name not in self.travel_data["party_resources"]:
            # Initialize if not exists
            self.travel_data["party_resources"][party_name] = {
                "supply_clock": 0,
                "fatigue": {},
                "conditions": {},
                "waypoints": []
            }
            
        resources = self.travel_data["party_resources"][party_name]
        current_supply = resources["supply_clock"]
        new_supply = max(0, min(4, current_supply + change))  # 0-4 range
        resources["supply_clock"] = new_supply
        
        self.save_travel_data()
        
        # Supply status descriptions
        supply_status = {
            0: "Full Supply - No penalties",
            1: "Low Supply - Minor complications",
            2: "Low Supply - Minor complications", 
            3: "Dangerously Low - Each character gains Fatigue 1",
            4: "Out of Supply - Severe penalties, starvation risk"
        }
        
        return {
            "status": "success",
            "message": f"Supply changed by {change}",
            "previous": current_supply,
            "current": new_supply,
            "status_text": supply_status.get(new_supply, "Unknown"),
            "progress_bar": self._create_progress_bar(new_supply, 4)
        }
        
    def add_party_fatigue(self, party_name: str, character_name: str, 
                         amount: int = 1) -> Dict[str, Any]:
        """Add fatigue to a character in the party"""
        if party_name not in self.travel_data["party_resources"]:
            return {"status": "error", "message": f"Party '{party_name}' not found"}
            
        resources = self.travel_data["party_resources"][party_name]
        if character_name not in resources["fatigue"]:
            resources["fatigue"][character_name] = 0
            
        resources["fatigue"][character_name] += amount
        self.save_travel_data()
        
        return {
            "status": "success",
            "message": f"Added {amount} fatigue to {character_name}",
            "character": character_name,
            "fatigue": resources["fatigue"][character_name],
            "fatigue_effects": self._get_fatigue_effects(resources["fatigue"][character_name])
        }
        
    def clear_party_fatigue(self, party_name: str, character_name: str, 
                           amount: int = None) -> Dict[str, Any]:
        """Clear fatigue from a character in the party"""
        if party_name not in self.travel_data["party_resources"]:
            return {"status": "error", "message": f"Party '{party_name}' not found"}
            
        resources = self.travel_data["party_resources"][party_name]
        if character_name not in resources["fatigue"]:
            return {"status": "error", "message": f"Character '{character_name}' not found"}
            
        if amount is None:
            resources["fatigue"][character_name] = 0
            cleared_amount = "all"
        else:
            previous_fatigue = resources["fatigue"][character_name]
            resources["fatigue"][character_name] = max(0, previous_fatigue - amount)
            cleared_amount = min(amount, previous_fatigue)
            
        self.save_travel_data()
        
        return {
            "status": "success",
            "message": f"Cleared {cleared_amount} fatigue from {character_name}",
            "character": character_name,
            "fatigue": resources["fatigue"][character_name]
        }
        
    # Waypoint Management
    def add_waypoint(self, party_name: str, waypoint_name: str, 
                    description: str = "") -> Dict[str, Any]:
        """Add a waypoint for a party"""
        if party_name not in self.travel_data["party_resources"]:
            self.travel_data["party_resources"][party_name] = {
                "supply_clock": 0,
                "fatigue": {},
                "conditions": {},
                "waypoints": []
            }
            
        waypoint = {
            "name": waypoint_name,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        
        self.travel_data["party_resources"][party_name]["waypoints"].append(waypoint)
        self.save_travel_data()
        
        return {
            "status": "success",
            "message": f"Added waypoint '{waypoint_name}'",
            "waypoint": waypoint
        }
        
    def get_waypoints(self, party_name: str) -> Dict[str, Any]:
        """Get waypoints for a party"""
        if party_name not in self.travel_data["party_resources"]:
            return {"status": "error", "message": f"Party '{party_name}' not found"}
            
        waypoints = self.travel_data["party_resources"][party_name]["waypoints"]
        
        return {
            "status": "success",
            "party_name": party_name,
            "waypoints": waypoints,
            "count": len(waypoints)
        }
        
    # Utility Functions
    def _create_progress_bar(self, current: int, max_value: int, length: int = 10) -> str:
        """Create a visual progress bar"""
        if max_value == 0:
            return "[" + "□" * length + "]"
            
        filled = int((current / max_value) * length)
        empty = length - filled
        return "[" + "■" * filled + "□" * empty + f"] ({current}/{max_value})"
        
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
            
    def get_journey_status(self, channel_id: str) -> Dict[str, Any]:
        """Get comprehensive journey status"""
        if channel_id not in self.travel_data["active_journeys"]:
            return {"status": "error", "message": "No active journey in this channel"}
            
        journey = self.travel_data["active_journeys"][channel_id]
        party_name = journey["party_name"]
        party_resources = self.travel_data["party_resources"].get(party_name, {})
        
        # Get current leg if exists
        current_leg = None
        if journey["legs"]:
            current_leg = journey["legs"][-1]
            
        return {
            "status": "success",
            "journey": {
                "party_name": party_name,
                "starting_region": journey["starting_region"],
                "status": journey["status"],
                "total_legs": len(journey["legs"]),
                "current_leg": current_leg,
                "start_time": journey["start_time"]
            },
            "party_resources": party_resources,
            "supply_status": self._get_supply_status(party_resources.get("supply_clock", 0)),
            "progress_bar": self._create_progress_bar(
                current_leg["current_progress"] if current_leg else 0,
                current_leg["clock_size"] if current_leg else 6
            ) if current_leg else "[□□□□□□]"
        }
        
    def _get_supply_status(self, supply_level: int) -> Dict[str, str]:
        """Get supply status information"""
        statuses = {
            0: {"name": "Full Supply", "effect": "No penalties or complications"},
            1: {"name": "Low Supply", "effect": "Minor narrative complications"},
            2: {"name": "Low Supply", "effect": "Minor narrative complications"},
            3: {"name": "Dangerously Low", "effect": "Each character gains Fatigue 1"},
            4: {"name": "Out of Supply", "effect": "Severe penalties; starvation risk"}
        }
        
        return statuses.get(supply_level, {"name": "Unknown", "effect": "Unknown"})
        
    def format_journey_status(self, status_data: Dict[str, Any]) -> str:
        """Format journey status for Discord display"""
        if status_data["status"] == "error":
            return f"❌ {status_data['message']}"
            
        journey = status_data["journey"]
        resources = status_data["party_resources"]
        supply_info = status_data["supply_status"]
        
        result = f"🗺️ **Journey Status** - {journey['party_name']}\n"
        result += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"**Status**: {journey['status'].title()}\n"
        result += f"**Starting Region**: {journey['starting_region']}\n"
        result += f"**Legs Completed**: {journey['total_legs']}\n\n"
        
        if resources:
            result += f"**Supply**: {supply_info['name']}\n"
            result += f"{status_data['progress_bar']}\n"
            result += f"Effect: {supply_info['effect']}\n\n"
            
        current_leg = journey.get("current_leg")
        if current_leg:
            result += f"**Current Leg**: #{current_leg['leg_number']} to {current_leg['destination']}\n"
            result += f"Progress: {status_data['progress_bar']}\n"
            if current_leg["complications"]:
                result += f"**Complications**: {len(current_leg['complications'])}\n"
                
        return result

