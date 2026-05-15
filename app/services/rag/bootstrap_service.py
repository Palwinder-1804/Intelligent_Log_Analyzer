import os

from langchain_core.documents import Document

from app.services.rag.dataset_loader_service import (
    load_log_dataset
)

from app.services.rag.preprocessing_service import (
    clean_logs
)

from app.services.rag.chunking_service import (
    chunk_logs
)

from app.services.rag.chroma_service import (
    log_vector_store
)


DATASET_PATHS = {
    "hdfs": "datasets/hdfs",
    "bgl": "datasets/bgl",
    "apache": "datasets/apache",
    "cicids": "datasets/cicids"
}


def bootstrap_knowledge_base():

    existing_documents = log_vector_store.get()

    if existing_documents["ids"]:
        print("Knowledge base already initialized")
        return

    print("Initializing RAG knowledge base...")

    all_documents = []

    for dataset_name, dataset_path in DATASET_PATHS.items():

        if not os.path.exists(dataset_path):
            print(f"Dataset path missing: {dataset_path}")
            continue

        logs = load_log_dataset(dataset_path)

        cleaned_logs = clean_logs(logs)

        chunks = chunk_logs(
            cleaned_logs,
            chunk_size=10
        )

        for chunk in chunks:

            content = "\n".join(chunk)

            document = Document(
                page_content=content,
                metadata={
                    "source": dataset_name
                }
            )

            all_documents.append(document)

    if all_documents:

        log_vector_store.add_documents(
            all_documents
        )

        print(
            f"Added {len(all_documents)} documents to ChromaDB"
        )

    print("Knowledge base initialization completed")