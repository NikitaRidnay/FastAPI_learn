from fastapi import FastAPI

app = FastAPI()



fake_items_db = [{"product_id": 0 ,"name":"Smartphone","category":"Electronics","price":599.99}, {"product_id": 1,"name":"iphone","category":"Electronics","price":1000}, {"product_id": 2,"name":"Tabletphone","category":"Electronics","price":200}]

#Конечная точка для получения информации о продукте:
@app.get("/product/{product_id}")
async def get_product():
    return fake_items_db

#Конечная точка для поиска товаров:
@app.get("/products/search")
async def search_products(keyword:str,category:str,limit:int=10):
    keyword_lower = keyword.lower() #переводим в нижний регистр ключевые слова
    category_lower = category.lower()#переводим в нижний регистр категории
    #Сортируем
    filtered = [
        item for item in fake_items_db
        if keyword_lower in item["name"].lower() and item["category"].lower() == category_lower
    ]
    return filtered[:limit] #возвращаем с фильтром по лимиту



