import os
import logging
from backend.core.db_setup import DB_PATH, init_db

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def reset_database():
    """Reset the database by deleting the existing file and reinitializing it."""
    try:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            logger.info("Existing database file deleted.")
        else:
            logger.info("No existing database file found.")

        # Reinitialize the database
        init_db()
        logger.info("Database reinitialized successfully.")
    except Exception as e:
        logger.error(f"Error resetting database: {e}")

# Run the database reset
reset_database()