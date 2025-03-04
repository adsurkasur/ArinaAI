import sqlite3
import logging
from .db_setup import DB_PATH

def save_fact(key, value):
    """Save a fact to the user memory."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_memory (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = ?;
            ''', (key, value, value))
            conn.commit()
        logging.info("Fact saved to database.")
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def get_fact(key):
    """Retrieve a fact from the user memory."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM user_memory WHERE key = ?', (key,))
            result = cursor.fetchone()
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

    if result:
        return result[0]
    return None