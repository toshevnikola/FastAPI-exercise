from app.database import MySqlConnection, SQLiteConnection
from app import model
from fastapi import FastAPI
from app.route.books import book_route
from app.route.categories import category_route

app = FastAPI()

app.include_router(book_route, tags=["books"], prefix='/books')
app.include_router(category_route, tags=["categories"], prefix='/categories')
model.MySqlConnection.Base.metadata.create_all(bind=MySqlConnection.engine)


@app.get("/")
def get_main():
    return {"msg": "Hello World"}
