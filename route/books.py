from typing import Optional
from service import BookService
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Path, APIRouter

from dto.request_objects import BookRequest

book_route = APIRouter()


@book_route.get("/")
def get_home():
    """display the homepage"""
    return {"Homepage": "Homepage"}


@book_route.post("")
def create_book(book_request: BookRequest, db: Session = Depends(get_db), bs: BookService = Depends(BookService)):
    """create a new book and store it in the db"""
    return bs.create_book(book_request, db)


@book_route.get("")
def get_books(price_filter: Optional[float] = None, author_filter: Optional[str] = None,
              db: Session = Depends(get_db), bs: BookService = Depends(BookService)):
    """get all books"""
    return bs.get_books(db=db, price_filter=price_filter, author_filter=author_filter)


@book_route.get("/{id}")
async def get_book(id: int = Path(Optional[int]), db: Session = Depends(get_db),
                   bs: BookService = Depends(BookService)):
    """get book with specified id"""
    return bs.get_book(db, id)


@book_route.put("/{id}")
async def modify_book(id: int = Path(Optional[int]), modified_book: BookRequest = None, db: Session = Depends(get_db),
                      bs: BookService = Depends(BookService)):
    """modify book with specified id with book_request object values"""
    book = bs.validate_book_id(id, db)
    if book: return bs.modify_book(db, modified_book, book)


@book_route.delete("/{id}")
async def delete_book(id: int = Path(Optional[int]), db: Session = Depends(get_db),
                      bs: BookService = Depends(BookService)):
    """delete book with specified id"""
    return bs.delete_book(id=id, db=db)
