from fastapi import APIRouter
from pydantic import BaseModel
import ollama
from datetime import datetime
from backend.core.message_saving import save_message
from backend.core.past_conversations import get_past_conversations
from backend.core.fact_extraction import extract_and_store_facts
from backend.core.fact_management import get_fact
from backend.core.memory_management import reset_memory
from backend.core.conversation_retrieval import get_similar_conversations
from backend.core.feedback_management import apply_feedback_adjustments
from backend.core.logging_setup import logger  # Import the logger from logging_setup.py
from backend.core.prompts import SYSTEM_PROMPT  # Import the SYSTEM_PROMPT from prompts.py

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_with_arina(request: ChatRequest):
    user_input = request.message.strip()
    logger.info(f"📩 User input: {user_input}")  # Debugging log

    if user_input.lower() == "arina, reset.":
        reset_memory()
        return {"response": "✅ Memory wiped."}

    extract_and_store_facts(user_input)
    user_name = get_fact("name")

    # Retrieve past relevant conversations
    history = get_past_conversations(limit=3)
    formatted_history = [{"role": role, "content": msg} for _, role, msg, _ in history]

    relevant_history = get_similar_conversations(user_input, top_n=3)
    formatted_relevant_history = [{"role": "user", "content": msg} for msg in relevant_history]

    # Prepare messages for AI model
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(formatted_history)
    messages.extend(formatted_relevant_history)
    messages.append({"role": "user", "content": user_input})

    messages = apply_feedback_adjustments(messages)

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
    except Exception as e:
        logger.error(f"Error saving message to database: {e}")

    logger.info(f"💬 Arina's reply: {arina_reply}")

    return {"response": arina_reply}