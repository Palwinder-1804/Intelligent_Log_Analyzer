import os
import sys
import traceback

# Optimize thread pool sizes for CPU libraries to minimize memory usage
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

# Add the current directory to sys.path to allow imports from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.rag.bootstrap_service import bootstrap_knowledge_base

if __name__ == "__main__":
    print("Starting RAG ingestion process...")
    try:
        bootstrap_knowledge_base()
        print("RAG ingestion completed successfully.")
    except Exception as exc:
        print(f"Error during RAG ingestion: {exc}")
        traceback.print_exc()
