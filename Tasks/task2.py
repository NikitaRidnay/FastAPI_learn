from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

"""Models.py"""
class User(BaseModel):
    name: str
    email: str
    age: int
    is_subscribed: bool

"""Your main.py"""
@app.post("/create_user/")
async def post_user(user:User):
    return {"New_username": user.name, "New_email": user.email, "New_age": user.age,"New_is_subscribed": user.is_subscribed}


