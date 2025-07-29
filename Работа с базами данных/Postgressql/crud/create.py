from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from databases import Database
from pydantic import BaseModel

# URL для PostgreSQL (ЗАМЕНИТЕ user, password, localhost, dbname на свои реальные данные!)
DATABASE_URL = "postgresql://postgres:1111@127.0.0.1:5432/FastApiTest"


# Главный объект для работы с базой данных - используется во всех запросах
database = Database(DATABASE_URL)


# Базовый класс для моделей пользователя - содержит общие поля
class UserBase(BaseModel):
    username: str
    email: str


# Модель для получения данных от клиента (валидация ввода)
# Наследует все поля от UserBase и может быть расширена дополнительными полями
# Пример: на входе мы можем запросить пароль, который не будем возвращать в ответе
class UserCreate(UserBase):
    """
    Входная модель для создания пользователя.
    В реальных проектах обычно содержит больше полей, чем выходная модель,
    например, пароль, подтверждение пароля или другие чувствительные данные.
    """
    pass  # В текущей реализации поля совпадают с базовой моделью


# Модель для возврата данных клиенту (сериализация вывода)
# Наследует общие поля и добавляет технические данные из БД
# Важно: выходная модель часто содержит меньше полей, чем входная
class UserReturn(UserBase):
    """
    Выходная модель пользователя. Демонстрирует:
    - Добавление служебных полей (id из БД)
    - Исключение чувствительных данных (если бы они были)
    - Формат данных, безопасный для возврата клиенту
    """
    id: int  # ID всегда присутствует после сохранения в БД


# Пример расширения моделей для учебных целей:
# class UserCreateWithPassword(UserCreate):
#     password: str
#     password_confirm: str

# class UserPrivateInfo(UserReturn):
#     created_at: datetime
#     last_login: datetime

# Управление подключением через lifespan (новый способ в FastAPI 0.95+)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер для управления подключением к БД.
    Заменяет устаревшие @app.on_event("startup") и @app.on_event("shutdown")
    """
    # Устанавливаем соединение при старте приложения
    await database.connect()
    yield  # Здесь работает приложение
    # Корректно закрываем подключение при завершении
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


# Роут для создания пользователей с примерами валидации
@app.post("/users/", response_model=UserReturn)
async def create_user(user: UserCreate):
    """
    Создание пользователя с валидацией данных.

    Параметры:
    - user: данные согласно модели UserCreate

    Возвращает:
    - UserReturn с данными созданного пользователя и ID из БД

    Демонстрирует:
    - Разделение входных и выходных моделей
    - Автоматическую документацию в Swagger/OpenAPI
    - Обработку ошибок базы данных

    Пример использования транзакции:
    async with database.transaction():
        # несколько запросов в одной транзакции
        await database.execute(...)

    Дополнительно сам объект Database имеет свой асинхронный контекстный менеджер, то есть можно писать:
    async with Database(DATABASE_URL) as db:
    	await db.execute(...)

    Примеры выше полезны, если мы устанавливаем соединение не один раз при старте приложения,
    а подключаемся к БД на каждый запрос (используем ресурсы по мере надобности, но чуть увеличиваем накладные расходы на создание соединения)
    """
    # SQL-запрос с параметризацией (защита от SQL-инъекций)
    query = """
            INSERT INTO users (username, email)
            VALUES (:username, :email) RETURNING id /* Получаем автоматически сгенерированный ID */ \
            """

    try:
        # Пример использования транзакции (раскомментировать при необходимости):
        # async with database.transaction():
        user_id = await database.execute(
            query=query,
            values=user.model_dump()  # Автоматическая конвертация в словарь
        )

        # Комбинируем базовые поля с полученным ID
        return UserReturn(
            id=user_id,
            **user.model_dump(mode='json')  # Сериализация для ответа
        )

    except Exception as e:
        # В реальном проекте добавить логирование ошибки
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при создании пользователя: {str(e)}"
        )