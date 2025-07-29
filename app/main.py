from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(title="Multi-Agent Supervisor System")

app.include_router(api_router, prefix="/api")
