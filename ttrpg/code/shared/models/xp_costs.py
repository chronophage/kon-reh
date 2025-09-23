# shared/models/xp_costs.py
from enum import Enum

class XPCosts:
    """Centralized XP cost definitions for Fate's Edge"""
    
    # Attributes: new rating × 3
    @staticmethod
    def attribute_cost(new_rating: int) -> int:
        return new_rating * 3
    
    # Skills: new level × 2
    @staticmethod
    def skill_cost(new_level: int) -> int:
        return new_level * 2
    
    # Followers: Cap²
    @staticmethod
    def follower_cost(cap: int) -> int:
        return cap * cap
    
    # Off-Screen Assets
    ASSET_COSTS = {
        "Minor": 4,
        "Standard": 8,
        "Major": 12
    }
    
    # Common Talents
    TALENT_COSTS = {
        "Battle Instincts": 4,
        "Silver Tongue": 3,
        "Iron Stomach": 3,
        "Stone-Sense": 5,
        "Backlash Soothing": 6,
        "Blood Memory": 7,
        "Familiar Bond": 9,
        "Echo-Walker": 20,
        "Warglord": 18,
        "Spirit-Shield": 15
    }

class AdvancementPath(Enum):
    ENHANCE_SELF = "Enhance Self"
    ACQUIRE_ASSETS = "Acquire Assets"
    LEARN_TALENTS = "Learn Talents"

