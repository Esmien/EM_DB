from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database (Postgres)
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int


    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """
        Собираем строку подключения автоматически из переменных.
        Используем asyncpg драйвер.
        """
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


    # Конфигурация Pydantic
    model_config = SettingsConfigDict(
        env_file=".env",  # Читаем из .env
        env_file_encoding="utf-8",
        extra="ignore",  # Игнорируем лишние переменные в .env
    )


# Создаем единственный экземпляр настроек
settings = Settings()
