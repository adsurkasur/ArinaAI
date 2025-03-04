import sqlite3
import logging
from .db_setup import DB_PATH

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