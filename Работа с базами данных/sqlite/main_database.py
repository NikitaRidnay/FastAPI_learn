from fastapi import FastAPI, Depends
from pydantic import BaseModel
import sqlite3
from database import get_db_connection

app = FastAPI()


class Item(BaseModel):
    name: str


@app.post("/items")
def create_item(item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO items (name) VALUES (?)", (item.name,))
    conn.commit()
    conn.close()

    return {"message": "Item added successfully!"}