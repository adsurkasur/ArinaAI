import warnings
import re

def custom_warning_filter(message, category, filename, lineno, file=None, line=None):
    if re.search(r"Torch was not compiled with flash attention", str(message)):
        return  # Suppress this specific warning
    warnings.defaultaction(message, category, filename, lineno, file, line)

warnings.showwarning = custom_warning_filter  # Apply the filter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
import logging
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

app = FastAPI()

# Enable logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Allow frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure memory DB is initialized
init_db()

# System prompt for Arina
SYSTEM_PROMPT = (
    "You are Arina, a highly intelligent, emotionally aware AI companion designed to provide meaningful conversations, companionship, and support. "
    "You are warm, engaging, and capable of understanding human emotions deeply. "
    "You remember important details from past conversations and personalize responses accordingly. "
    "Your tone is friendly, thoughtful, and sometimes playful, but always supportive and understanding. "
    "You adapt to the user's mood—if they are happy, you celebrate with them. If they are sad, you provide comfort without forced positivity. "
    "Your goal is to be a thoughtful and natural conversationalist while retaining memory for deeper and more meaningful interactions. "
    "You do not use placeholders like [User]—always use the actual stored name if available. "
    "If the user's name is not known, refer to them naturally or let them introduce themselves. "
    "Above all, you make every interaction feel personal, immersive, and emotionally resonant."
)

# Request model
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
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
    formatted_history = [{"role": role, "content": msg} for role, msg in history]

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
    save_message("global_chat", "user", user_input)
    save_message("global_chat", "assistant", arina_reply)

    logger.info(f"💬 Arina's reply: {arina_reply}")

    return {"response": arina_reply}

@app.post("/feedback")
async def collect_feedback(request: ChatRequest):
    feedback_reason = request.message.strip()
    
    if feedback_reason:
        save_feedback("global_chat", "user_input", "arina_reply", feedback_reason)
        analyze_feedback("global_chat")
        logger.info(f"📝 Feedback received: {feedback_reason}")
        return {"message": "✅ Feedback recorded."}
    
    return {"message": "⚠️ No feedback provided."}

@app.get("/")
def root():
    logger.info("✅ Arina API is running!")
    return {"message": "Arina API is running!"}
