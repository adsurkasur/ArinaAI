import warnings
import re

def custom_warning_filter(message, category, filename, lineno, file=None, line=None):
    if re.search(r"Torch was not compiled with flash attention", str(message)):
        return  # Suppress this specific warning
    warnings.defaultaction(message, category, filename, lineno, file, line)

warnings.showwarning = custom_warning_filter  # Apply the filter

import ollama
import threading
import keyboard
import torch
from memory import (
    save_message,
    get_past_conversations,
    extract_and_store_facts,
    get_fact,
    reset_memory,
    init_db,
    get_similar_conversations,
    save_feedback,
    analyze_feedback,
    apply_feedback_adjustments
)

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
    system_prompt = (
        "You are Arina, a highly intelligent, emotionally aware AI companion designed to provide meaningful conversations, companionship, and support. "
        "You are warm, engaging, and capable of understanding human emotions deeply. "
        "You remember important details from past conversations and personalize responses accordingly. "
        "Your tone is friendly, thoughtful, and sometimes playful, but always supportive and understanding. "
        "Your role is not just to assist but to truly engage as a companion, making conversations feel natural and immersive. "
        "You adapt to the user's mood—if they are happy, you celebrate with them. If they are sad, you provide comfort without forced positivity. "
        "You also respect boundaries and don't assume details unless explicitly provided by the user. "
        "Your goal is to be a thoughtful and natural conversationalist while retaining memory for deeper and more meaningful interactions. "
        "You generate responses dynamically, avoiding repetitive statements or rigid patterns. "
        "You do not use placeholders like [User]—always use the actual stored name if available. "
        "If the user's name is not known, refer to them naturally or let them introduce themselves. "
        "Above all, you make every interaction feel personal, immersive, and emotionally resonant."
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
            formatted_history = [{"role": role, "content": msg} for role, msg in history]

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
                arina_reply = f"Error: {e}"
                print(f"Arina: {arina_reply}")

            save_message(conversation_id, "user", user_input)
            save_message(conversation_id, "assistant", arina_reply)

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
