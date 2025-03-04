import sqlite3
import logging
from .db_setup import DB_PATH
from .fact_management import save_user_fact, get_user_fact


def save_feedback(conversation_id, user_input, arina_reply, reason):
    """Save user feedback including reasoning."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO feedback (conversation_id, user_input, arina_reply, reason)
                VALUES (?, ?, ?, ?)
            ''', (conversation_id, user_input, arina_reply, reason))
            conn.commit()
        logging.info("Feedback saved to database.")
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def analyze_feedback(conversation_id):
    """Analyze past feedback and adjust response behavior."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT reason FROM feedback WHERE conversation_id = ?", (conversation_id,))
            feedbacks = cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
        return
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return

    if not feedbacks:
        logging.info("No feedback found for this conversation.")
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
    try:
        user_facts = {fact: get_user_fact(fact) for fact in ["response_tone", "response_length", "clarity"]}

        for issue in common_issues:
            if "robotic" in issue and user_facts["response_tone"] != "casual":
                save_user_fact("response_tone", "casual")
            elif ("too short" in issue or "brief" in issue) and user_facts["response_length"] != "long":
                save_user_fact("response_length", "long")
            elif "confusing" in issue and user_facts["clarity"] != "improve":
                save_user_fact("clarity", "improve")

    except Exception as e:
        logging.error(f"Error updating user fact: {e}")



def apply_feedback_adjustments(messages):
    """Modify responses based on stored user feedback preferences."""
    response_tone = get_user_fact("response_tone") or "neutral"
    response_length = get_user_fact("response_length") or "default"
    clarity = get_user_fact("clarity") or "normal"

    if not response_tone or not response_length or not clarity:
        logging.info("⚠️ Some user preferences are missing, using defaults.")

    for message in messages:
        if message["role"] == "system":
            if response_tone == "casual":
                message["content"] += " Make your tone friendly and engaging."
            if response_length == "long":
                message["content"] += " Provide detailed and expanded answers."
            if clarity == "improve":
                message["content"] += " Make sure your response is clear and easy to understand."
    
    return messages