# 1. Install Requirements:

> Create an virtualenv and source it
```bash
python3 -m venv .venv && source .venv/bin/activate
```
> Now install requirements but make sure you're in (.venv)
```bash
pip3 install -U -r requirements.txt
```

urfu_schedule_bot/
├── core/                      # Ядро системы
│   ├── __init__.py
│   ├── bot.py                # Главный бот (оркестратор)
│   ├── config.py             # Конфигурация
│   ├── database.py           # Подключение к БД
│   └── dependencies.py       # Зависимости между модулями
│
├── modules/                  # Независимые модули
│   ├── __init__.py           # Регистрация модулей
│   │
│   ├── users/                # Модуль пользователей
│   │   ├── __init__.py
│   │   ├── models.py        # SQLAlchemy модели
│   │   ├── repository.py    # Работа с БД
│   │   ├── service.py       # Бизнес-логика
│   │   └── handlers.py      # Команды и обработчики
│   │
│   ├── schedule/            # Модуль расписания
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── parser.py       # Парсинг сайта УрФУ
│   │   ├── cache.py        # Кэширование (Redis)
│   │   ├── service.py
│   │   └── handlers.py
│   │
│   ├── notifications/       # Модуль уведомлений
│   │   ├── __init__.py
│   │   ├── service.py
│   │   ├── scheduler.py    # Планировщик уведомлений
│   │   └── handlers.py
│   │
│   └── admin/              # Админ-панель
│       ├── __init__.py
│       ├── service.py
│       └── handlers.py
│
├── shared/                  # Общие компоненты
│   ├── __init__.py
│   ├── keyboards.py        # Общие клавиатуры
│   ├── validators.py       # Валидация данных
│   ├── utils.py           # Утилиты
│   └── decorators.py      # Декораторы (кэш, логирование)
│
├── migrations/             # Миграции БД (Alembic)
│   └── alembic/
│
├── scripts/               # Вспомогательные скрипты
│   ├── init_db.py        # Инициализация БД
│   └── backup.py         # Бэкап данных
│
├── tests/                # Тесты по модулям
│   ├── users/
│   ├── schedule/
│   └── conftest.py
│
├── requirements.txt      # Зависимости
├── docker-compose.yml    # Docker для разработки
├── .env.example         # Пример переменных окружения
├── main.py             # Точка входа
└── README.md


Telegram API
     ↓
┌─────────────────┐
│  Core Bot       │ ← Регистрирует обработчики из модулей
└─────────────────┘
         │
         ↓ (вызывает обработчики модулей)
┌─────────────────┐
│   Users Module  │ ← Работает с профилями
│                 │ ← Управляет настройками
└─────────────────┘
         │ (запрашивает данные)
         ↓
┌─────────────────┐
│ Schedule Module │ ← Парсит сайт УрФУ
│                 │ ← Кэширует данные
└─────────────────┘
         │ (уведомляет)
         ↓
┌─────────────────┐
│ Notifications   │ ← Отправляет уведомления
│ Module          │ ← Планирует напоминания
└─────────────────┘
         │ (мониторит)
         ↓
┌─────────────────┐
│   Admin Module  │ ← Статистика и управление
└─────────────────┘

