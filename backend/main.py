import sys
import os

# Ensure the backend module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import warnings
import re
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.core.db_setup import init_db
from backend.routes.chat import chat_with_arina
from backend.routes.feedback import collect_feedback
from backend.core.logging_setup import logger  # Import the logger from logging_setup.py

def custom_warning_filter(message, category, filename, lineno, file=None, line=None):
    if re.search(r"Torch was not compiled with flash attention", str(message)):
        return  # Suppress this specific warning
    warnings.defaultaction(message, category, filename, lineno, file, line)

warnings.showwarning = custom_warning_filter  # Apply the filter

# Ensure the database is initialized
init_db()

app = FastAPI()

# Allow frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class FeedbackRequest(BaseModel):
    user_input: str
    arina_reply: str
    reason: str

@app.post("/chat")
async def chat(request: ChatRequest):
    return await chat_with_arina(request)

@app.post("/feedback")
async def feedback(request: FeedbackRequest):
    return await collect_feedback(request)

@app.get("/")
def root():
    logger.info("✅ Arina API is running!")
    return {"message": "Arina API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)