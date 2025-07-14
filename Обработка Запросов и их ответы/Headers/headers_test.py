from typing import Annotated
from fastapi import FastAPI, Header,Response


app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}

#повторяющиеся заголовки
#В этом примере x_token — это список строк,
# в котором будут храниться все значения заголовка X-Token, если их несколько.

#Если вы отправите запрос с двумя значениями для заголовка X-Token, например:

# - X-Token: foo
# - X-Token: bar

#Ответ от FastAPI будет таким:

#{
 #   "X-Token values": [
  #      "bar",
   #     "foo"
    #]
#}
@app.get("/itemss/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}


@app.get("/")
def root(user_agent: str = Header()):
    return {"User-Agent": user_agent}

@app.get("/")
def root():
    data = "Hello from here"
    return Response(content=data, media_type="text/plain", headers={"Secret-Code" : "123459"})