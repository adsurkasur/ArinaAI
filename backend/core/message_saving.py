import sqlite3
import json
import logging
from backend.core.embedding import generate_embedding  # Adjusted import path
import os

# Define the relative path for the database
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/arina_memory.db")

def save_message(timestamp, conversation_id, role, message):
    """Save conversation history and its embedding."""
    embedding = generate_embedding(message)
    if embedding is None:
        return
    
    hour = timestamp.hour
    day_of_week = timestamp.weekday()

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO conversations (timestamp, conversation_id, role, message, embedding, hour, day_of_week)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp, conversation_id, role, message, json.dumps(embedding), hour, day_of_week))
            conn.commit()
        logging.info("Message saved to database.")
    except Exception as e:
        logging.error(f"Error saving message to database: {e}")

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
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.executemany('''
                    INSERT INTO conversations (timestamp, conversation_id, role, message, embedding, hour, day_of_week)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', data)
                conn.commit()
            logging.info("Batch of messages saved to database.")
        except Exception as e:
            logging.error(f"Error saving batch of messages to database: {e}")