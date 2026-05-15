from langchain_ollama import OllamaLLM

from app.core.config import settings


llm = OllamaLLM(
    model=settings.OLLAMA_MODEL
)