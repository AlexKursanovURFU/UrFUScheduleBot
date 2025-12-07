from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Telegram
    BOT_TOKEN: str
    ADMIN_ID: Optional[int] = None
    # Logging
    LOG_LEVEL: str = "INFO"
      
    class Config:
        env_file = ".env"

# Создаем глобальный конфиг
config = Settings()