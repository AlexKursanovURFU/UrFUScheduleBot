import logging
from decouple import config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters



# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение настроек из .env
TOKEN = config('TELEGRAM_BOT_TOKEN')
ADMIN_ID = config('ADMIN_ID', default=None, cast=int)

# Константы
BASE_URL = "https://urfu.ru"
SCHEDULE_URL = f"{BASE_URL}/ru/students/study/schedule/#/groups"

class URFUScheduleBot:

    def __init__(self, token: str, admin_id: int):
        self.token = token
        self.admin_id = admin_id
        self.application = Application.builder().token(token).build()

        # Регистрация обработчиков команд

        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("admin", self.admin_command))
        self.application.add_handler(CallbackQueryHandler(self.button_handler))
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handle_message
        ))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        welcome_text = (
            f"Привет, {user.first_name}! 👋\n\n"
            "Я бот для получения расписания занятий УрФУ.\n"
            "Используйте команды:\n"
            "/schedule - Найти расписание группы\n"
            "/help - Получить справку\n\n"
            "Выберите действие ниже:"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔍 Найти расписание", callback_data="find_schedule")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def help_command(self, update, context):
        """Обработчик команды /help"""
        help_text = (
            "📚 *Помощь по использованию бота*\n\n"
            "Доступные команды:\n"
            "/start - Начать работу с ботом\n"
            "/schedule - Поиск расписания по номеру группы\n"
            "/help - Эта справка\n\n"
            "*Как использовать:*\n"
            "1. Используйте /schedule или кнопку ниже\n"
            "2. Введите номер группы (например: МЕН-330603)\n"
            "3. Получите расписание на текущую неделю\n\n"
            "*Примечание:*\n"
            "Бот получает данные с официального сайта УрФУ:\n"
            "https://urfu.ru/ru/students/study/schedule/#/groups"
        )
        
        keyboard = [[InlineKeyboardButton("🔍 Найти расписание", callback_data="find_schedule")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(help_text, parse_mode='Markdown', reply_markup=reply_markup)

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на inline-кнопки"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "find_schedule":
            await query.edit_message_text(
                "Введите номер группы (например: МЕН-330603):\n"
                "Или нажмите кнопку для примера:",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Пример: МЕН-330603", callback_data="example_group")
                ]])
            )
            context.user_data['waiting_for_group'] = True
            
        elif query.data == "example_group":
            await self.process_group_name(update, context, "МЕН-330603")
            
        elif query.data == "help":
            help_text = (
                "📋 *Как найти группу:*\n"
                "1. Полное название группы обычно выглядит так:\n"
                "   • МЕН-333001\n"
                "   • МЕН-333009\n"
                "   • МЕН-330603\n"
                "2. Название можно найти на сайте УрФУ\n"
                "3. При проблемах - попробуйте разные форматы\n\n"
                "Попробуйте ввести номер группы:"
            )
            await query.edit_message_text(help_text, parse_mode='Markdown')
            context.user_data['waiting_for_group'] = True
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        if context.user_data.get('waiting_for_group'):
            group_name = update.message.text.strip()
            await self.process_group_name(update, context, group_name)
        else:
            await update.message.reply_text(
                "Используйте /schedule для поиска расписания или /help для справки."
            )

    async def process_group_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE, group_name: str):
        """Обработка введенного названия группы"""
        await self.send_message(
                    update, 
                    f"❌ *Неверный формат группы:* {group_name}\n"
                    "Пример правильного формата: *МЕН-333001*\n\n"
                    "Попробуйте еще раз:",
                    parse_mode='Markdown'
                )
        return 0

    async def send_message(self, update: Update, text: str, **kwargs):
        """Универсальная отправка сообщения"""
        if update.callback_query:
            await update.callback_query.edit_message_text(text, **kwargs)
        else:
            await update.message.reply_text(text, **kwargs)

    async def admin_command(self, update, context):
        """Обработчик команды /admin"""
        user_id = update.effective_user.id
        if user_id == self.admin_id:
            await update.message.reply_text(f"Привет, администратор! Ваш ID: {user_id}")
        else:
            await update.message.reply_text("У вас нет прав администратора.")
    
    def run(self):
        """Запуск бота"""
        logger.info("Бот запущен...")
        self.application.run_polling(allowed_updates=[])

if __name__ == '__main__':
    bot = URFUScheduleBot(TOKEN, ADMIN_ID)
    bot.run()