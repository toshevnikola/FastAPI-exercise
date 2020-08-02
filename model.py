from sqlalchemy import Column, Integer, String, Numeric

from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), index=True)
    author = Column(String(128))
    price = Column(Numeric(10, 2))

    class Config:
        orm_mode = True
