from pydantic import BaseModel

from database import engine, SessionLocal, Base
import model


class BookRequest(BaseModel):
    title: str
    author: str
    price: int

