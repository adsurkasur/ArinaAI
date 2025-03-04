import sqlite3
import logging
from .db_setup import DB_PATH
from datetime import datetime

def get_interaction_trends():
    """Analyze the user's interaction patterns (hourly and day-of-week)."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT hour, day_of_week, interaction_count FROM interaction_patterns
                ORDER BY day_of_week, hour
            ''')
            trends = cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return []
    
    return trends

def get_time_of_day():
    """Determine the current time of day."""
    hour = datetime.now().hour

    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    elif 18 <= hour < 24:
        return "evening"
    else:
        return "night"

def analyze_usage_patterns():
    """Analyze interaction trends and store the most active time of day."""
    trends = get_interaction_trends()
    
    time_counts = {"morning": 0, "afternoon": 0, "evening": 0, "night": 0}
    
    for hour, _, count in trends:
        if 6 <= hour < 12:
            time_counts["morning"] += count
        elif 12 <= hour < 18:
            time_counts["afternoon"] += count
        elif 18 <= hour < 24:
            time_counts["evening"] += count
        else:
            time_counts["night"] += count

    most_active = max(time_counts, key=time_counts.get)

    # Store in memory
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_memory (key, value)
                VALUES ('most_active_time', ?)
                ON CONFLICT(key) DO UPDATE SET value = ?;
            ''', (most_active, most_active))
            conn.commit()
        logging.info(f"Stored most active time: {most_active}")
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")

    return most_active