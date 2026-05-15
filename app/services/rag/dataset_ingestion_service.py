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


def ingest_dataset_to_rag(
    dataset_path: str,
    dataset_name: str
):

    logs = load_log_dataset(dataset_path)

    cleaned_logs = clean_logs(logs)

    chunks = chunk_logs(cleaned_logs)

    documents = []

    for chunk in chunks:

        content = "\n".join(chunk)

        document = Document(
            page_content=content,
            metadata={
                "source": dataset_name
            }
        )

        documents.append(document)

    log_vector_store.add_documents(documents)

    return {
        "dataset": dataset_name,
        "documents_added": len(documents)
    }