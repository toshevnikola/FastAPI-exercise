from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from starlette import status

from app import main, model
from app.route.books import book_route
from app.database import get_db
from fastapi.testclient import TestClient
from app.service import CategoryService
from random import randint
from test.config import set_test_db_client

client = set_test_db_client()


def test_create_book():
    response = client.post(
        "/books",
        json={"title": "string_promena",
              "author": "string_promena",
              "price": 20,
              "category_ids": [1]}
    )
    data = response.json()
    assert response.status_code == 200
    assert data['title'] == 'string_promena'
    assert data['author'] == 'string_promena'
    assert data['price'] == 20
    assert "id" in data


def test_get_book():
    response = client.post("/categories", json={"name": "test_category" + str(randint(1000000, 9999999)),
                                                "description": "test_description2"})
    data_category = response.json()
    response = client.post(
        "/books",
        json={"title": "string_promena",
              "author": "string_promena",
              "price": 20,
              "category_ids": [data_category['id']]})

    data_new_user = response.json()

    # test get valid book
    response = client.get('/books/' + str(data_new_user['id']))
    data_get_user = response.json()
    assert data_new_user['id'] == data_get_user['id']
    assert data_new_user['title'] == data_get_user['title']
    assert data_new_user['author'] == data_get_user['author']
    assert data_new_user['price'] == data_get_user['price']
    assert data_category['id'] == data_get_user['categories'][0]['id']
    assert 1 == len(data_get_user['categories'])
    assert response.status_code == 200

    # test get invalid id book
    response = client.get('/books/99987991111182')
    data_get_user = response.json()
    assert data_get_user['detail'] == "Book with id 99987991111182 doesn't exist"
    assert response.status_code == 405
    # test get invalid id type
    response = client.get('/books/invalidtype')
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

    assert response.status_code == 422


def test_modify_book():
    response = client.post("/categories", json={"name": "test_category" + str(randint(1000000, 9999999)),
                                                "description": "test_description2"})
    data_category = response.json()

    response = client.post("/categories", json={"name": "test_category" + str(randint(1000000, 9999999)),
                                                "description": "test_description2"})
    data_category2 = response.json()

    modified_category = list()
    modified_category.append(data_category['id'])
    modified_category.append(data_category2['id'])
    response = client.post(
        "/books",
        json={"title": "string_promena",
              "author": "string_promena",
              "price": 20,
              "category_ids": [data_category['id']]})

    data_new_user = response.json()

    # test valid mofication
    response = client.put('/books/' + str(data_new_user['id']), json={
        "title": "change_title_1",
        "author": "change_author_1",
        "price": 1,
        "category_ids": modified_category
    })
    assert response.status_code == 200
    data_modified_user = response.json()
    assert data_modified_user['title'] == 'change_title_1'
    assert data_modified_user['author'] == 'change_author_1'
    assert data_modified_user['price'] == 1
    assert len(data_modified_user['categories']) == 2
    assert data_category['id'] == data_modified_user['categories'][0]['id']
    assert data_category2['id'] == data_modified_user['categories'][1]['id']

    # test invalid id
    response = client.put('/books/' + str(99987991111182), json={
        "title": "change_title_1",
        "author": "change_author_1",
        "price": 1,
        "category_ids": modified_category
    })
    data = response.json()
    assert response.status_code == 405
    assert data['detail'] == "Book with id 99987991111182 doesn't exist"

    # test invalid body params
    response = client.put('/books/' + str(data_new_user['id']), json={
        "title": "change_title_1",
        "author": "change_author_1",
        "price": "money",
        "category_ids": modified_category
    })
    data = response.json()
    assert response.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "price"
                ],
                "msg": "value is not a valid integer",
                "type": "type_error.integer"
            }
        ]
    }


def test_delete_book():
    response = client.post("/categories", json={"name": "test_category" + str(randint(1000000, 9999999)),
                                                "description": "test_description2"})
    data_category = response.json()

    response = client.post(
        "/books",
        json={"title": "string_promena",
              "author": "string_promena",
              "price": 20,
              "category_ids": [data_category['id']]})

    data_new_user = response.json()

    response = client.delete('/books/' + str(data_new_user['id']))

    assert response.status_code == 200
    assert response.text == '{"Deleted":true}'

    response = client.delete('/books/' + str(data_new_user['id']))
    data = response.json()
    assert response.status_code == 405
    assert data['detail'] == "Book with id " + str(data_new_user['id']) + " doesn't exist"


def test_add_category_to_book():
    response = client.post("/categories", json={"name": "test_category" + str(randint(1000000, 9999999)),
                                                "description": "test_description2"})
    data_category = response.json()

    response = client.post("/categories", json={"name": "test_category" + str(randint(1000000, 9999999)),
                                                "description": "test_description2"})
    data_category2 = response.json()


    response = client.post(
        "/books",
        json={"title": "string_promena",
              "author": "string_promena",
              "price": 20,
              "category_ids": [data_category['id']]})

    data_new_user = response.json()

    response = client.patch('/books/' + str(data_new_user['id']), json=[data_category2['id']])
    data_added_category = response.json()
    assert response.status_code == 200
    assert len(data_added_category['categories']) == 2
    assert data_added_category['categories'][0]['id'] == data_category['id']
    assert data_added_category['categories'][1]['id'] == data_category2['id']
    print(data_added_category)
