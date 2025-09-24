# shared/database/skill_db.py
import sqlite3
import os
import json
import csv
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class SkillCategory(Enum):
    COMBAT = "Combat"
    SOCIAL = "Social"
    EXPLORATION = "Exploration"
    CRAFTING = "Crafting"
    MAGIC = "Magic"
    LORE = "Lore"
    GENERAL = "General"

class TalentType(Enum):
    GENERAL = "General"
    CULTURAL = "Cultural"
    PRESTIGE = "Prestige"

@dataclass
class Skill:
    id: Optional[int]
    name: str
    category: SkillCategory
    description: str
    attribute_links: str  # Comma-separated attributes
    cost_formula: str  # Formula for cost calculation
    max_rating: int = 5
    is_custom: bool = False

@dataclass
class Talent:
    id: Optional[int]
    name: str
    talent_type: TalentType
    description: str
    cost: int
    prerequisites: str  # JSON string of prerequisites
    culture: str = ""  # For cultural talents
    is_custom: bool = False

@dataclass
class PrestigeTalent:
    id: Optional[int]
    name: str
    description: str
    cost: int
    prerequisites: str  # JSON string of prerequisites
    tier: int  # 1-5 tier system
    culture: str = ""
    is_custom: bool = False

class SkillDatabase:
    def __init__(self, db_path=None):
        # Set default path to shared/data/skills.db
        if db_path is None:
            # Get the directory where this script is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Navigate to the shared/data directory
            self.db_path = os.path.join(current_dir, '..', 'data', 'skills.db')
        else:
            self.db_path = db_path
        
        # Normalize the path
        self.db_path = os.path.abspath(self.db_path)
        
        # Ensure the data directory exists
        db_dir = os.path.dirname(self.db_path)
        if db_dir:  # Only try to create directory if there is one
            os.makedirs(db_dir, exist_ok=True)
        
        self.init_database()
        self.populate_default_data()


    def init_database(self):
        """Initialize the database with tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Skills table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                attribute_links TEXT,
                cost_formula TEXT,
                max_rating INTEGER DEFAULT 5,
                is_custom BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Talents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS talents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                talent_type TEXT NOT NULL,
                description TEXT,
                cost INTEGER,
                prerequisites TEXT,
                culture TEXT,
                is_custom BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Prestige Talents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prestige_talents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                cost INTEGER,
                prerequisites TEXT,
                tier INTEGER,
                culture TEXT,
                is_custom BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def populate_default_data(self):
        """Populate with default Fate's Edge skills and talents"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Default skills
        default_skills = [
            ("Melee", "Combat", "Blades, axes, polearms", "Body,Wits,Presence", "new_level * 2"),
            ("Ranged", "Combat", "Bows, crossbows, thrown arms", "Body,Wits", "new_level * 2"),
            ("Athletics", "Exploration", "Climbing, running, swimming", "Body", "new_level * 2"),
            ("Arcana", "Magic", "Magical theory, rituals, spellwork", "Wits,Spirit", "new_level * 2"),
            ("Diplomacy", "Social", "Negotiation, mediation, etiquette", "Presence", "new_level * 2"),
            ("Stealth", "Exploration", "Hiding, shadowing, evading", "Wits", "new_level * 2"),
            ("Deception", "Social", "Disguise, misdirection, bluffing", "Presence", "new_level * 2"),
            ("Survival", "Exploration", "Tracking, foraging, navigation", "Wits", "new_level * 2"),
            ("Command", "Social", "Leadership, intimidation, rallying", "Presence", "new_level * 2"),
            ("Craft", "Crafting", "Smithing, alchemy, tinkering", "Wits", "new_level * 2"),
            ("Performance", "Social", "Music, oratory, storytelling", "Presence", "new_level * 2"),
            ("Lore", "Lore", "History, cultures, languages", "Wits", "new_level * 2"),
            ("Brawl", "Combat", "Fists, grappling, improvised fighting", "Body", "new_level * 2"),
            ("Insight", "Social", "Intuition, empathy, lie detection", "Wits,Spirit", "new_level * 2")
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO skills (name, category, description, attribute_links, cost_formula)
            VALUES (?, ?, ?, ?, ?)
        ''', default_skills)
        
        # Default talents
        default_talents = [
            ("Battle Instincts", "General", "Once per scene, re-roll a failed defense roll", 4, '{"skill_requirements": {}}'),
            ("Silver Tongue", "General", "Gain +1 die when persuading or deceiving through speech", 3, '{"skill_requirements": {}}'),
            ("Iron Stomach", "General", "Immune to mundane poisons and spoiled food; halve Complications from toxic sources", 3, '{"attribute_requirements": {"Body": 2}}'),
            ("Stone-Sense", "Cultural", "Detect flaws in stone or earth; gain +1 die on Engineering or Craft rolls underground", 5, '{"culture": "Dwarves", "attribute_requirements": {"Wits": 2}}'),
            ("Backlash Soothing", "Cultural", "Once per session, reduce a magical Backlash Complication by 2 points when in natural terrain", 6, '{"culture": "Wood Elves", "attribute_requirements": {"Spirit": 2}}'),
            ("Blood Memory", "Cultural", "After a battle, meditate to gain one temporary Skill die reflecting a foe's tactics for the next scene", 7, '{"culture": "Ykrul", "attribute_requirements": {"Body": 3}}')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO talents (name, talent_type, description, cost, prerequisites)
            VALUES (?, ?, ?, ?, ?)
        ''', default_talents)
        
        # Default prestige talents
        default_prestige = [
            ("Echo-Walker", "High Elf prestige ability. Step briefly into Aerisahl; once per arc, turn any Complication into a boon", 20, '{"attributes": {"Wits": 5, "Arcana": 4}, "culture": "High Elf"}', 5),
            ("Warglord", "Ykrul prestige ability. Rally scattered warbands into a single host; once per campaign, may unify tribes under one banner", 18, '{"attributes": {"Body": 5, "Command": 3}, "culture": "Ykrul"}', 5),
            ("Spirit-Shield", "Dwarf prestige ability. Once per session, erase up to 3 Complications from an ally's roll, taking 1 Backlash yourself", 15, '{"attributes": {"Spirit": 4, "Resolve": 3}, "culture": "Dwarf"}', 4),
            ("Duelist's Insight", "Tier II prestige. Once per duel, re-roll all failed dice if you describe a flourish tied to your rival's weakness", 8, '{"attributes": {"Body": 3, "Melee": 3}}', 2),
            ("Hearth-Banner", "Tier II prestige. Allies defending your home or banner gain +1 die to all rolls within its borders", 10, '{"attributes": {"Presence": 2, "Command": 2}, "assets": ["Homestead"]}', 2)
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO prestige_talents (name, description, cost, prerequisites, tier)
            VALUES (?, ?, ?, ?, ?)
        ''', default_prestige)
        
        conn.commit()
        conn.close()
    
    def get_all_skills(self) -> List[Skill]:
        """Retrieve all skills from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM skills')
        rows = cursor.fetchall()
        conn.close()
        
        return [Skill(row[0], row[1], SkillCategory(row[2]), row[3], row[4], row[5], row[6], bool(row[7])) 
                for row in rows]
    
    def get_skills_by_category(self, category: SkillCategory) -> List[Skill]:
        """Retrieve skills by category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM skills WHERE category = ?', (category.value,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Skill(row[0], row[1], SkillCategory(row[2]), row[3], row[4], row[5], row[6], bool(row[7])) 
                for row in rows]
    
    def get_skill_by_name(self, name: str) -> Optional[Skill]:
        """Retrieve a specific skill by name"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM skills WHERE name = ?', (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Skill(row[0], row[1], SkillCategory(row[2]), row[3], row[4], row[5], row[6], bool(row[7]))
        return None
    
    def add_custom_skill(self, skill: Skill) -> bool:
        """Add a custom skill to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO skills (name, category, description, attribute_links, cost_formula, max_rating, is_custom)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (skill.name, skill.category.value, skill.description, skill.attribute_links, 
                  skill.cost_formula, skill.max_rating, skill.is_custom))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_all_talents(self) -> List[Talent]:
        """Retrieve all talents from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM talents')
        rows = cursor.fetchall()
        conn.close()
        
        return [Talent(row[0], row[1], TalentType(row[2]), row[3], row[4], row[5], row[6], bool(row[7])) 
                for row in rows]
    
    def get_talents_by_type(self, talent_type: TalentType) -> List[Talent]:
        """Retrieve talents by type"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM talents WHERE talent_type = ?', (talent_type.value,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Talent(row[0], row[1], TalentType(row[2]), row[3], row[4], row[5], row[6], bool(row[7])) 
                for row in rows]
    
    def get_all_prestige_talents(self) -> List[PrestigeTalent]:
        """Retrieve all prestige talents from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM prestige_talents')
        rows = cursor.fetchall()
        conn.close()
        
        return [PrestigeTalent(row[0], row[1], row[2], row[3], row[4], row[5], row[6], bool(row[7])) 
                for row in rows]
    
    def get_prestige_talents_by_tier(self, tier: int) -> List[PrestigeTalent]:
        """Retrieve prestige talents by tier"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM prestige_talents WHERE tier = ?', (tier,))
        rows = cursor.fetchall()
        conn.close()
        
        return [PrestigeTalent(row[0], row[1], row[2], row[3], row[4], row[5], row[6], bool(row[7])) 
                for row in rows]
    
    def add_custom_talent(self, talent: Talent) -> bool:
        """Add a custom talent to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO talents (name, talent_type, description, cost, prerequisites, culture, is_custom)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (talent.name, talent.talent_type.value, talent.description, talent.cost, 
                  talent.prerequisites, talent.culture, talent.is_custom))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def add_custom_prestige_talent(self, talent: PrestigeTalent) -> bool:
        """Add a custom prestige talent to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO prestige_talents (name, description, cost, prerequisites, tier, culture, is_custom)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (talent.name, talent.description, talent.cost, talent.prerequisites, 
                  talent.tier, talent.culture, talent.is_custom))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    # Import/Export Methods
    def export_to_json(self, filepath: str) -> bool:
        """Export all custom content to JSON file"""
        try:
            data = {
                "skills": [asdict(skill) for skill in self.get_all_skills() if skill.is_custom],
                "talents": [asdict(talent) for talent in self.get_all_talents() if talent.is_custom],
                "prestige_talents": [asdict(talent) for talent in self.get_all_prestige_talents() if talent.is_custom]
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
    
    def import_from_json(self, filepath: str) -> dict:
        """Import custom content from JSON file"""
        results = {"skills": 0, "talents": 0, "prestige_talents": 0, "errors": []}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Import skills
            for skill_data in data.get("skills", []):
                try:
                    skill = Skill(
                        id=None,
                        name=skill_data["name"],
                        category=SkillCategory(skill_data["category"]),
                        description=skill_data["description"],
                        attribute_links=skill_data["attribute_links"],
                        cost_formula=skill_data["cost_formula"],
                        max_rating=skill_data.get("max_rating", 5),
                        is_custom=True
                    )
                    if self.add_custom_skill(skill):
                        results["skills"] += 1
                except Exception as e:
                    results["errors"].append(f"Skill '{skill_data.get('name', 'Unknown')}': {str(e)}")
            
            # Import talents
            for talent_data in data.get("talents", []):
                try:
                    talent = Talent(
                        id=None,
                        name=talent_data["name"],
                        talent_type=TalentType(talent_data["talent_type"]),
                        description=talent_data["description"],
                        cost=talent_data["cost"],
                        prerequisites=talent_data["prerequisites"],
                        culture=talent_data.get("culture", ""),
                        is_custom=True
                    )
                    if self.add_custom_talent(talent):
                        results["talents"] += 1
                except Exception as e:
                    results["errors"].append(f"Talent '{talent_data.get('name', 'Unknown')}': {str(e)}")
            
            # Import prestige talents
            for talent_data in data.get("prestige_talents", []):
                try:
                    talent = PrestigeTalent(
                        id=None,
                        name=talent_data["name"],
                        description=talent_data["description"],
                        cost=talent_data["cost"],
                        prerequisites=talent_data["prerequisites"],
                        tier=talent_data["tier"],
                        culture=talent_data.get("culture", ""),
                        is_custom=True
                    )
                    if self.add_custom_prestige_talent(talent):
                        results["prestige_talents"] += 1
                except Exception as e:
                    results["errors"].append(f"Prestige Talent '{talent_data.get('name', 'Unknown')}': {str(e)}")
                    
            return results
        except Exception as e:
            results["errors"].append(f"Import error: {str(e)}")
            return results
    
    def export_to_csv(self, filepath: str) -> bool:
        """Export all custom content to CSV files"""
        try:
            # Export skills
            skills = [s for s in self.get_all_skills() if s.is_custom]
            if skills:
                with open(f"{filepath}_skills.csv", 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["name", "category", "description", "attribute_links", "cost_formula", "max_rating"])
                    for skill in skills:
                        writer.writerow([
                            skill.name, skill.category.value, skill.description,
                            skill.attribute_links, skill.cost_formula, skill.max_rating
                        ])
            
            # Export talents
            talents = [t for t in self.get_all_talents() if t.is_custom]
            if talents:
                with open(f"{filepath}_talents.csv", 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["name", "talent_type", "description", "cost", "prerequisites", "culture"])
                    for talent in talents:
                        writer.writerow([
                            talent.name, talent.talent_type.value, talent.description,
                            talent.cost, talent.prerequisites, talent.culture
                        ])
            
            # Export prestige talents
            prestige_talents = [p for p in self.get_all_prestige_talents() if p.is_custom]
            if prestige_talents:
                with open(f"{filepath}_prestige.csv", 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["name", "description", "cost", "prerequisites", "tier", "culture"])
                    for talent in prestige_talents:
                        writer.writerow([
                            talent.name, talent.description, talent.cost,
                            talent.prerequisites, talent.tier, talent.culture
                        ])
            
            return True
        except Exception as e:
            print(f"CSV Export error: {e}")
            return False
    
    def import_from_csv(self, base_filepath: str) -> dict:
        """Import custom content from CSV files"""
        results = {"skills": 0, "talents": 0, "prestige_talents": 0, "errors": []}
        
        # Import skills
        skills_file = f"{base_filepath}_skills.csv"
        if os.path.exists(skills_file):
            try:
                with open(skills_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            skill = Skill(
                                id=None,
                                name=row["name"],
                                category=SkillCategory(row["category"]),
                                description=row["description"],
                                attribute_links=row["attribute_links"],
                                cost_formula=row["cost_formula"],
                                max_rating=int(row.get("max_rating", 5)),
                                is_custom=True
                            )
                            if self.add_custom_skill(skill):
                                results["skills"] += 1
                        except Exception as e:
                            results["errors"].append(f"Skill '{row.get('name', 'Unknown')}': {str(e)}")
            except Exception as e:
                results["errors"].append(f"Skills CSV error: {str(e)}")
        
        # Import talents
        talents_file = f"{base_filepath}_talents.csv"
        if os.path.exists(talents_file):
            try:
                with open(talents_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            talent = Talent(
                                id=None,
                                name=row["name"],
                                talent_type=TalentType(row["talent_type"]),
                                description=row["description"],
                                cost=int(row["cost"]),
                                prerequisites=row["prerequisites"],
                                culture=row.get("culture", ""),
                                is_custom=True
                            )
                            if self.add_custom_talent(talent):
                                results["talents"] += 1
                        except Exception as e:
                            results["errors"].append(f"Talent '{row.get('name', 'Unknown')}': {str(e)}")
            except Exception as e:
                results["errors"].append(f"Talents CSV error: {str(e)}")
        
        # Import prestige talents
        prestige_file = f"{base_filepath}_prestige.csv"
        if os.path.exists(prestige_file):
            try:
                with open(prestige_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            talent = PrestigeTalent(
                                id=None,
                                name=row["name"],
                                description=row["description"],
                                cost=int(row["cost"]),
                                prerequisites=row["prerequisites"],
                                tier=int(row["tier"]),
                                culture=row.get("culture", ""),
                                is_custom=True
                            )
                            if self.add_custom_prestige_talent(talent):
                                results["prestige_talents"] += 1
                        except Exception as e:
                            results["errors"].append(f"Prestige Talent '{row.get('name', 'Unknown')}': {str(e)}")
            except Exception as e:
                results["errors"].append(f"Prestige CSV error: {str(e)}")
        
        return results

