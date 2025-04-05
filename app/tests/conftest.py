'''
Фикстуры — это подготовка данных или окружения перед тестом (например, создание клиента для запросов или сессии базы данных).
pytest app/tests/ -v -s --cache-clear
'''
from loguru import logger
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.main import app
from app.core.config import settings
from app.core.database import Base, get_async_session, async_session_maker

# Настройка тестовой БД
TEST_DATABASE_URL= settings.TEST_DATABASE_URL

test_async_engine = create_async_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)
logger.debug(f"Connecting to test database: {settings.TEST_DATABASE_URL}")

test_async_session_maker = async_sessionmaker(
    bind=test_async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Не сбрасывать состояние объектов после commit
    autoflush=False
    )

# Переопределяем зависимость get_async_session в приложении
async def override_get_async_session():
    logger.debug(f"Using OVERRIDEN test database session {TEST_DATABASE_URL}")
    async with test_async_session_maker() as session:
        logger.debug("New test session created")
        yield session
        logger.debug("Test session cleanup (before close)")

app.dependency_overrides[get_async_session] = override_get_async_session



@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_database():
    """Создаём и очищаем тестовую БД перед всеми тестами"""
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS citext"))
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Test database prepared")
    yield
    # временное отключение очистки
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_async_engine.dispose() # закрываем движок
    logger.info("Test database cleaned up")


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Создаём новую сессию для каждого теста"""
    async with test_async_session_maker() as session:
        yield session
        await session.rollback() # Откатываем изменения после теста
        # await session.commit() # Сохраняем данные вместо отката
        # logger.debug("Test session committed")
    # Закрытие сессии происходит автоматически благодаря async with


@pytest_asyncio.fixture(scope="function")
async def client():
    """Асинхронный клиент для тестирования"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
          base_url="http://test",
          ) as client:
        yield client