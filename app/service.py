from typing import Optional

from fastapi import HTTPException
from app import model
from sqlalchemy.orm import Session

from app.dto.request_objects import BookRequest, CategoryRequest


class BookService:
    def __init__(self):
        pass

    def create_book(self, book_request: BookRequest, db: Session):
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

        return self.validate_book_id(id, db)

    def modify_book(self, db: Session, modified_book: BookRequest, book: model.Book):
        book.title = modified_book.title
        book.price = modified_book.price
        book.author = modified_book.author
        book.categories = db.query(model.Category).filter(model.Category.id.in_(modified_book.category_ids)).all()
        db.commit()
        db.refresh(book)
        print(book.categories)
        return book

    def add_category(self, book: model.Book, category_ids: list, db: Session):
        categories = db.query(model.Category).filter(model.Category.id.in_(category_ids)).all()
        book.categories.extend(categories)
        db.commit()
        db.refresh(book)
        book.categories = book.categories
        print(book.categories)
        print(categories)
        return book

    def delete_book(self, id: int, db: Session):
        book = self.get_book(db, id)
        if book:
            db.delete(book)
            db.commit()
            return {"Deleted": True}
        return {"Deleted": False}

    def validate_book_id(self, id: int, db: Session):
        book = db.query(model.Book).filter(model.Book.id == id).first()
        if book:
            book.categories = book.categories
            return book
        else:
            raise HTTPException(status_code=405, detail="Book with id {:d} doesn't exist".format(id))


class CategoryService:
    def get_categories(self, db: Session, name_filter: Optional[str] = None, description_filter: Optional[str] = None):
        query_result = db.query(model.Category)
        if name_filter:
            query_result = query_result.filter(model.Category.name.contains(name_filter))
        if description_filter:
            query_result = query_result.filter(model.Category.description.contains(description_filter))

        return query_result.all()

    def create_category(self, db: Session, category_request: CategoryRequest):
        category = model.Category(name=category_request.name, description=category_request.description)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def get_category(self, id: int, db: Session):
        return db.query(model.Category).filter(model.Category.id == id).first()

    def delete_category(self, id: int, db: Session):
        category = db.query(model.Category).filter(model.Category.id == id).first()
        if category:
            db.delete(category)
            db.commit()
            return {"Deleted": True}
        return {"Deleted": False}

    def modify_category(self, category: model.Category, modified_category: CategoryRequest, db: Session):
        category.name = modified_category.name
        category.description = modified_category.description
        db.commit()
        db.refresh(category)
        return category

    def validate_category_id(self, id: int, db: Session):
        category = db.query(model.Category).filter(model.Category.id == id).first()
        if category:
            return category
        else:
            raise HTTPException(status_code=405, detail="Category with id {:d} doesn't exist".format(id))
