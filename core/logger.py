import logging
import sys
from logging.handlers import RotatingFileHandler

from core.config import config


def setup_logger(name: str = "bot") -> logging.Logger:
    """Настройка и создание логгера"""
    
    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Если уже есть обработчики, не добавляем новые
    if logger.handlers:
        return logger
    
    # Форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Файловый обработчик (с ротацией)
    file_handler = RotatingFileHandler(
        filename='bot.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Добавляем обработчики
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Отключаем пропагацию в корневой логгер
    logger.propagate = False
    
    return logger


# Создаем глобальный логгер
logger = setup_logger()