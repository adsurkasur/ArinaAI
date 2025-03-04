from datetime import datetime
import logging
from .message_saving import save_message

def handle_user_input(conversation_id, role, message):
    """Handle user input and save messages."""
    timestamp = datetime.now()
    try:
        save_message(timestamp, conversation_id, role, message)
        logging.info(f"User input handled and saved: {message}")
    except Exception as e:
        logging.error(f"Error handling user input: {e}")