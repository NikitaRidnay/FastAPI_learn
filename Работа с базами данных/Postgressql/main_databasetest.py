from fastapi import FastAPI, Depends
from pydantic import BaseModel
from databaseconnect import get_db_connection
import asyncpg

app = FastAPI()

class Item(BaseModel):
    name: str

@app.post("/items")
async def create_item(item: Item, db: asyncpg.Connection = Depends(get_db_connection)):
    await db.execute('''
        INSERT INTO items(name) VALUES($1)
    ''', item.name)
    return {"message": "Item added successfully!"}