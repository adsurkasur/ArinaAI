import sqlite3
import logging
from .db_setup import DB_PATH

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