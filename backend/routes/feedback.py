from fastapi import APIRouter
from pydantic import BaseModel
from backend.main import logger  # Import the logger from main.py
from backend.core.feedback_management import save_feedback, analyze_feedback

router = APIRouter()

class FeedbackRequest(BaseModel):
    message: str

@router.post("/feedback")
async def collect_feedback(request: FeedbackRequest):
    feedback_reason = request.message.strip()
    
    if feedback_reason:
        save_feedback("global_chat", "user_input", "arina_reply", feedback_reason)
        analyze_feedback("global_chat")
        logger.info(f"📝 Feedback received: {feedback_reason}")
        return {"message": "✅ Feedback recorded."}
    
    return {"message": "⚠️ No feedback provided."}