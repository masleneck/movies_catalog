from loguru import logger
from sqlalchemy import Integer, text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'


DATABASE_URL = settings.DATABASE_URL


async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_size=20,        # Размер пула соединений
    max_overflow=10,     # Максимальное количество соединений поверх pool_size
    echo=False           # Логировать SQL 
)
logger.debug(f"Connecting to database: {settings.DATABASE_URL}")


async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Не сбрасывать состояние объектов после commit
    autoflush=False
    )


async def get_async_session():
    """Явное создание сессии без автокоммита"""
    async with async_session_maker() as session: # открывает сессию
        yield session  # передает сессию в обработчик запроса, а после завершения автоматически закрывает ее



async def check_db_connection():
    """Проверка подключения к БД"""
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.success("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False