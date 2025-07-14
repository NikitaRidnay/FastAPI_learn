from fastapi import  FastAPI
from uuid import UUID
from datetime import datetime, date, time
from decimal import Decimal
from typing import Annotated
from fastapi import Query

app = FastAPI()

""" UUID (Universally Unique Identifier)"""

#Тип UUID используется для создания уникальных идентификаторов,
# которые часто применяются для идентификации объектов в распределенных системах.
@app.get("/items/{item_id}")
async def get_item(item_id: UUID):
    return {"item_id": item_id}

"""datetime"""

# Используется для даты и времени
@app.get("/datetime/")
async def get_datetime(dt: datetime, day: date, t: time):
    return {"datetime": dt, "date": day, "time": t}

"""frozenset"""
# Тип frozenset представляет собой неизменяемое множество.
# Этот тип полезен, когда вам нужно работать с коллекциями, которые не должны изменяться.
@app.get("/unique-items/")
async def get_unique_items(items: frozenset):
    return {"unique_items": items}

"""Decimal"""
#Decimal используется для работы с числами с фиксированной точностью,
#что важно в задачах, где требуется высокая точность (например, в финансовых расчетах).
@app.get("/price/")
async def get_price(price: Decimal):
    return {"price": price}

"""Bytes"""
#Тип bytes используется для работы с бинарными данными, например, с изображениями или файлами.
@app.post("/upload/")
async def upload_file(file: bytes):
    return {"file_size": len(file)}

"""Anotated"""
#Для более сложных случаев можно использовать Annotated из модуля typing
# (или из typing_extensions для Python версий ниже 3.9).
# Это позволяет добавлять дополнительные метаданные к типам данных,
# например, ограничения или параметры для валидаторов.

#В этом примере с помощью Annotated мы добавляем ограничения на длину строки параметра query.
@app.get("/items/")
async def get_items(
    query: Annotated[str, Query(min_length=3, max_length=50)]
):
    return {"query": query}


