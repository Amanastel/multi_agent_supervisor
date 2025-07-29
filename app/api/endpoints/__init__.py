# app/api/endpoints/__init__.py

from fastapi import APIRouter
from app.api.endpoints import calendar, gmail, unified, supervisor

router = APIRouter()
router.include_router(supervisor.router)  # Supervisor first (main entry point)
router.include_router(calendar.router)
router.include_router(gmail.router)
router.include_router(unified.router)
