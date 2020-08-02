from typing import Optional
import model
from sqlalchemy.orm import Session

from dto.request_objects import BookRequest, CategoryRequest


class BookService:

    def create_book(self, book_request: BookRequest, db: Session):
        """creates a new book and stores it in the db"""
        categories = db.query(model.Category).filter(model.Category.id.in_(book_request.category_ids)).all()
        print(categories)
        book = model.Book(title=book_request.title, author=book_request.author, price=book_request.price,
                          categories=categories)
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


class CategoryService:
    def get_categories(self, db: Session):
        return db.query(model.Category).all()

    def create_category(self, db: Session, category_request: CategoryRequest):
        category = model.Category(name=category_request.name, description=category_request.description)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
