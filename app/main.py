from app.database import engine, SessionLocal
from app import model
from fastapi import FastAPI
from app.route.books import book_route
from app.route.categories import category_route

app = FastAPI()

app.include_router(book_route, tags=["books"], prefix='/books')
app.include_router(category_route, tags=["categories"], prefix='/categories')
model.Base.metadata.create_all(bind=engine)



@app.get("/")
def get_main():
    return {"msg": "Hello World"}
