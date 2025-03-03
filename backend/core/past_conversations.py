import sqlite3
from .db_setup import DB_PATH

def get_past_conversations(limit=5):
    """Retrieve past conversations limited to the most recent ones."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT conversation_id, role, message, timestamp FROM conversations
        ORDER BY timestamp DESC LIMIT ?
    ''', (limit,))
    conversations = cursor.fetchall()
    conn.close()
    return conversations