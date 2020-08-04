import unittest
from urllib import response

from fastapi import Depends
from sqlalchemy.orm import Session

from app import main, model
from fastapi.testclient import TestClient
import sqlite3
from app.database import SQLiteConnection, MySqlConnection
from app.dto.request_objects import BookRequest
from app.service import BookService

client = TestClient(main.app)


class TestDefaultRoutes():

    def test_read_main(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}


class TestBookRoutes():
    book_service = BookService()
    db = MySqlConnection.SessionLocal()

    fake_book_request = BookRequest(**{
        "title": "string_promena",
        "author": "string_promena",
        "price": 20,
        "category_ids": []
    })

    def test_create_book(self):
        response = self.book_service.create_book(book_request=self.fake_book_request, db=self.db)
        assert response == "Created"

