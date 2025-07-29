from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from databases import Database
from pydantic import BaseModel

# URL для PostgreSQL (ЗАМЕНИТЕ user, password, localhost, dbname на свои данные!)
DATABASE_URL = "postgresql://postgres:1111@127.0.0.1:5432/FastApiTest"

# Главный объект для работы с базой данных
database = Database(DATABASE_URL)


# Базовый класс для моделей пользователя
class UserBase(BaseModel):
    username: str
    email: str


# Модель для создания пользователя (входные данные)
class UserCreate(UserBase):
    """
    Модель для получения данных от клиента.
    В реальных проектах может содержать дополнительные поля,
    например, пароль, которые не возвращаются в ответе.
    """


# Модель для возврата данных пользователя (выходные данные)
class UserReturn(UserBase):
    """
    Модель для сериализации данных пользователя.
    Включает технические поля из БД (id) и исключает чувствительные данные.
    """
    id: int  # ID всегда присутствует после сохранения в БД


# Управление подключением к БД через lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом подключения к базе данных"""
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


# Эндпоинт для создания пользователей
@app.post("/users/", response_model=UserReturn)
async def create_user(user: UserCreate):
    """
    Создание нового пользователя в базе данных.

    Возвращает:
    - UserReturn с данными созданного пользователя и ID из БД

    Пример тела запроса:
    {
        "username": "john_doe",
        "email": "john@example.com"
    }
    """
    query = """
            INSERT INTO users (username, email)
            VALUES (:username, :email) RETURNING id \
            """
    try:
        user_id = await database.execute(
            query=query,
            values=user.model_dump()
        )
        return UserReturn(
            id=user_id,
            **user.model_dump()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка создания пользователя: {str(e)}"
        )


# Эндпоинт для получения пользователя по ID
@app.get("/users/{user_id}", response_model=UserReturn)
async def get_user(user_id: int):
    """
    Получение информации о пользователе по его ID.

    Параметры:
    - user_id: идентификатор пользователя в БД

    Возвращает:
    - Данные пользователя в формате UserReturn
    - 404 ошибку если пользователь не найден
    """
    query = """
            SELECT id, username, email
            FROM users
            WHERE id = :user_id \
            """
    try:
        result = await database.fetch_one(
            query=query,
            values={"user_id": user_id}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения пользователя: {str(e)}"
        )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Пользователь с указанным ID не найден"
        )

    return UserReturn(
        id=result["id"],
        username=result["username"],
        email=result["email"]
    )


# Роут для полного обновления информации о пользователе по ID
@app.put("/users/{user_id}", response_model=UserReturn)
async def update_user(user_id: int, user: UserCreate):
    """
    Полное обновление данных пользователя по ID (PUT-запрос).

    Параметры:
    - user_id: ID пользователя в базе данных
    - user: новые данные пользователя (все поля обязательны)

    Возвращает:
    - Обновленные данные пользователя в формате UserReturn
    - 404 ошибку если пользователь не найден
    - 500 ошибку при проблемах с базой данных

    Пример запроса:
    {
        "username": "new_username",
        "email": "new_email@example.com"
    }
    """
    # SQL-запрос с возвратом обновленных данных
    query = """
            UPDATE users
            SET username = :username, \
                email    = :email
            WHERE id = :user_id RETURNING id \
            """

    values = {
        "user_id": user_id,
        "username": user.username,
        "email": user.email
    }

    try:
        # Выполняем запрос и получаем обновленные данные
        result = await database.execute(query=query, values=values)

        # Если запись не найдена
        if not result:
            raise HTTPException(
                status_code=404,
                detail="Пользователь с указанным ID не найден"
            )

        # Преобразуем результат запроса в модель UserReturn
        return UserReturn(**user.model_dump(), id=result, )

    except HTTPException as he:
        # Пробрасываем HTTPException из проверки выше
        raise he

    except Exception as e:
        # Обрабатываем другие ошибки базы данных
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка обновления пользователя: {str(e)}"
        )