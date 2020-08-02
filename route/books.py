from typing import Optional

from services import BookService
from database import get_db

import models
from sqlalchemy.orm import Session
from fastapi import Depends, Path, APIRouter

from dto.request_objects import BookRequest

book_router = APIRouter()


@book_router.get("/")
def get_home():
    """displays the homepage"""
    return {"Homepage": "Homepage"}


@book_router.post("/books")
def create_book(book_request: BookRequest, db: Session = Depends(get_db)):
    """creates a new book and stores it in the db"""
    return BookService.create_book(book_request, db)


@book_router.get("/books")
async def get_books(price_filter: Optional[float] = None, author_filter: Optional[str] = None,
                    db: Session = Depends(get_db)):
    query_result = db.query(models.Book)
    if price_filter:
        query_result = query_result.filter(models.Book.price > price_filter)
    if author_filter:
        query_result = query_result.filter(models.Book.author.contains(author_filter))

    return query_result.all()


@book_router.get("/books/{id}")
async def get_book(id: int = Path(Optional[int]), db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == id).first()


@book_router.put("/books/{id}")
async def modify_book(id: int = Path(Optional[int]), modified_book: BookRequest = None, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    book.title = modified_book.title
    book.price = modified_book.price
    book.author = modified_book.author
    db.commit()
    print(book.author)
    return book


@book_router.delete("/books/{id}")
async def delete_book(id: int = Path(Optional[int]), db: Session = Depends(get_db)):
    db.delete(db.query(models.Book).filter(models.Book.id == id).first())
    db.commit()
    return {"Deleted": True}
