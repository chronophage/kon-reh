# shared/models/character.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class Archetype(Enum):
    SOLO = "Solo"
    MIXED = "Mixed"
    MASTERMIND = "Mastermind"

class AttributeType(Enum):
    BODY = "Body"
    WITS = "Wits"
    SPIRIT = "Spirit"
    PRESENCE = "Presence"

class SkillType(Enum):
    MELEE = "Melee"
    RANGED = "Ranged"
    ATHLETICS = "Athletics"
    ARCANA = "Arcana"
    DIPLOMACY = "Diplomacy"
    STEALTH = "Stealth"
    DECEPTION = "Deception"
    SURVIVAL = "Survival"
    COMMAND = "Command"
    CRAFT = "Craft"
    PERFORMANCE = "Performance"
    LORE = "Lore"

@dataclass
class Attribute:
    name: AttributeType
    value: int = 2

@dataclass
class Skill:
    name: SkillType
    value: int = 0

@dataclass
class Talent:
    name: str
    description: str
    cost: int
    prerequisites: Dict = field(default_factory=dict)

@dataclass
class Follower:
    name: str
    specialty: str
    cap: int  # 1-5 rating
    condition: str = "Maintained"  # Maintained, Neglected, Compromised

@dataclass
class Asset:
    name: str
    tier: str  # Minor, Standard, Major
    description: str
    condition: str = "Maintained"  # Maintained, Neglected, Compromised

@dataclass
class Character:
    name: str = ""
    archetype: Archetype = Archetype.SOLO
    xp: int = 0
    total_earned_xp: int = 0
    boons: int = 0
    fatigue: int = 0
    attributes: Dict[AttributeType, Attribute] = field(default_factory=dict)
    skills: Dict[SkillType, Skill] = field(default_factory=dict)
    talents: List[Talent] = field(default_factory=list)
    followers: List[Follower] = field(default_factory=list)
    assets: List[Asset] = field(default_factory=list)
    notes: str = ""
    
    def __post_init__(self):
        # Initialize default attributes if not provided
        if not self.attributes:
            for attr_type in AttributeType:
                self.attributes[attr_type] = Attribute(attr_type)
                
        # Initialize default skills if not provided
        if not self.skills:
            for skill_type in SkillType:
                self.skills[skill_type] = Skill(skill_type)
    
    def get_attribute(self, attr_type: AttributeType) -> int:
        return self.attributes.get(attr_type, Attribute(attr_type)).value
    
    def get_skill(self, skill_type: SkillType) -> int:
        return self.skills.get(skill_type, Skill(skill_type)).value
    
    def dice_pool(self, attr_type: AttributeType, skill_type: SkillType) -> int:
        """Calculate dice pool for a given attribute + skill combination"""
        attr_value = self.get_attribute(attr_type)
        skill_value = self.get_skill(skill_type)
        return attr_value + skill_value
    
    def add_xp(self, amount: int):
        """Add XP to character"""
        self.xp += amount
        self.total_earned_xp += amount
    
    def spend_xp(self, amount: int) -> bool:
        """Spend XP if available"""
        if self.xp >= amount:
            self.xp -= amount
            return True
        return False

