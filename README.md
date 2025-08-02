#### **Описание проекта**

LightTech - это Django REST API для управления пользовательскими аккаунтами и финансовыми операциями. Основные функции:

- Регистрация, авторизация и управление сессиями пользователей
- Пополнение и снятие средств с баланса
- Переводы между пользователями
- История операций с балансом
---
#### **Запуск проекта с помощью Docker**

1. Склонируйте репозиторий:
```bash
git clone https://github.com/yourusername/lighttech.git
cd lighttech
```
2. Создайте файл `.env` на основе `.env.example`:
3. Запустите проект:
```
docker-compose up --build
```
4. После запуска приложение будет доступно по адресу:
    - API: `http://localhost:8000`
    - Документация Swagger: `http://localhost:8000/api/docs/`
    - Админка: `http://localhost:8000/admin/`
5. Для создания суперпользователя (в отдельном терминале):
```
docker-compose run web python manage.py createsuperuser
```

---
#### **Основные эндпоинты API**

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
#### **Запуск тестов**

#### Запуск всех тестов
```bash
docker-compose run web python manage.py test
```

#### Запуск тестов приложения аутентификации
```bash
docker-compose run web python manage.py test authapp
```

#### Запуск тестов приложения баланса
```bash
docker-compose run web python manage.py test balance
```

**Покрытие тестами:**
- Регистрация и аутентификация пользователей
- Успешное пополнение и снятие средств
- Переводы между пользователями
- История операций
- Обработка ошибок:
    - Недостаток средств при снятии
    - Попытка перевода самому себе
    - Отрицательная сумма операций
    - Несуществующий баланс получателя
---
#### **Документация API**

Проект использует `drf-spectacular` для автоматической генерации документации:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
---
#### **Структура проекта**
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
#### **Технологический стек**

- **Backend**: Django 5.2, Django REST Framework
- **База данных**: PostgreSQL
- **Аутентификация**: JWT (djangorestframework-simplejwt)
- **Документация**: drf-spectacular
- **Контейнеризация**: Docker
- **Тестирование**: Django Test Framework