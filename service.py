from typing import Optional
import model
from sqlalchemy.orm import Session
from dto.request_objects import BookRequest


class BookService:

    def create_book(self, book_request: BookRequest, db: Session):
        """creates a new book and stores it in the db"""
        book = model.Book(title=book_request.title, author=book_request.author, price=book_request.price)
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

    def get_books(self, db: Session, price_filter: Optional[float] = None, author_filter: Optional[str] = None):
        query_result = db.query(model.Book)
        if price_filter:
            query_result = query_result.filter(model.Book.price > price_filter)
        if author_filter:
            query_result = query_result.filter(model.Book.author.contains(author_filter))

        return query_result.all()

    def get_book(self, db: Session, id: int):
        return db.query(model.Book).filter(model.Book.id == id).first()

    def modify_book(self, db: Session, modified_book: BookRequest, id: int):
        book = db.query(model.Book).filter(model.Book.id == id).first()
        book.title = modified_book.title
        book.price = modified_book.price
        book.author = modified_book.author
        db.commit()
        db.refresh(book)
        return book

    def delete_book(self, id: int, db: Session):
        book = self.get_book(db, id)
        if book:
            db.delete(book)
            db.commit()
            return {"Deleted": True}
        return {"Deleted": False}
