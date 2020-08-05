from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.database import Base

association_table = Table('categories_books', Base.metadata,
                          Column('categories_id', Integer, ForeignKey('categories.id')),
                          Column('books_id', Integer, ForeignKey('books.id'))
                          )


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=False, index=True)
    description = Column(String(256))
    books = relationship("Book",
                         secondary=association_table, back_populates="categories")

    class Config:
        orm_mode = True


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), index=True)
    author = Column(String(128))
    price = Column(Numeric(10, 2))
    categories = relationship(
        "Category",
        secondary=association_table,
        back_populates="books")

    class Config:
        orm_mode = True
