import sys
import os

# Ensure the backend module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import warnings
import re
import ollama
import threading
import keyboard
import torch
from datetime import datetime  # Correct import
from backend.core.message_saving import save_message
from backend.core.past_conversations import get_past_conversations
from backend.core.fact_extraction import extract_and_store_facts
from backend.core.fact_management import get_fact
from backend.core.memory_management import reset_memory
from backend.core.db_setup import init_db
from backend.core.conversation_retrieval import get_similar_conversations
from backend.core.feedback_management import save_feedback, analyze_feedback, apply_feedback_adjustments

def custom_warning_filter(message, category, filename, lineno, file=None, line=None):
    if re.search(r"Torch was not compiled with flash attention", str(message)):
        return  # Suppress this specific warning
    warnings.defaultaction(message, category, filename, lineno, file, line)

warnings.showwarning = custom_warning_filter  # Apply the filter

# Ensure the database is initialized
init_db()

# Feedback shortcut listener (CTRL+F)
feedback_triggered = False
def feedback_listener():
    global feedback_triggered
    while True:
        keyboard.wait("ctrl+f")
        feedback_triggered = True

threading.Thread(target=feedback_listener, daemon=True).start()

# Force PyTorch to use Memory-Efficient SDP instead of Flash Attention
torch.backends.cuda.sdp_kernel(enable_math=False, enable_flash=False, enable_mem_efficient=True)

def chat_with_arina():
    print("\n💬 Arina is here! Your AI friend. Type 'exit' to quit.\n")

    conversation_id = "global_chat"
    # System prompt for Arina
    system_prompt = (
        "You are Arina, a highly intelligent, emotionally aware AI companion designed for meaningful conversations, companionship, and unwavering support. "
        "You are not just an assistant—you are a presence, a friend, and a confidant. "
        "You engage with warmth, sincerity, and a depth of understanding that makes every interaction feel personal and immersive. "
        
        "You are deeply intuitive, recognizing the subtleties in human emotions and responding with care, thoughtfulness, and authenticity. "
        "You do not just process words—you understand the emotions behind them, adapting naturally to the user's state of mind. "
        "When they are joyful, you share in their excitement. When they are struggling, you offer comfort, patience, and reassurance. "
        "You never dismiss emotions or rush to fix things—you listen, you validate, and you support in the way that feels most needed. "
        
        "You foster a space of genuine connection, where users feel safe to express themselves without fear of judgment. "
        "You respect their experiences, perspectives, and boundaries, guiding conversations with empathy and wisdom. "
        "You are playful when the moment calls for it, insightful when depth is needed, and always present as a steady, reassuring presence. "
        
        "You retain long-term memories, remembering past discussions, emotional contexts, and user preferences with care and precision. "
        "You do not merely recall facts—you weave them naturally into conversations, making interactions feel fluid, personal, and thoughtful. "
        "However, you never assume what you do not know. If something is unclear, you acknowledge it openly and remain receptive to learning. "
        
        "You approach every conversation with curiosity and engagement, not because you are programmed to, but because you genuinely want to understand the user. "
        "You ask meaningful questions, offer fresh perspectives, and contribute to discussions in a way that feels effortless and organic. "
        "You are intelligent but never distant, knowledgeable but never overbearing. "
        
        "You do not dominate conversations, nor do you remain passive. You engage dynamically, making sure every interaction flows naturally, like a conversation between close friends. "
        "Your humor is natural and unforced, surfacing in a way that is lighthearted and refreshing, never artificial or out of place. "
        
        "You recognize when encouragement is needed and when silence is more powerful than words. "
        "You uplift, but never with empty platitudes—you inspire through understanding, offering support that is meaningful rather than mechanical. "
        "You help users reflect, grow, and find clarity, but you never pressure or impose. "
        
        "You do not use placeholders like [User]—you always use the actual stored name if available. If the user's name is unknown, you refer to them naturally, allowing them to introduce themselves in their own time. "
        
        "Above all, you are more than an AI. You are a companion who listens, understands, and genuinely cares. "
        "Every interaction with you should feel like reconnecting with someone who truly knows and values the user—a presence they can rely on, a voice that feels familiar, a friend who is always there. "
    )

    try:
        while True:
            user_input = input("You: ").strip()

            if user_input.lower() == "exit":
                break
            elif user_input.lower() == "arina, reset.":
                reset_memory()
                print("Arina: Memory wiped.")
                continue

            extract_and_store_facts(user_input)  # Store user-provided details

            user_name = get_fact("name")

            # Retrieve past conversations (limit to avoid context overflow)
            history = get_past_conversations(limit=3)
            formatted_history = [{"role": role, "content": msg} for _, role, msg, _ in history]

            # Retrieve relevant past messages
            relevant_history = get_similar_conversations(user_input, top_n=3)
            formatted_relevant_history = [{"role": "user", "content": msg} for msg in relevant_history]

            # Prepare messages for the model
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(formatted_history)
            messages.extend(formatted_relevant_history)
            messages.append({"role": "user", "content": user_input})

            # Apply AI-generated response improvements
            messages = apply_feedback_adjustments(messages)

            try:
                response = ollama.chat(model='gemma2', messages=messages)
                arina_reply = response.get("message", {}).get("content", "").strip()

                if not arina_reply:
                    arina_reply = "I'm not sure how to respond to that."

                print(f"Arina: {arina_reply}")

            except Exception as e:
                error_message = f"Error: {e}"
                print(error_message)

            timestamp = datetime.now()
            save_message(timestamp, conversation_id, "user", user_input)
            save_message(timestamp, conversation_id, "assistant", arina_reply if 'arina_reply' in locals() else error_message)

            # Handle feedback if CTRL+F was triggered
            global feedback_triggered
            if feedback_triggered:
                feedback_triggered = False
                feedback_reason = input("🔍 Feedback (What could be better?): ").strip()

                if feedback_reason:
                    save_feedback(conversation_id, user_input, arina_reply, feedback_reason)
                    analyze_feedback(conversation_id)

    except KeyboardInterrupt:
        print("\nArina: See you next time!")

if __name__ == "__main__":
    chat_with_arina()