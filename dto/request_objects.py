from typing import List

from pydantic import BaseModel

from database import engine, SessionLocal, Base
import model


class CategoryRequest(BaseModel):
    name: str
    description: str


class BookRequest(BaseModel):
    title: str
    author: str
    price: int
    category_ids: List[int]
