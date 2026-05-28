import torch
from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings

# Restrict PyTorch CPU thread pools to save CPU cycles and RAM overhead
torch.set_num_threads(1)

device = "cuda" if torch.cuda.is_available() else "cpu"

embedding_model = HuggingFaceEmbeddings(
    model_name=settings.EMBEDDING_MODEL,
    model_kwargs={'device': device}
)
