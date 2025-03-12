# 📌 Django Project: MySite

## 📖 Описание проекта
Этот проект представляет собой Django-приложение с REST API, поддержкой кэширования, авторизацией пользователей и панелью администратора. В проекте используется `Django 5.0.3`, `Django REST Framework`, `Gunicorn`, `Sentry SDK` и другие инструменты.

## 🚀 Развертывание проекта
### 1️⃣ Клонирование репозитория
```bash
# Замените URL на актуальный репозиторий
git clone https://github.com/your-repo/mysite.git
cd mysite
```

### 2️⃣ Установка зависимостей
#### 📦 С помощью Poetry:
```bash
poetry install
```
#### 🐍 С помощью pip:
```bash
pip install -r requirements.txt
```

### 3️⃣ Конфигурация переменных окружения
Создайте файл `.env` на основе `.env.template` и укажите необходимые значения:
```ini
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,0.0.0.0
```

### 4️⃣ Запуск проекта
#### 📌 Локальный запуск
```bash
python manage.py migrate
python manage.py createsuperuser  # Создание администратора
python manage.py runserver
```

#### 🐳 Запуск через Docker
```bash
docker-compose up --build
```

## 🛠 Проверка работоспособности
Открыть в браузере:
- 🔹 API Swagger: [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
- 🔹 Django Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 🧪 Запуск тестов
```bash
python manage.py test
```

## 📡 API-запросы с помощью `curl`
### 📌 Получение списка пользователей
```bash
curl -X GET http://127.0.0.1:8000/api/users/ -H "Authorization: Token your_api_key"
```
### 📌 Создание нового пользователя
```bash
curl -X POST http://127.0.0.1:8000/api/users/ -H "Content-Type: application/json" -d '{"username": "newuser", "password": "password123"}'
```

## 📝 Заключение
Проект готов к развертыванию и использованию! 🎉 Если у вас есть вопросы, создайте issue или свяжитесь с автором проекта.

