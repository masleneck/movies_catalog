from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_session
from app.models.movie import Movie
from app.schemas.movies import MovieCreate, MovieResponse

router = APIRouter(prefix="/movies", tags=["movies"])

@router.post("/", response_model=MovieResponse)
async def create_movie(movie: MovieCreate, session: AsyncSession = Depends(get_async_session)):
    db_movie = Movie(
        title=movie.title,
        description=movie.description,
        release_date=movie.release_date,
        duration=movie.duration
    )
    session.add(db_movie)
    await session.commit()
    await session.refresh(db_movie)
    return db_movie

@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_async_session)):
    movie = await db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie