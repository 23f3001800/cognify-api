import os, logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from config import get_settings
from routers import chat, ingest, embed, summarise
from middleware.logging import LoggingMiddleware

settings = get_settings()

# Activate LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"]  = settings.langchain_tracing_v2
os.environ["LANGCHAIN_API_KEY"]     = settings.langchain_api_key
os.environ["LANGCHAIN_PROJECT"]     = settings.langchain_project

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-load embedding model at startup (not on first request)
    from sentence_transformers import SentenceTransformer
    app.state.embedder = SentenceTransformer(settings.embed_model)
    logging.info(f"Embedding model loaded: {settings.embed_model}")
    yield
    logging.info("Shutting down")

app = FastAPI(
    title="AI Engineering API",
    description="Production-grade LLM API — RAG, chat, embeddings, summarisation",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(chat.router,      prefix="/chat",     tags=["Chat"])
app.include_router(ingest.router,    prefix="",          tags=["Ingestion"])
app.include_router(embed.router,     prefix="/embed",    tags=["Embeddings"])
app.include_router(summarise.router, prefix="/summarise",tags=["Summarisation"])

@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok", "env": settings.environment,
            "model": settings.llm_model}

@app.get("/ready", tags=["System"])
async def ready(request):
    if not hasattr(request.app.state, "embedder"):
        from fastapi import HTTPException
        raise HTTPException(503, "Not ready — models still loading")
    return {"ready": True}