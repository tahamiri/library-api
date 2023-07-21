from fastapi import APIRouter

from app.api.endpoints import book
from app.api.endpoints import authentication

api_router = APIRouter()

api_router.include_router(authentication.router, prefix="/auth", tags=["user"])
api_router.include_router(book.router, prefix="/api", tags=["book"])
