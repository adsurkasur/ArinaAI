import sqlite3
import logging
from .db_setup import DB_PATH
from datetime import datetime

def reset_memory():
    """Wipe all stored conversations and facts."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conversations")
            cursor.execute("DELETE FROM user_memory")
            cursor.execute("DELETE FROM feedback")
            cursor.execute("DELETE FROM interaction_patterns")
            conn.commit()
        logging.info("Memory reset: All data deleted.")
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def update_last_interaction():
    """Update the last interaction timestamp in memory."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            timestamp = datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO user_memory (key, value)
                VALUES ('last_interaction', ?)
                ON CONFLICT(key) DO UPDATE SET value = ?;
            ''', (timestamp, timestamp))
            conn.commit()
        logging.info("Last interaction timestamp updated.")
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def get_last_interaction():
    """Retrieve the last interaction timestamp safely."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM user_memory WHERE key = 'last_interaction'")
            result = cursor.fetchone()
            if result:
                try:
                    return datetime.fromisoformat(result[0])
                except ValueError:  # Handle corrupt timestamp
                    logging.error(f"Invalid timestamp format in DB: {result[0]}")
                    return None
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    return None  # Default to None if no interaction is found