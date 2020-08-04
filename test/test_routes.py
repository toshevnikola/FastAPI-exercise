import unittest
from urllib import response

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import database_exists, create_database

from app import main, model
from app.route import books
from app.route.books import book_route, get_db
from fastapi.testclient import TestClient
import sqlite3
from app.dto.request_objects import BookRequest
from app.service import BookService

SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:admin@localhost/fastapidemo_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

if not database_exists(engine.url):
    create_database(engine.url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

model.Base.metadata.create_all(bind=engine)


# Override db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


main.app.dependency_overrides[get_db] = override_get_db
client = TestClient(main.app)


def test_create_book():
    response = client.post(
        "/books",
        json={"title": "string_promena",
              "author": "string_promena",
              "price": 20,
              "category_ids": [1]}
    )
    assert response.status_code == 200
