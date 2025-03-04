from fastapi import APIRouter
from pydantic import BaseModel
import ollama
from datetime import datetime
from backend.core.message_saving import save_message
from backend.core.past_conversations import get_past_conversations
from backend.core.fact_extraction import extract_and_store_facts
from backend.core.memory_management import reset_memory, get_last_interaction, update_last_interaction
from backend.core.fact_management import get_user_fact, save_user_fact
from backend.core.conversation_retrieval import get_similar_conversations
from backend.core.feedback_management import apply_feedback_adjustments
from backend.core.logging_setup import logger  # Import the logger from logging_setup.py
from backend.core.prompts import SYSTEM_PROMPT  # Import the SYSTEM_PROMPT from prompts.py
from backend.core.interaction_trends import get_time_of_day
from backend.core.search_utils import needs_web_search, search_duckduckgo

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_with_arina(request: ChatRequest):
    user_input = request.message.strip()
    logger.info(f"📩 User input: {user_input}")

    # Check if the user's query requires a web search
    if needs_web_search(user_input):
        logger.info(f"🌍 Web search triggered for: {user_input}")
        search_summary, search_links = search_duckduckgo(user_input)
        
        search_context = f"I found the following information: {search_summary}"
        if search_links:
            search_context += f" (Related links: {', '.join(search_links)})"
        
        dynamic_prompt = (
            f"User asked: {user_input}\n"
            f"{search_context}\n"
            f"Based on this, please provide a natural, conversational response "
            f"that integrates this information without listing out links verbatim."
        )
        
        response = ollama.chat(model="gemma2", messages=[
            {"role": "system", "content": dynamic_prompt}
        ])
        arina_reply = response.get("message", {}).get("content", "").strip()
        
        if not arina_reply:
            arina_reply = "I'm not sure how to respond to that, but I'm here to help."
        return {"response": arina_reply}
    
    if user_input.lower() == "arina, reset.":
        reset_memory()
        return {"response": "✅ Memory wiped."}

    extract_and_store_facts(user_input)
    user_name = get_user_fact("name")

    # Retrieve past relevant conversations
    history = get_past_conversations(limit=3)
    formatted_history = [{"role": role, "content": msg} for _, role, msg, _ in history]

    relevant_history = get_similar_conversations(user_input, top_n=3)
    formatted_relevant_history = [{"role": "user", "content": msg} for msg in relevant_history]

    # Get last interaction time
    last_interaction = get_last_interaction()
    current_time_of_day = get_time_of_day()

    # Get user's most active time
    most_active_time = get_user_fact("most_active_time") or "unknown"

    # Generate time-aware context for Arina dynamically
    time_context = f"Be aware that it is {current_time_of_day}. Adjust the conversation naturally based on this."

    if most_active_time and most_active_time != "unknown":
        time_context += f" The user is usually active in the {most_active_time}. Adjust your tone accordingly."

    time_gap = None
    if last_interaction:
        time_gap = (datetime.now() - last_interaction).total_seconds()

    if time_gap is not None:
        if time_gap > 86400:  
            time_context += " The user has returned after a long time. Let them feel welcomed without explicitly mentioning the gap."
        elif time_gap > 43200:  
            time_context += f" Since it is {current_time_of_day}, ensure your response flows accordingly."
        elif time_gap > 18000:  
            time_context += f" Adapt the conversation for a {current_time_of_day} chat naturally."
        else:
            time_context += " The conversation is active; keep it engaging."

    # Apply feedback adjustments to system prompt
    system_prompt_adjusted = apply_feedback_adjustments([{"role": "system", "content": SYSTEM_PROMPT}])[0]["content"]
    messages = [{"role": "system", "content": system_prompt_adjusted + "\n\n" + time_context}]
    messages.extend(formatted_history)
    messages.extend(formatted_relevant_history)
    messages.append({"role": "user", "content": user_input})

    try:
        response = ollama.chat(model="gemma2", messages=messages)
        logger.info(f"🧠 Ollama raw response: {response}")  # Debugging log

        # Extract response message
        arina_reply = response.get("message", {}).get("content", "").strip()

        if not arina_reply:
            logger.warning("⚠️ Empty response from Ollama!")
            arina_reply = "🤖 I'm not sure how to respond to that."

    except Exception as e:
        logger.error(f"🚨 Error connecting to Ollama: {e}")
        arina_reply = "⚠️ Arina is having trouble responding. Try again."

    # Save conversation to memory
    try:
        save_message(datetime.now(), "global_chat", "user", user_input)
        save_message(datetime.now(), "global_chat", "assistant", arina_reply)
        update_last_interaction()

        # Update most active time based on latest interaction
        current_hour = datetime.now().hour
        if 6 <= current_hour < 12:
            save_user_fact("most_active_time", "morning")
        elif 12 <= current_hour < 18:
            save_user_fact("most_active_time", "afternoon")
        elif 18 <= current_hour < 24:
            save_user_fact("most_active_time", "evening")
        else:
            save_user_fact("most_active_time", "night")

    except Exception as e:
        logger.error(f"Error saving message to database: {e}")

    logger.info(f"💬 Arina's reply: {arina_reply}")

    return {"response": arina_reply}