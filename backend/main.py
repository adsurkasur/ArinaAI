import sys
import os

# Ensure the backend module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import warnings
import re
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.core.db_setup import init_db
from backend.routes.chat import chat_with_arina
from backend.routes.feedback import collect_feedback

def custom_warning_filter(message, category, filename, lineno, file=None, line=None):
    if re.search(r"Torch was not compiled with flash attention", str(message)):
        return  # Suppress this specific warning
    warnings.defaultaction(message, category, filename, lineno, file, line)

warnings.showwarning = custom_warning_filter  # Apply the filter

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

# Include routes
app.include_router(chat_with_arina.router)
app.include_router(collect_feedback.router)

@app.get("/")
def root():
    logger.info("✅ Arina API is running!")
    return {"message": "Arina API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)