import logging
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(message):
    """Generate embeddings for a message."""
    try:
        embedding = embedding_model.encode(message).tolist()
        return embedding
    except Exception as e:
        logging.error(f"Error generating embedding: {e}")
        return None