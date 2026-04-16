from fastapi import FastAPI
from app.routes import health
from app.routes import ingest

app = FastAPI(title="RAG System")

app.include_router(health.router)
app.include_router(ingest.router)