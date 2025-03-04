import sqlite3
import logging
from .db_setup import DB_PATH

def get_past_conversations(limit=5):
    """Retrieve past conversations limited to the most recent ones."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT conversation_id, role, message, timestamp FROM conversations
            ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        conversations = cursor.fetchall()
        return conversations
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return []
    finally:
        if conn:
            conn.close()