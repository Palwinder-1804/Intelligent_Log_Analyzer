from sentence_transformers import SentenceTransformer

from app.core.config import settings


embedding_model = SentenceTransformer(
    settings.EMBEDDING_MODEL
)


def generate_embedding(log: str):

    embedding = embedding_model.encode(
        [log]
    )[0]

    return embedding