import os

from langchain_core.documents import Document

from app.services.rag.dataset_loader_service import load_log_dataset
from app.services.rag.preprocessing_service import clean_logs
from app.services.rag.chunking_service import chunk_logs
from app.services.rag.chroma_service import log_vector_store

DATASETS_ROOT = "datasets"
LOG_EXTENSIONS = (".log", ".txt")


def _discover_dataset_paths() -> dict[str, str]:
    if not os.path.isdir(DATASETS_ROOT):
        return {}

    paths = {}
    for name in sorted(os.listdir(DATASETS_ROOT)):
        path = os.path.join(DATASETS_ROOT, name)
        if os.path.isdir(path):
            paths[name] = path

    return paths


def bootstrap_knowledge_base():
    existing_documents = log_vector_store.get()

    if existing_documents["ids"]:
        print("Knowledge base already initialized")
        return

    dataset_paths = _discover_dataset_paths()

    if not dataset_paths:
        print("Knowledge base bootstrap skipped: no datasets/ folders found")
        return

    print("Initializing RAG knowledge base...")

    all_documents = []

    for dataset_name, dataset_path in dataset_paths.items():
        logs = load_log_dataset(dataset_path)

        if not logs:
            print(
                f"  Skipped {dataset_name}: no {LOG_EXTENSIONS} files in {dataset_path}"
            )
            continue

        cleaned_logs = clean_logs(logs)
        chunks = chunk_logs(cleaned_logs, chunk_size=10)

        for chunk in chunks:
            content = "\n".join(chunk)
            all_documents.append(
                Document(
                    page_content=content,
                    metadata={"source": dataset_name},
                )
            )

        print(
            f"  Loaded {dataset_name}: {len(logs)} lines -> {len(chunks)} chunks"
        )

    if all_documents:
        log_vector_store.add_documents(all_documents)
        print(f"Knowledge base ready: {len(all_documents)} documents indexed")
    else:
        print(
            "Knowledge base empty: add .log or .txt files under datasets/ "
            "(e.g. datasets/hdfs/HDFS.log, datasets/bgl/BGL.log)"
        )
