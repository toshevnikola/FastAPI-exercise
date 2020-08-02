from typing import Optional
from service import CategoryService
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Path, APIRouter

from dto.request_objects import BookRequest, CategoryRequest

category_route = APIRouter()


@category_route.get("/")
def get_categories(db: Session = Depends(get_db), cs: CategoryService = Depends(CategoryService)):
    """display the homepage"""
    return cs.get_categories(db)


@category_route.post("/")
def create_category(category_request: CategoryRequest, db: Session = Depends(get_db),
                    cs: CategoryService = Depends(CategoryService)):
    return cs.create_category(db, category_request)
