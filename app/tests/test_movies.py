'''
Тестовые функции — каждая проверяет один сценарий (например, создание фильма или получение несуществующего фильма).
pytest app/tests/ -v
'''
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.movie import Movie
from datetime import date

@pytest.mark.asyncio
async def test_create_movie(client: AsyncClient, db_session: AsyncSession):
    payload = {
        "title": "Inception",
        "description": "Mind-bending thriller",
        "release_date": "2010-07-16",
        "duration": 148,
    }

    response = await client.post("/api/v1/movies/", json=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["release_date"] == payload["release_date"]
    assert data["duration"] == payload["duration"]
    assert "id" in data

    movie = await db_session.get(Movie, data["id"])
    assert movie is not None
    assert movie.title == "Inception"

@pytest.mark.asyncio
async def test_get_movie(client: AsyncClient, db_session: AsyncSession):
    movie = Movie(
        title="The Matrix",
        description="Sci-fi action film",
        release_date=date(1999, 3, 31),
        duration=136,
    )
    db_session.add(movie)
    await db_session.commit()
    await db_session.refresh(movie)

    response = await client.get(f"/api/v1/movies/{movie.id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["title"] == "The Matrix"
    assert data["id"] == movie.id
    assert data["release_date"] == "1999-03-31"

@pytest.mark.asyncio
async def test_get_movie_not_found(client: AsyncClient):
    response = await client.get("/api/v1/movies/999999")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    assert response.json()["detail"] == "Movie not found"