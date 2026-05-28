import numpy as np
from app.services.rag.embedding_service import embedding_model


def generate_embedding(log: str):
    # Reuse the langchain HuggingFaceEmbeddings model initialized in embedding_service.py
    # to avoid loading the model weights twice in memory.
    embedding = embedding_model.embed_query(log)
    return np.array(embedding)