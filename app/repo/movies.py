from fastapi import HTTPException
from app.models import Movie
from app.repo.base import BaseDAO
from app.schemas.movies import MovieCreate


class MovieDAO(BaseDAO[Movie]):
    model = Movie
    
    async def create_movie(self, movie_data: MovieCreate) -> Movie:
        """Создает новый продукт"""
        # Проверяем, не существует ли уже фильм с таким названием
        existing_item = await self.find_one_by_fields(title=movie_data.title)
        if existing_item:
            raise HTTPException(400,detail="Фильм с таким названием уже существует")
        
        new_item = await self.add(movie_data)
        await self._session.commit()
        return new_item
    

    async def get_movie(self, movie_id: int) -> Movie:
        movie = await self.find_one_or_none_by_id(movie_id)
        if not movie:
            raise HTTPException(400,detail=f"Фильма с id={movie_id} не существует!")
        return movie