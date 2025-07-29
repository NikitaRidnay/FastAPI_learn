import asyncpg
import asyncio

async def get_db_connection():
    try:
        conn = await asyncpg.connect(host="127.0.0.1",database="FastApiTest",user="postgres",password="1111",port="5432"
        )
        return conn
    except:
        print("<UNK> <UNK> <UNK> <UNK>")

