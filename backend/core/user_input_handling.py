from datetime import datetime
from .message_saving import save_message

def handle_user_input(conversation_id, role, message):
    """Handle user input and save messages."""
    timestamp = datetime.now()
    save_message(timestamp, conversation_id, role, message)