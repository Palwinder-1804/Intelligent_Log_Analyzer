from langchain_chroma import Chroma

from app.services.rag.embedding_service import (
    embedding_model
)


VECTOR_DB_PATH = "vector_store"


log_vector_store = Chroma(
    collection_name="log_collection",
    embedding_function=embedding_model,
    persist_directory=VECTOR_DB_PATH
)


incident_vector_store = Chroma(
    collection_name="incident_collection",
    embedding_function=embedding_model,
    persist_directory=VECTOR_DB_PATH
)


security_vector_store = Chroma(
    collection_name="security_collection",
    embedding_function=embedding_model,
    persist_directory=VECTOR_DB_PATH
)