
from database import engine
import model
from fastapi import FastAPI
from route.books import book_route


app = FastAPI()

app.include_router(book_route, tags=["books"])
model.Base.metadata.create_all(bind=engine)
