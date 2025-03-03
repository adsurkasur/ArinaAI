import sqlite3
from .fact_management import save_fact, get_fact
from .db_setup import DB_PATH

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