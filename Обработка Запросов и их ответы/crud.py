import fastapi
from fastapi import Body, FastAPI, status
from pydantic import BaseModel
from starlette import status


app = FastAPI()

messages_db = {
    "0": "This is the first message",
    "1": "This is the second message",
    "2": "This is the third message",
}

"""Выводим все сообщения из словаря messages_db"""


@app.get("/")
async def get_all_messages() -> dict:
    return messages_db


""" Функция для вывода сообщения из словаря message_db по message_id"""


@app.get("/message/{message_id}")
async def get_message(message_id: str) -> str:
    return messages_db[message_id]


"""Создаем новую запись при post запросе """


@app.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(message: str = Body()) -> str:
    current_index = len(messages_db)
    messages_db[current_index] = message
    return f"Message created!"


"""Изменяем сообщение по message_id"""


@app.put("/message/{message_id}")
async def update_message(message_id: str, message: str = Body()) -> str:
    messages_db[message_id] = message
    return f"Message updated!"


"""Удаляем сообщение по запросу (message_id)"""


@app.delete("/message/{message_id}")
async def delete_message(message_id: str) -> str:
    messages_db.pop(message_id)
    return f"Message ID={message_id} deleted!"


"""Удаляем весь словарь message_db"""


@app.delete("/")
async def kill_message_all() -> str:
    messages_db.clear()
    return f"All messages deleted!"
