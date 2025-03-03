import sqlite3
from .db_setup import DB_PATH

def save_fact(key, value):
    """Save a fact to the user memory."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert or update the fact in the user_memory table
    cursor.execute('''
        INSERT INTO user_memory (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = ?;
    ''', (key, value, value))

    conn.commit()
    conn.close()

def get_fact(key):
    """Retrieve a fact from the user memory."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT value FROM user_memory WHERE key = ?', (key,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    return None