from fastapi import FastAPI, Cookie, Response, HTTPException
from pydantic import BaseModel
import uuid  # Для генерации уникальных токенов

app = FastAPI()

#база данных пользователей
users = [
    {"user_id": 1, "username": "user1", "password": "password1"},
    {"user_id": 2, "username": "user2", "password": "password2"}
]

# Хранилище активных сессий
sessions = {}


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login_user(credentials: LoginRequest, response: Response):
    # Проверяем учетные данные
    user = next((u for u in users
                 if u["username"] == credentials.username
                 and u["password"] == credentials.password), None)

    if not user:
        # Возвращаем ошибку, если учетные данные неверны
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Генерируем уникальный токен сессии
    session_token = str(uuid.uuid4())

    # Сохраняем сессию (храним только user_id для безопасности)
    sessions[session_token] = user["user_id"]

    # Устанавливаем защищенную HTTP-only куку
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,  # Только для HTTPS в production
        samesite="Lax"  # Защита от CSRF атак
    )

    return {"message": "Login successful"}


@app.get('/user')
async def user_info(session_token: str = Cookie(None)):
    # Проверяем наличие куки
    if not session_token:
        raise HTTPException(
            status_code=401,
            detail="Session token missing"
        )

    # Ищем user_id по токену
    user_id = sessions.get(session_token)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid session token"
        )

    # Находим пользователя в базе
    user = next((u for u in users if u["user_id"] == user_id), None)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    # Возвращаем информацию о пользователе (без пароля)
    return {
        "user_id": user["user_id"],
        "username": user["username"]
    }


# Эндпоинт для выхода из системы
@app.post("/logout")
async def logout(response: Response, session_token: str = Cookie(None)):
    if session_token and session_token in sessions:
        # Удаляем сессию
        del sessions[session_token]

    # Очищаем куку
    response.delete_cookie("session_token")
    return {"message": "Logout successful"}