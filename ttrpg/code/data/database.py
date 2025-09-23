# data/database.py
import sqlite3
import os
import logging
from typing import Optional, List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = None):
        """Initialize database manager with optional custom path"""
        if db_path is None:
            # Default to fate_edge_decks.db in the same directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(current_dir, '..', 'fate_edge_decks.db')
        else:
            self.db_path = db_path
            
        # Ensure the database directory exists
        db_dir = os.path.dirname(os.path.abspath(self.db_path))
        os.makedirs(db_dir, exist_ok=True)
        
        self.initialize_database()
        
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection"""
        return sqlite3.connect(self.db_path)
        
    def initialize_database(self):
        """Initialize the database with required tables"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create tables
            self.create_tables(cursor)
            
            # Load initial reference data if needed
            self.load_reference_data(cursor)
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
            
    def create_tables(self, cursor):
        """Create all required tables"""
        # Clock reference table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clock_reference (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                size INTEGER,
                category TEXT
            )
        ''')
        
        # Character templates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS character_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                archetype TEXT,
                description TEXT,
                xp_cost INTEGER
            )
        ''')
        
        # Asset reference table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS asset_reference (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                tier TEXT,
                description TEXT,
                xp_cost INTEGER
            )
        ''')
        
        # Follower reference table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS follower_reference (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                cap INTEGER,
                specialty TEXT,
                description TEXT
            )
        ''')
        
        # Consequence cards table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consequence_cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                suit TEXT NOT NULL,
                rank TEXT NOT NULL,
                description TEXT,
                severity TEXT,
                UNIQUE(suit, rank)
            )
        ''')
        
    def load_reference_data(self, cursor):
        """Load initial reference data using INSERT OR IGNORE to prevent duplicates"""
        # Clock templates
        clock_templates = [
            ('Supply Clock', 'Party resource tracking', 4, 'Resource'),
            ('Peril Clock', 'Escalating danger', 6, 'Threat'),
            ('Doom Clock', 'Catastrophic event timer', 8, 'Threat'),
            ('Debt Clock', 'Financial obligations', 6, 'Resource'),
            ('Injury Clock', 'Character harm tracking', 4, 'Threat'),
            ('Hunt Clock', 'Pursuit tracking', 6, 'Threat'),
            ('Campaign Mandate', 'Public legitimacy', 6, 'Campaign'),
            ('Campaign Crisis', 'Opposition engine', 6, 'Campaign')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO clock_reference (name, description, size, category)
            VALUES (?, ?, ?, ?)
        ''', clock_templates)
        
        # Asset templates
        asset_templates = [
            ('Minor Safehouse', 'Standard', 'Basic safehouse for short stays', 4),
            ('Standard Noble Title', 'Standard', 'Regional title with political influence', 8),
            ('Major Mercantile Charter', 'Major', 'Large-scale trade license', 12),
            ('Workshop', 'Minor', 'Crafting and repair facility', 4),
            ('Spy Ring', 'Standard', 'Intelligence network', 8)
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO asset_reference (name, tier, description, xp_cost)
            VALUES (?, ?, ?, ?)
        ''', asset_templates)
        
        # Consequence card data (partial - you'd expand this)
        consequence_cards = [
            ('Hearts', '2', 'Minor emotional setback', 'Minor'),
            ('Hearts', '3', 'Social complication', 'Minor'),
            ('Hearts', '4', 'Relationship strain', 'Moderate'),
            ('Swords', '2', 'Minor injury or equipment issue', 'Minor'),
            ('Swords', '3', 'Combat disadvantage', 'Moderate'),
            ('Pentacles', '2', 'Resource strain', 'Minor'),
            ('Pentacles', '3', 'Gear or supply issue', 'Moderate'),
            ('Wands', '2', 'Magical echo or minor backlash', 'Minor'),
            ('Wands', '3', 'Arcane complication', 'Moderate')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO consequence_cards (suit, rank, description, severity)
            VALUES (?, ?, ?, ?)
        ''', consequence_cards)
        
    # Shared query methods
    def get_clock_templates(self) -> List[Dict[str, Any]]:
        """Get all clock templates"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clock_reference ORDER BY category, name')
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return results
        
    def get_asset_templates(self) -> List[Dict[str, Any]]:
        """Get all asset templates"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM asset_reference ORDER BY tier, name')
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return results
        
    def get_consequence_cards(self, suit: str = None, severity: str = None) -> List[Dict[str, Any]]:
        """Get consequence cards with optional filtering"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM consequence_cards'
        params = []
        
        if suit or severity:
            query += ' WHERE 1=1'
            if suit:
                query += ' AND suit = ?'
                params.append(suit)
            if severity:
                query += ' AND severity = ?'
                params.append(severity)
                
        query += ' ORDER BY suit, rank'
        
        cursor.execute(query, params)
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return results
        
    def get_character_templates(self) -> List[Dict[str, Any]]:
        """Get all character templates"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM character_templates ORDER BY archetype, name')
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return results

# Global database manager instance
db_manager: Optional[DatabaseManager] = None

def get_db_manager(db_path: str = None) -> DatabaseManager:
    """Get or create global database manager instance"""
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager(db_path)
    return db_manager

# Convenience functions for common operations
def initialize_shared_database():
    """Initialize the shared database"""
    return get_db_manager()

def get_clock_templates():
    """Get clock templates from shared database"""
    return get_db_manager().get_clock_templates()

def get_asset_templates():
    """Get asset templates from shared database"""
    return get_db_manager().get_asset_templates()

def get_consequence_cards(suit: str = None, severity: str = None):
    """Get consequence cards from shared database"""
    return get_db_manager().get_consequence_cards(suit, severity)
