import uvicorn
from app.database import engine
from app import model
from fastapi import FastAPI
from app.route.books import book_route
from app.route.categories import category_route
from app.route.users import user_route

app = FastAPI()

app.include_router(book_route, tags=["books"], prefix='/books')
app.include_router(category_route, tags=["categories"], prefix='/categories')
app.include_router(user_route, tags=["users"], prefix='/users')
model.Base.metadata.create_all(bind=engine)


@app.get("/")
def get_main():
    return {"msg": "Hello World"}
