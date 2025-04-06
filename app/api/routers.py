from fastapi import APIRouter
from app.api.endpoints import movie_router

main_router = APIRouter()
main_router.include_router(movie_router)
