from database import engine
import model
from fastapi import FastAPI
from route.books import book_route
from route.categories import category_route

app = FastAPI()

app.include_router(book_route, tags=["books"], prefix='/books')
app.include_router(category_route, tags=["categories"], prefix='/categories')
model.Base.metadata.create_all(bind=engine)
