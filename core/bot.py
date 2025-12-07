from typing import Optional
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from core.logger import logger

class TelegramBot:
    def __init__(self, token: str, admin_id: Optional[int] = None):
        """Инициализация бота"""
        self.token = token
        self.admin_id = admin_id
        self.application = Application.builder().token(token).build()
        
        # Регистрация обработчиков
        self._register_handlers()
    
    def _register_handlers(self) -> None:
        """Регистрация всех обработчиков команд и сообщений"""
        # Команды
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # Обработка обычных сообщений
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo_message))
        
        # Обработка ошибок
        self.application.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: CallbackContext) -> None:
        """Обработчик команды /start"""
        user = update.effective_user
        await update.message.reply_text(
            f"Привет, {user.first_name}! 👋\n"
            f"Я минимальный телеграм-бот.\n"
            f"Используй /help для просмотра доступных команд."
        )
        logger.info(f"User {user.id} ({user.username}) started the bot")
    
    async def help_command(self, update: Update, context: CallbackContext) -> None:
        """Обработчик команды /help"""
        help_text = """
        📋 Доступные команды:
        
        /start - Начать работу с ботом
        /help - Показать это сообщение
        
        Просто отправьте любое сообщение, и я его повторю!
        """
        await update.message.reply_text(help_text)
    
    async def echo_message(self, update: Update, context: CallbackContext) -> None:
        """Эхо-ответ на текстовые сообщения"""
        user_message = update.message.text
        user = update.effective_user
        
        await update.message.reply_text(
            f"Вы написали: {user_message}\n"
            f"ID вашего сообщения: {update.message.message_id}"
        )
        logger.info(f"User {user.id} sent message: {user_message}")
    
    async def error_handler(self, update: Update, context: CallbackContext) -> None:
        """Обработчик ошибок"""
        logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "Произошла ошибка при обработке вашего запроса. 😔"
            )
    
    def run(self) -> None:
        """Запуск бота"""
        logger.info("Бот запущен и готов к работе...")
        
        # Запуск polling
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)