import sqlite3
import json
import logging
from datetime import datetime
from .embedding import generate_embedding
from .db_setup import DB_PATH

def save_message(timestamp, conversation_id, role, message):
    """Save conversation history and its embedding with precise timestamp."""
    embedding = generate_embedding(message)
    if embedding is None:
        return
    
    hour = timestamp.hour
    day_of_week = timestamp.weekday()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (timestamp, conversation_id, role, message, embedding, hour, day_of_week)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, conversation_id, role, message, json.dumps(embedding), hour, day_of_week))
        conn.commit()

    logging.info("Message saved to database.")

def save_multiple_messages(messages):
    """Batch insert multiple messages."""
    data = []
    for message in messages:
        timestamp, conversation_id, role, msg = message
        embedding = generate_embedding(msg)
        if embedding:
            hour = timestamp.hour
            day_of_week = timestamp.weekday()
            data.append((timestamp, conversation_id, role, msg, json.dumps(embedding), hour, day_of_week))

    if data:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.executemany('''
                INSERT INTO conversations (timestamp, conversation_id, role, message, embedding, hour, day_of_week)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', data)
            conn.commit()
        logging.info("Batch of messages saved to database.")