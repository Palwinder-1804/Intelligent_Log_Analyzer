from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.api.routes.auth import router as auth_router
from app.api.routes.user import router as user_router
from app.api.routes.logs import router as logs_router
from app.api.routes.anomaly import router as anomaly_router
from app.api.routes.rag import router as rag_router
from app.api.routes.llm import router as llm_router
from app.services.rag.bootstrap_service import bootstrap_knowledge_base
from app.api.routes.rca import router as rca_router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    bootstrap_knowledge_base()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(logs_router)
app.include_router(anomaly_router)
app.include_router(rag_router)
app.include_router(llm_router)
app.include_router(rca_router)

@app.get("/")
async def root():
    return {
        "message": "Intelligent Log Analysis API Running"
    }