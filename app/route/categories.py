from typing import Optional
from app.service import CategoryService
from app.database import MySqlConnection
from sqlalchemy.orm import Session
from fastapi import Depends, Path, APIRouter
from app.dto.request_objects import CategoryRequest
from app.main import *

category_route = APIRouter()

category_service = CategoryService

get_db = MySqlConnection().get_db

@category_route.get("")
def get_categories(name_filter: Optional[str] = None, description_filter: Optional[str] = None,
                   db: Session = Depends(get_db), cs: CategoryService = Depends(category_service)):
    """Get all or filtered categories """
    return cs.get_categories(db, name_filter=name_filter, description_filter=description_filter)


@category_route.post("")
def create_category(category_request: CategoryRequest, db: Session = Depends(get_db),
                    cs: CategoryService = Depends(category_service)):
    """Create new category"""
    return cs.create_category(db, category_request)


@category_route.get("/{id}")
def get_category(id: int = Path(Optional[int]), db: Session = Depends(get_db),
                 cs: CategoryService = Depends(category_service)):
    """Get category with specified id"""
    return cs.get_category(id, db)


@category_route.delete("/{id}")
async def delete_category(id: int = Path(Optional[int]), db: Session = Depends(get_db),
                          cs: CategoryService = Depends(category_service)):
    """Delete category with specified id"""
    return cs.delete_category(id=id, db=db)


@category_route.put("/{id}")
async def modify_category(id: int, modified_category: CategoryRequest, db: Session = Depends(get_db),
                          cs: CategoryService = Depends(category_service)):
    """Modify Category"""

    category = cs.validate_category_id(id, db)
    if category: return cs.modify_category(category, modified_category, db)
