import sqlite3
import json
import os
import datetime
import logging
import spacy
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model and spaCy model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
nlp = spacy.load("en_core_web_sm")

# Define the relative path for the database
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/arina_memory.db")

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def init_db():
    """Initialize the database if it does not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Chat history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            conversation_id TEXT,
            role TEXT CHECK(role IN ('user', 'assistant')),
            message TEXT,
            embedding TEXT,
            hour INTEGER,  -- New field for hour of the interaction
            day_of_week INTEGER  -- New field for the day of the week
        )
    ''')

    # User facts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_memory (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    # Feedback table (included as before)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT,
            user_input TEXT,
            arina_reply TEXT,
            reason TEXT
        )
    ''')

    # User interaction patterns table (hourly trends)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interaction_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hour INTEGER,
            day_of_week INTEGER,
            interaction_count INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def generate_embedding(message):
    """Generate embeddings for a message."""
    try:
        embedding = embedding_model.encode(message).tolist()
        return embedding
    except Exception as e:
        logging.error(f"Error encoding message: {e}")
        return None

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

def reset_memory():
    """Wipe all stored conversations and facts."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversations")
        cursor.execute("DELETE FROM user_memory")
        cursor.execute("DELETE FROM feedback")
        cursor.execute("DELETE FROM interaction_patterns")
        conn.commit()
    logging.info("Memory reset: All data deleted.")

def create_indexes():
    """Create indexes to improve query performance."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_interaction_patterns_hour_day ON interaction_patterns(hour, day_of_week)")
        conn.commit()
    logging.info("Indexes created.")

def extract_name(text):
    """Extract name from text using spaCy."""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_and_store_facts(message):
    """Extract relevant personal facts from user input and store them."""
    name = extract_name(message)
    if name:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user_memory (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = ?", ("name", name, name))
            conn.commit()
        logging.info("Fact stored.")

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

def handle_user_input(conversation_id, role, message):
    """Handle user input and save messages."""
    timestamp = datetime.datetime.now()
    save_message(timestamp, conversation_id, role, message)

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

def get_interaction_trends():
    """Analyze the user's interaction patterns (hourly and day-of-week)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT hour, day_of_week, interaction_count FROM interaction_patterns
        ORDER BY day_of_week, hour
    ''')
    
    trends = cursor.fetchall()
    conn.close()
    
    return trends

def analyze_usage_patterns():
    """Analyze the time of day and day-of-week to detect trends."""
    trends = get_interaction_trends()
    
    morning, afternoon, evening, night = 0, 0, 0, 0
    
    for hour, _, count in trends:
        if 6 <= hour < 12:
            morning += count
        elif 12 <= hour < 18:
            afternoon += count
        elif 18 <= hour < 24:
            evening += count
        else:
            night += count
    
    # Determine the most active time of day
    time_of_day = ""
    if morning > max(afternoon, evening, night):
        time_of_day = "morning"
    elif afternoon > max(morning, evening, night):
        time_of_day = "afternoon"
    elif evening > max(morning, afternoon, night):
        time_of_day = "evening"
    else:
        time_of_day = "night"
    
    return time_of_day

def save_feedback(conversation_id, user_input, arina_reply, reason):
    """Save user feedback including reasoning."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (conversation_id, user_input, arina_reply, reason)
        VALUES (?, ?, ?, ?)
    ''', (conversation_id, user_input, arina_reply, reason))
    conn.commit()
    conn.close()

def analyze_feedback(conversation_id):
    """Analyze past feedback and adjust response behavior."""
    conn = sqlite3.connect(DB_PATH)
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

def get_similar_conversations(user_input, top_n=5):
    """Retrieve past relevant messages using semantic similarity."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT message, embedding FROM conversations')
    conversations = cursor.fetchall()
    conn.close()
    
    user_embedding = embedding_model.encode(user_input).tolist()
    similarities = []
    
    for message, embedding in conversations:
        embedding = json.loads(embedding)
        similarity = np.dot(user_embedding, embedding) / (np.linalg.norm(user_embedding) * np.linalg.norm(embedding))
        similarities.append((message, similarity))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [msg for msg, _ in similarities[:top_n]]
