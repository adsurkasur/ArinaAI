import sqlite3
import logging
from .db_setup import DB_PATH

def save_user_fact(key, value):
    """Save a user-specific fact to memory."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_memory (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = ?;
            ''', (key, value, value))
            conn.commit()
        logging.info(f"Saved user fact: {key} = {value}")
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def get_user_fact(key):
    """Retrieve a user-specific fact from memory."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM user_memory WHERE key = ?', (key,))
            result = cursor.fetchone()
            return result[0] if result else None
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return None
