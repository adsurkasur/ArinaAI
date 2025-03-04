from fastapi import APIRouter
from pydantic import BaseModel
from backend.core.logging_setup import logger  # Import the logger from logging_setup.py
from backend.core.feedback_management import save_feedback, analyze_feedback

router = APIRouter()

class FeedbackRequest(BaseModel):
    user_input: str
    arina_reply: str
    reason: str

@router.post("/feedback")
async def collect_feedback(request: FeedbackRequest):
    logger.info(f"📩 Feedback received: {request.reason}")
    # Process the feedback here
    return {"response": "Feedback received"}