'''
Тестовые функции — каждая проверяет один сценарий (например, создание фильма или получение несуществующего фильма).
pytest app/tests/ -v
'''
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.movie import Movie
from datetime import date
from loguru import logger

@pytest.mark.asyncio
async def test_create_movie(client: AsyncClient):
    payload = {
        "title": "Inception",
        "description": "Mind-bending thriller",
        "release_date": "2010-07-16",
        "duration": 148,
    }
    logger.info("Starting test_create_movie")
    logger.debug(f"Sending payload: {payload}")

    response = await client.post("/api/v1/movies/", json=payload)

    logger.debug(f"Received response: {response.status_code}, {response.json()}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    logger.success(f"Movie created successfully with ID: {data.get('id')}")

    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["release_date"] == payload["release_date"]
    assert data["duration"] == payload["duration"]
    assert "id" in data
    logger.info("Finished test_create_movie")



@pytest.mark.asyncio
async def test_get_movie(client: AsyncClient, db_session: AsyncSession):
    movie = Movie(
        title="The Matrix",
        description="Sci-fi action film",
        release_date=date(1999, 3, 31),
        duration=136,
    )
    logger.info("Starting test_get_movie")
    logger.debug(f"Creating test movie: {movie.title}")

    db_session.add(movie)
    await db_session.commit()  # Фиксируем изменения
    logger.debug(f"Movie committed to database with ID: {movie.id}")

    response = await client.get(f"/api/v1/movies/{movie.id}")

    logger.debug(f"GET response: {response.status_code}, {response.json()}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    logger.success(f"Successfully retrieved movie: {data}")

    assert data["title"] == "The Matrix"
    assert data["id"] == movie.id
    assert data["release_date"] == "1999-03-31"
    logger.info("Finished test_get_movie")



@pytest.mark.asyncio
async def test_get_movie_not_found(client: AsyncClient):
    non_existent_id = 999999
    logger.info(f"Starting test_get_movie_not_found with ID: {non_existent_id}")

    response = await client.get(f"/api/v1/movies/{non_existent_id}")
    
    logger.debug(f"GET response for non-existent movie: {response.status_code}, {response.json()}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    error_detail = response.json()["detail"]
    logger.success(f"Correctly received error: {error_detail}")
    assert error_detail == "Movie not found"

    logger.info("Finished test_get_movie_not_found")