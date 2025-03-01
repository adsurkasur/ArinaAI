import sqlite3
import time
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def init_db():
    """Initialize the database if it does not exist."""
    conn = sqlite3.connect("/d:/Projects/ArinaAI/backend/data/arina_memory.db")
    cursor = conn.cursor()

    # Chat history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            conversation_id TEXT,
            role TEXT CHECK(role IN ('user', 'assistant')),
            message TEXT,
            embedding TEXT
        )
    ''')

    # User facts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_memory (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    # Feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT,
            user_input TEXT,
            arina_reply TEXT,
            reason TEXT
        )
    ''')

    conn.commit()
    conn.close()

def save_message(conversation_id, role, message):
    """Save conversation history and its embedding."""
    if role not in ["user", "assistant"]:
        return
    
    embedding = embedding_model.encode(message).tolist()
    
    conn = sqlite3.connect("/d:/Projects/ArinaAI/backend/data/arina_memory.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conversations (timestamp, conversation_id, role, message, embedding)
        VALUES (?, ?, ?, ?, ?)
    ''', (time.time(), conversation_id, role, message, json.dumps(embedding)))
    conn.commit()
    conn.close()
    
def get_past_conversations(limit=5):
    """Retrieve past conversations limited to the most recent ones."""
    conn = sqlite3.connect("/d:/Projects/ArinaAI/backend/data/arina_memory.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT role, message FROM conversations 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (limit,))
    
    conversations = cursor.fetchall()
    conn.close()
    
    return conversations

def save_fact(key, value):
    """Store a user fact in memory."""
    conn = sqlite3.connect("/d:/Projects/ArinaAI/backend/data/arina_memory.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_memory (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
    ''', (key, value))
    conn.commit()
    conn.close()

def get_fact(key):
    """Retrieve a stored fact from user memory."""
    conn = sqlite3.connect("/d:/Projects/ArinaAI/backend/data/arina_memory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM user_memory WHERE key = ?", (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def extract_and_store_facts(user_input):
    """Extract relevant personal facts from user input and store them."""
    if "my name is" in user_input.lower():
        name = user_input.split("my name is")[-1].strip().split()[0]
        save_fact("name", name)

def get_similar_conversations(user_input, top_n=5):
    """Retrieve past relevant messages using semantic similarity."""
    user_embedding = embedding_model.encode(user_input)

    conn = sqlite3.connect("/d:/Projects/ArinaAI/backend/data/arina_memory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT message, embedding FROM conversations")
    
    all_conversations = cursor.fetchall()
    conn.close()

    if not all_conversations:
        return []

    similarities = []
    for message, stored_embedding in all_conversations:
        stored_vector = np.array(json.loads(stored_embedding))
        similarity = np.dot(user_embedding, stored_vector) / (np.linalg.norm(user_embedding) * np.linalg.norm(stored_vector))
        similarities.append((message, similarity))

    # Sort by similarity score and return top_n results
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [msg for msg, _ in similarities[:top_n]]

def save_feedback(conversation_id, user_input, arina_reply, reason):
    """Save user feedback including reasoning."""
    conn = sqlite3.connect("/d:/Projects/ArinaAI/backend/data/arina_memory.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (conversation_id, user_input, arina_reply, reason)
        VALUES (?, ?, ?, ?)
    ''', (conversation_id, user_input, arina_reply, reason))
    conn.commit()
    conn.close()

def analyze_feedback(conversation_id):
    """Analyze past feedback and adjust response behavior."""
    conn = sqlite3.connect("/d:/Projects/ArinaAI/backend/data/arina_memory.db")
    cursor = conn.cursor()
    
    # Get all feedback for this conversation
    cursor.execute("SELECT reason FROM feedback WHERE conversation_id = ?", (conversation_id,))
    feedbacks = cursor.fetchall()
    
    conn.close()

    if not feedbacks:
        return
    
    issue_counts = {}

    # Process feedback to detect common complaints
    for (reason,) in feedbacks:
        words = reason.lower().split()
        for word in words:
            if word in issue_counts:
                issue_counts[word] += 1
            else:
                issue_counts[word] = 1

    # Identify most common complaints
    common_issues = sorted(issue_counts, key=issue_counts.get, reverse=True)[:3]

    # Apply personalized feedback adjustments
    for issue in common_issues:
        if "robotic" in issue:
            save_fact("response_tone", "casual")
        elif "too short" in issue or "brief" in issue:
            save_fact("response_length", "long")
        elif "confusing" in issue:
            save_fact("clarity", "improve")
    
def apply_feedback_adjustments(messages):
    """Modify responses based on stored user feedback preferences."""
    response_tone = get_fact("response_tone")
    response_length = get_fact("response_length")
    clarity = get_fact("clarity")

    for message in messages:
        if message["role"] == "system":
            if response_tone == "casual":
                message["content"] += " Make your tone friendly and engaging."
            if response_length == "long":
                message["content"] += " Provide detailed and expanded answers."
            if clarity == "improve":
                message["content"] += " Make sure your response is clear and easy to understand."
    
    return messages

def reset_memory():
    """Wipe all stored conversations and facts."""
    conn = sqlite3.connect("/d:/Projects/ArinaAI/backend/data/arina_memory.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM conversations")
    cursor.execute("DELETE FROM user_memory")
    
    conn.commit()
    conn.close()
