from fastapi import APIRouter
from app.api.endpoints import files, analysis

api_router = APIRouter()
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
