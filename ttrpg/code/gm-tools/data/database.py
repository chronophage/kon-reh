import sqlite3
import os
import datetime

class Database:
    def __init__(self):
        self.db_path = "fate_edge_decks.db"
        self.sql_path = "data/fate_edge_data_clean.sql"
        self.clocks_sql_path = "data/fate_edge_clocks.sql"
        self.log_path = "fate_edge_debug.log"
        self.init_database()
        
    def log_debug(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        try:
            with open(self.log_path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_message)
        except Exception as e:
            print(f"Logging error: {e}")
        print(log_message.strip())
        
    def init_database(self):
        self.log_debug("Initializing database")
        if os.path.exists(self.sql_path):
            self.log_debug(f"Loading database from SQL file: {self.sql_path}")
            self.load_from_sql_file()
        elif not os.path.exists(self.db_path):
            self.log_debug("Creating default database")
            self.create_default_database()
        else:
            self.log_debug("Using existing database")
            
        self.load_clock_reference_data()
        
    def load_from_sql_file(self):
        try:
            conn = sqlite3.connect(self.db_path)
            with open(self.sql_path, 'r', encoding='utf-8') as sql_file:
                sql_script = sql_file.read()
                conn.executescript(sql_script)
            conn.close()
            self.log_debug("Database loaded successfully from SQL file")
        except Exception as e:
            error_msg = f"Error loading SQL file: {e}"
            self.log_debug(error_msg)
            if not os.path.exists(self.db_path):
                self.log_debug("Creating default database as fallback")
                self.create_default_database()
                
    def create_default_database(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS consequence_descriptors (
                    id INTEGER PRIMARY KEY,
                    suit TEXT,
                    rank TEXT,
                    domain TEXT,
                    severity TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS npc_descriptors (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    suit TEXT,
                    rank TEXT,
                    description TEXT,
                    hook_suggestion TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS adventure_descriptors (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    suit TEXT,
                    rank TEXT,
                    description TEXT
                )
            """)
            
            conn.commit()
            conn.close()
            self.log_debug("Default database created successfully")
        except Exception as e:
            self.log_debug(f"Error creating default database: {e}")
            
    def load_clock_reference_data(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clock_reference (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    segments INTEGER
                )
            """)
            
            cursor.execute("SELECT COUNT(*) FROM clock_reference")
            count = cursor.fetchone()[0]
            
            if count == 0:
                default_clocks = [
                    ("Action / Task", 4),
                    ("Stealth / Alert / Heat", 4),
                    ("Recovery / Healing", 4),
                    ("Resource Depletion", 4),
                    ("Environmental Hazard", 6),
                    ("Investigation / Cluework", 6),
                    ("Negotiation / Social Contest", 6),
                    ("Travel / Journey Leg", 6),
                    ("Craft / Research / Downtime Project", 6),
                    ("Trace / Manhunt / Security Response", 6),
                    ("Threat / Boss (single phase)", 8),
                    ("Heist Layer / Access", 8),
                    ("Countdown / Doom / Catastrophe", 8),
                    ("Setpiece Objective", 8),
                    ("Faction Progress / Territory Shift", 8),
                    ("Relationship / Trust / Influence", 6),
                    ("Major Project / Arc Goal", 12),
                    ("Campaign-Level Change", 12)
                ]
                
                cursor.executemany(
                    "INSERT INTO clock_reference (name, segments) VALUES (?, ?)",
                    default_clocks
                )
            
            conn.commit()
            conn.close()
            self.log_debug("Clock reference data loaded successfully")
        except Exception as e:
            self.log_debug(f"Error loading clock reference data: {e}")
            
    def get_consequence_meaning(self, suit, rank):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if rank in ["Jack", "Queen", "King"]:
                rank_range = "J-K"
            elif rank == "Ace":
                rank_range = "Ace"
            elif int(rank) <= 5:
                rank_range = "2-5"
            elif int(rank) <= 10:
                rank_range = "6-10"
            else:
                rank_range = "J-K"
                
            cursor.execute("""
                SELECT domain, severity FROM consequence_descriptors 
                WHERE suit = ? AND rank = ?
            """, (suit, rank_range))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return result[0], result[1]
            else:
                return "Unknown Domain", "Unknown Severity"
        except Exception as e:
            return "Database Error", str(e)
        
    def get_npc_descriptor(self, category, suit, rank):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT description, hook_suggestion FROM npc_descriptors 
                WHERE category = ? AND suit = ? AND rank = ?
            """, (category, suit, str(rank)))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                desc = result[0] if result[0] else f"{suit} {rank}"
                hook = result[1] if result[1] else None
                return desc, hook
            else:
                return f"{suit} {rank}", None
        except Exception as e:
            return "Database Error", str(e)
        
    def get_adventure_descriptor(self, category, suit, rank):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT description FROM adventure_descriptors 
                WHERE category = ? AND suit = ? AND rank = ?
            """, (category, suit, str(rank)))
            
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0]:
                return result[0]
            else:
                return f"{category}: {suit} {rank} (No descriptor found)"
        except Exception as e:
            return f"Database Error: {str(e)}"
