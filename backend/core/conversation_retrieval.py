import sqlite3
import json
import numpy as np
from .embedding import generate_embedding
from .db_setup import DB_PATH

def find_similar_conversations(query_message):
    """Find similar conversations based on embedding similarity."""
    query_embedding = generate_embedding(query_message)
    if query_embedding is None:
        return []

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT message, embedding FROM conversations')
        conversations = cursor.fetchall()
    
    similarities = []
    for message, embedding in conversations:
        embedding = json.loads(embedding)
        similarity = np.dot(query_embedding, embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(embedding))
        similarities.append((message, similarity))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [msg for msg, _ in similarities[:5]]

def get_similar_conversations(user_input, top_n=5):
    """Retrieve past relevant messages using semantic similarity."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT message, embedding FROM conversations')
    conversations = cursor.fetchall()
    conn.close()
    
    user_embedding = generate_embedding(user_input)
    if user_embedding is None:
        return []
    
    similarities = []
    
    for message, embedding in conversations:
        embedding = json.loads(embedding)
        similarity = np.dot(user_embedding, embedding) / (np.linalg.norm(user_embedding) * np.linalg.norm(embedding))
        similarities.append((message, similarity))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [msg for msg, _ in similarities[:top_n]]