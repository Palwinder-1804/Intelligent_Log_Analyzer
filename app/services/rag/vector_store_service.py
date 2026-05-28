import os
import faiss
import torch
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore

from app.services.rag.embedding_service import embedding_model

VECTOR_DB_PATH = "vector_store"


class VectorStoreWrapper:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.path = os.path.join(VECTOR_DB_PATH, collection_name)
        self._store = None
        self._is_gpu = False

    @property
    def store(self) -> FAISS:
        if self._store is None:
            if os.path.exists(os.path.join(self.path, "index.faiss")):
                # Load the existing FAISS index
                self._store = FAISS.load_local(
                    self.path, 
                    embedding_model, 
                    allow_dangerous_deserialization=True
                )
            else:
                # Initialize an empty FAISS index
                # We need the dimension of the embeddings. We can get it by embedding a dummy string.
                dim = len(embedding_model.embed_query("test"))
                index = faiss.IndexFlatL2(dim)
                
                self._store = FAISS(
                    embedding_function=embedding_model,
                    index=index,
                    docstore=InMemoryDocstore(),
                    index_to_docstore_id={},
                )
                
            # Attempt to move the index to GPU if available
            if torch.cuda.is_available():
                try:
                    res = faiss.StandardGpuResources()
                    self._store.index = faiss.index_cpu_to_gpu(res, 0, self._store.index)
                    self._is_gpu = True
                    print(f"[{self.collection_name}] FAISS index moved to GPU.")
                except AttributeError:
                    # faiss-cpu does not have StandardGpuResources
                    self._is_gpu = False
                except Exception as e:
                    self._is_gpu = False
                    print(f"[{self.collection_name}] Could not move FAISS index to GPU: {e}")

        return self._store

    def add_documents(self, documents: list):
        if documents:
            self.store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 4):
        return self.store.similarity_search(query, k=k)

    def get(self):
        # A simple mock to replace ChromaDB's get() method checking for existing docs
        return {"ids": list(self.store.index_to_docstore_id.values())}

    def save(self):
        if self._store is not None:
            os.makedirs(self.path, exist_ok=True)
            
            if self._is_gpu:
                try:
                    # We must move the index back to CPU to save it to disk
                    cpu_index = faiss.index_gpu_to_cpu(self._store.index)
                    original_index = self._store.index
                    self._store.index = cpu_index
                    self._store.save_local(self.path)
                    self._store.index = original_index
                except Exception as e:
                    print(f"[{self.collection_name}] Error saving GPU index: {e}. Falling back to default save.")
                    self._store.save_local(self.path)
            else:
                self._store.save_local(self.path)


log_vector_store = VectorStoreWrapper("log_collection")
incident_vector_store = VectorStoreWrapper("incident_collection")
security_vector_store = VectorStoreWrapper("security_collection")
