# **Описание проекта**

LightTech - это Django REST API для управления пользовательскими аккаунтами и финансовыми операциями. Основные функции:

- Регистрация, авторизация и управление сессиями пользователей
- Пополнение и снятие средств с баланса
- Переводы между пользователями
- История операций с балансом
---
# **Запуск проекта с помощью Docker**

1. Склонируйте репозиторий:
```bash
git clone https://github.com/yourusername/lighttech.git
cd lighttech
```
2. Создайте файл `.env` на основе `.env.example`:
```bash
SECRET_KEY='your_secret_key_here'
DEBUG=True

DB_NAME='your_db_name_here'
DB_USER='your_db_user_here'
DB_PASSWORD='your_db_password_here'
DB_HOST='db' #если запускатесь через docker comose 
DB_PORT='your_db_port_here'

ALLOWED_HOSTS='localhost,127.0.0.1'

ROTATE_REFRESH_TOKENS=True
BLACKLIST_AFTER_ROTATION=True
ACCESS_TOKEN_LIFETIME_MINUTES=10
REFRESH_TOKEN_LIFETIME_MINUTES=1440

REDIS_URL='redis://redis:6379/1' #если запускатесь через docker comose 
```
3. Запустите проект:
```
docker compose up --build
```
4. После запуска приложение будет доступно по адресу:
    - API: `http://localhost:8000`
    - Документация Swagger: `http://localhost:8000/api/docs/`
    - Админка: `http://localhost:8000/admin/`
5. Для создания суперпользователя (в отдельном терминале):
```
docker compose run web python manage.py createsuperuser
```

---
# **Основные эндпоинты API**

**Аутентификация:**
- `POST /api/auth/v1/register/` - регистрация пользователя
- `POST /api/auth/v1/login/` - авторизация
- `POST /api/auth/v1/logout/` - выход из системы
- `POST /api/auth/v1/token/refresh/` - обновление JWT токена

**Операции с балансом:**
- `POST /api/balance/v1/deposit/` - пополнение баланса
- `POST /api/balance/v1/withdraw/` - снятие средств
- `POST /api/balance/v1/transfer/` - перевод другому пользователю
- `GET /api/balance/v1/operations/` - история операций

---
# **Запуск тестов**

#### Запуск всех тестов
```bash
docker-compose run web pytest
```

**Покрытие тестами:**
- Модульные тесты сервисов
    - Регистрация пользователя и создание баланса
    - Операции с балансом (пополнение/снятие/перевод)
    - Обработка ошибок бизнес-логики
- Интеграционные тесты API:
  - Аутентификация (регистрация, вход, выход)
  - Полный цикл операций с балансом
  - История операций с кешированием
  - Авторизация и права доступа
- Обработка edge cases:
  - Недостаток средств при снятии/переводе
  - Перевод самому себе
  - Невалидные суммы операций
  - Просмотр истории без авторизации
  - Обработка несуществующих ресурсов
  - Конкурентные запросы (блокировки БД)
- Дополнительно:
    - Тестирование транзакционности операций
    - Проверка кеширования истории операций
    - Валидация всех входных параметров
---
# **Документация API**

Проект использует `drf-spectacular` для автоматической генерации документации:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
---
# **Структура проекта**
```bash
lighTech/
├── authapp/          # Приложение аутентификации
│   ├── services.py   # Бизнес-логика регистрации
│   ├── views/        # API представления
│   └── ...
├── balance/          # Приложение операций с балансом
│   ├── models.py     # Модели БД
│   ├── services.py   # Бизнес-логика операций
│   ├── views/        # API представления
│   └── ...
├── lighTech/         # Основная конфигурация проекта
│   ├── settings.py   # Настройки Django
│   └── urls.py       # Главные URL-маршруты
├── docker-compose.yml # Конфигурация Docker
├── Dockerfile        # Образ Docker для приложения
├── .env.example      # Шаблон переменных окружения
└── requirements.txt  # Зависимости Python
```
# **Технологический стек**

- **Backend**: Django 5.2, Django REST Framework
- **База данных**: PostgreSQL
- **Аутентификация**: JWT (djangorestframework-simplejwt)
- **Документация**: drf-spectacular
- **Контейнеризация**: Docker
- **Тестирование**: Pytest
- **Логирование**: logging