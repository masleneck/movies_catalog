from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_session
from app.repo.movies import MovieDAO
from app.schemas.movies import MovieCreate, MovieResponse

router = APIRouter(prefix="/movies", tags=["movies"])

@router.post("/create_movie", response_model=MovieResponse, summary="Создать фильм")
async def create_movie(movie_data: MovieCreate, session: AsyncSession = Depends(get_async_session)):
    return await MovieDAO(session).create_movie(movie_data)

@router.get("/{movie_id}", response_model=MovieResponse, summary="Найти фильм по id")
async def get_movie(movie_id: int, session: AsyncSession = Depends(get_async_session)):
    return await MovieDAO(session).get_movie(movie_id)
