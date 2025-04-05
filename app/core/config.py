from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger
class Settings(BaseSettings):
    DATABASE_URL: str = "DATABASE_URL"
    TEST_DATABASE_URL: str = "TEST_DATABASE_URL"
    model_config = SettingsConfigDict(
        case_sensitive=False, 
        env_file=".env",
        env_file_encoding="utf-8",
        )


settings= Settings()
if __name__ == '__main__':
    logger.info(f"DATABASE_URL: {settings.DATABASE_URL}")
    logger.info(f"TEST_DATABASE_URL: {settings.TEST_DATABASE_URL}")