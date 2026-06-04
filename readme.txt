# Expense Calculator

Приложение для разделения расходов между участниками события.

## Stack
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker (опционально)

## Быстрый старт с Docker

1. Скопируйте настройки: `cp .env.example .env`
2. Запустите: `docker-compose up -d`
3. Примените миграции: `docker exec -it calculator-app-1 alembic upgrade head`
4. Откройте: http://localhost:8000/docs

Остановка: `docker-compose down`

## Локальный запуск (без Docker)

Устанавливаем Python 3.12 и запускаем виртуальное окружение
Создаем виртуальное окружение:
py -3.12 -m venv venv
alembic upgrade head

Запускаем его:
venv\scripts\activate

Проверяем при запуске (python --version), должно быть
Python 3.12.x

Устанавливаем библиотеки:
pip install -r requirements.txt

Инициируем Алембик:
alembic init alembic

Дальше применяем:
alembic revision --autogenerate -m "initial"
alembic upgrade head

По директориям:
crud - тут работа с БД
schemas - тут схемы проверки вводных данных через pydantic
services -  тут уже логика обработки

По основным таблицам - логика:
User
  ↓
Event (owner_id)
  ↓
EventMember (user внутри события)
  ↓
Expense (кто заплатил)
  ↓
ExpenseSplit (как делим)

запустить тест для проверки заполнения
python -m scripts.test_db 

Запускаем Uvicorn:
uvicorn app.main:app --reload

Проверяем:
http://127.0.0.1:8000/docs

SELECT * FROM public.users;
SELECT * FROM public.events;
SELECT * FROM public.expenses;
SELECT * FROM public.event_members;
SELECT * FROM public.expense_splits;

Delete from public.expense_splits;
Delete from public.expenses;
Delete from public.event_members;
Delete from public.events;
Delete from public.users;
Delete from public.users;

