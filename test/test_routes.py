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
    fake_book_request = BookRequest(**{
        "title": "string_promena",
        "author": "string_promena",
        "price": 20,
        "category_ids": []
    })


    def test_get_book(self):
        response = client.get("/books/22")
        assert response.status_code == 200
        assert response.json() == {
            "id": 22,
            "author": "string",
            "title": "string",
            "price": 0,
            "categories": []
        }

        response = client.get("/books/25")
        assert response.status_code == 200
        assert response.json() == {
            "author": "string",
            "id": 25,
            "title": "string",
            "price": 0,
            "categories": [
                {
                    "name": "strin4g",
                    "id": 4,
                    "description": "strin4g4"
                },
                {
                    "name": "sci-fi",
                    "id": 5,
                    "description": "science fiction"
                }
            ]
        }

        response = client.get("/books/1")
        assert response.status_code == 405
        assert response.json() == {
            "detail": "Book with id 1 doesn't exist"
        }

        response = client.get("/books/banana")
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": [
                        "path",
                        "id"
                    ],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer"
                }
            ]
        }
