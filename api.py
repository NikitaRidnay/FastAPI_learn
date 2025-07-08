from typing import Annotated

from fastapi import FastAPI, Path, Query
from starlette.config import undefined

app = FastAPI()

country_dict = {
    'Russia': ['Moscow', 'St. Petersburg', 'Novosibirsk', 'Ekaterinburg', 'Kazan'],
    'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia'],
}
@app.get("/")
async def welcome() ->dict:
    return {"message": "This is my first fast api project"}


@app.get("/user/{username}")
async def login(
        username: Annotated[str, Path(min_length=3, max_length=15, description='Enter your username', example='permin0ff')],
        first_name: Annotated[str, Query(max_length=10)] = ...) -> dict:
    return {"user": username, "Name": first_name}


@app.get("/user")
async def search(people: Annotated[list[str], Query()]) -> dict:
    return {"user": people}


@app.get("/hello/{first_name}/{last_name}")
async def welcome_user(first_name: str,last_name:str) -> dict:
    return {"user": f'hello {first_name} {last_name}'}

@app.get("/order/{order_id}")
async def order(order_id: int) -> dict:
    return {"id": order_id}
@app.get("/user/profile")
async def profile() -> dict:
    return {"profile": "View profile user"}

@app.get("/user/{user_name}")
async def user(user_name: str) -> dict:
    return {"user": user_name}

@app.get("/user")
async def login(username: str, age: int | None = None) -> dict:
    return {"user": username, "age": age}

@app.get("/product/{product_id}")
async def product(product_id: str) -> dict:
    return {"Stock number : ": product_id}

@app.get("/users/{user_name}")
async def user(user_name: str) -> dict:
    return {"user_name": user_name}
@app.get("/users/admin")
async def admin_users(message:str) -> dict:
    return {"message": "hello admin"}

@app.get("/product")
async def detail_view(id: int) -> dict:
    return {'Product': f"Stock number: {id}"}

@app.get("/users")
async def users(name:str | None = 'undefined',age:int | None = 18) -> dict:
    return {"user_name": name, "user_age": age}

@app.get("/country/{country}")
async def list_cities(country: str, limit: int = 5):

    cities = country_dict[country]

    limited_cities = cities[:limit]

    return {"country": country, "cities": limited_cities}
