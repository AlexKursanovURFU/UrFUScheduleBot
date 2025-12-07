import asyncio
from core.bot import TelegramBot
from core.config import config
from core.logger import logger


def main() -> None:
    """Основная функция запуска"""
    try:
        # Создание и запуск бота
        bot = TelegramBot(
            token=config.BOT_TOKEN,
            admin_id=config.ADMIN_ID
        )
        
        logger.info("Запуск бота...")
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Не удалось запустить бота: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()