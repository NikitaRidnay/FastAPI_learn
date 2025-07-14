from fastapi import FastAPI, Path, Query, Form

app = FastAPI()


@app.post("/register/")
async def register_user(
    username: str = Form(...),
    email: str = Form(...),
    age: int = Form(...),
    password: str = Form(...)
):
    return {
        "username": username,
        "email": email,
        "age": age,
        "password_length": len(password)
    }