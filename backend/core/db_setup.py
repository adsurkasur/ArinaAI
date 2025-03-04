import sqlite3
import os
import logging

# Define the relative path for the database
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/arina_memory.db")

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def init_db():
    """Initialize the database if it does not exist."""
    try:
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
                hour INTEGER,
                day_of_week INTEGER
            )
        ''')

        # User facts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_memory (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')

        # Ensure last interaction timestamp exists
        cursor.execute('''
            INSERT INTO user_memory (key, value)
            VALUES ('last_interaction', datetime('now'))
            ON CONFLICT(key) DO UPDATE SET value = datetime('now');
        ''')

        # Feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT,
                user_input TEXT,
                arina_reply TEXT,
                reason TEXT
            )
        ''')

        # User interaction patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interaction_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hour INTEGER,
                day_of_week INTEGER,
                interaction_count INTEGER
            )
        ''')

        conn.commit()
        logger.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"SQLite error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()

def create_indexes():
    """Create indexes to improve query performance."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_interaction_patterns_hour_day ON interaction_patterns(hour, day_of_week)")
        conn.commit()
        logger.info("Indexes created successfully.")
    except sqlite3.Error as e:
        logger.error(f"SQLite error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()