import sqlite3
import os
import logging

# Define the relative path for the database
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/arina_memory.db")

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def init_db():
    """Initialize the database if it does not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Chat history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            conversation_id TEXT,
            role TEXT CHECK(role IN ('user', 'assistant')),
            message TEXT,
            embedding TEXT,
            hour INTEGER,  -- New field for hour of the interaction
            day_of_week INTEGER  -- New field for the day of the week
        )
    ''')

    # User facts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_memory (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    # Feedback table (included as before)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT,
            user_input TEXT,
            arina_reply TEXT,
            reason TEXT
        )
    ''')

    # User interaction patterns table (hourly trends)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interaction_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hour INTEGER,
            day_of_week INTEGER,
            interaction_count INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def create_indexes():
    """Create indexes to improve query performance."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_interaction_patterns_hour_day ON interaction_patterns(hour, day_of_week)")
        conn.commit()
    logging.info("Indexes created.")