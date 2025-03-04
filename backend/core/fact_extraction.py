import sqlite3
import logging
import spacy
from .fact_management import save_user_fact

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
    """Extract personal facts like name, location, and interests."""
    doc = nlp(message)
    
    # Extract name
    name = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), None)
    if name:
        clean_name = name.split(".")[0]  # Store only the first sentence
        save_user_fact("name", clean_name)
        logging.info(f"User name '{name}' stored in memory.")
    
    # Extract location
    location = next((ent.text for ent in doc.ents if ent.label_ == "GPE"), None)
    if location:
        save_user_fact("location", location)
        logging.info(f"User location '{location}' stored in memory.")

    # Extract hobbies (simple keyword detection)
    hobbies = []
    hobby_keywords = ["love", "enjoy", "like", "hobby", "passion"]
    for token in doc:
        if token.text.lower() in hobby_keywords and token.head.pos_ == "NOUN":
            hobbies.append(token.head.text)

    if hobbies:
        save_user_fact("hobbies", ", ".join(hobbies))
        logging.info(f"User hobbies '{', '.join(hobbies)}' stored in memory.")
