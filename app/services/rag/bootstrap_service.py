import os
from tqdm import tqdm

from langchain_core.documents import Document

from app.services.rag.dataset_loader_service import load_log_dataset
from app.services.rag.preprocessing_service import clean_logs
from app.services.rag.chunking_service import chunk_logs
from app.services.rag.vector_store_service import log_vector_store
from app.core.config import settings

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

    total_indexed = 0

    for dataset_name, dataset_path in dataset_paths.items():
        logs = load_log_dataset(dataset_path, max_lines=settings.MAX_BOOTSTRAP_LINES)

        if not logs:
            print(
                f"  Skipped {dataset_name}: no {LOG_EXTENSIONS} files in {dataset_path}"
            )
            continue

        num_logs = len(logs)
        cleaned_logs = clean_logs(logs)
        del logs  # Free memory immediately

        chunks = chunk_logs(cleaned_logs, chunk_size=10)
        del cleaned_logs  # Free memory immediately

        print(
            f"  Loaded {dataset_name}: {num_logs} lines -> {len(chunks)} chunks"
        )

        batch_size = 5000
        print(f"Indexing chunks from {dataset_name} into FAISS...")
        for i in tqdm(range(0, len(chunks), batch_size), desc=f"Ingesting {dataset_name}"):
            batch_chunks = chunks[i:i + batch_size]
            batch_docs = [
                Document(
                    page_content="\n".join(chunk),
                    metadata={"source": dataset_name},
                )
                for chunk in batch_chunks
            ]
            log_vector_store.add_documents(batch_docs)

        total_indexed += len(chunks)
        del chunks  # Free memory

    if total_indexed > 0:
        log_vector_store.save()
        print(f"Knowledge base ready: {total_indexed} documents indexed")
    else:
        print(
            "Knowledge base empty: add .log or .txt files under datasets/ "
            "(e.g. datasets/hdfs/HDFS.log, datasets/bgl/BGL.log)"
        )
