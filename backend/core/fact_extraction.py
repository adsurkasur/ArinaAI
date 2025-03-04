import sqlite3
import logging
import spacy
from .db_setup import DB_PATH

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_name(text):
    """Extract name from text using spaCy."""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_and_store_facts(message):
    """Extract relevant personal facts from user input and store them."""
    name = extract_name(message)
    if name:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO user_memory (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = ?", ("name", name, name))
                conn.commit()
            logging.info("Fact stored.")
        except sqlite3.Error as e:
            logging.error(f"SQLite error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")