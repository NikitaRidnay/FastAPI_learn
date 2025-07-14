from typing import Annotated
from fastapi import FastAPI, Header,Response
from fastapi import HTTPException

app = FastAPI()

@app.get("/headers")
async def headers(user_agent: Annotated[str | None, Header()] = None):
    Accepted:Annotated[str | None, Header()]
    if not user_agent:
        raise HTTPException(status_code=400)
    return {"User-Agent": user_agent}

