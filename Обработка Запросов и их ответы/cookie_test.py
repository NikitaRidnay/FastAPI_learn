from fastapi import Cookie, FastAPI,Response
from typing import Optional
app = FastAPI()

@app.get("/items/")
def read_items(ads_id: Optional[str] = Cookie(default=None)):
    return {"ads_id": ads_id}

@app.get("/")
def root(last_visit = Cookie()):
    return {"last visit": last_visit}

#В этом примере устанавливается cookie с именем user_id и значением 12345. Также указывается срок действия cookie max_age=3600 (1 час) и флаг httponly=True, что делает cookie доступной только для сервера и недоступной через JavaScript, повышая безопасность.
#Метод set_cookie позволяет настраивать следующие параметры:
#key: имя cookie.
#value: значение cookie.
#max_age: срок действия cookie (в секундах).
#expires: дата и время истечения срока действия cookie.
#path: путь, с которым cookie будет доступна.
#domain: домен, с которым cookie будет доступна.
#secure: если True, cookie будет передаваться только по защищенному соединению (https).
#httponly: если True, cookie не будет доступна через JavaScript, что повышает безопасность.
#samesite: позволяет ограничить, как cookie будет передаваться с запросами из других сайтов.
@app.get("/set-cookie")
def set_cookie(response: Response):
    response.set_cookie(key="user_id", value="12345", max_age=3600, httponly=True)
    return {"message": "Cookie has been set!"}



#Вы можете указать время истечения срока действия файла cookie,
# используя параметр expires,
# или установить максимальный возраст с помощью параметра max_age.
# Это помогает контролировать срок службы файлов cookie и эффективно управлять данными сеанса.

#FastAPI предоставляет простой способ удалить файлы cookie,
# установив время их истечения в прошлом.
# Это дает указание клиенту удалить файл cookie из своего хранилища.

#Также у класса Response есть метод delete_cookie,
# который принимает в качестве аргумента строку (наименование cookie) и удаляет её на стороне клиента.
#Пример:

@app.post("/logout", status_code=204)
async def logout_user(response: Response):
    response.delete_cookie("example_access_token")
    return {"message": "Logged out successfully"}