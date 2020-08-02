from typing import Optional
from service import CategoryService
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Path, APIRouter

from dto.request_objects import BookRequest, CategoryRequest

category_route = APIRouter()


@category_route.get("")
def get_categories(name_filter: Optional[str] = None, description_filter: Optional[str] = None,
                   db: Session = Depends(get_db), cs: CategoryService = Depends(CategoryService)):
    """Get all or filtered categories """
    return cs.get_categories(db, name_filter=name_filter, description_filter=description_filter)


@category_route.post("")
def create_category(category_request: CategoryRequest, db: Session = Depends(get_db),
                    cs: CategoryService = Depends(CategoryService)):
    """Create new category"""
    return cs.create_category(db, category_request)


@category_route.get("/{id}")
def get_category(id: int = Path(Optional[int]), db: Session = Depends(get_db),
                 cs: CategoryService = Depends(CategoryService)):
    """Get category with specified id"""
    return cs.get_category(id, db)


@category_route.delete("/{id}")
async def delete_category(id: int = Path(Optional[int]), db: Session = Depends(get_db),
                          cs: CategoryService = Depends(CategoryService)):
    """Delete category with specified id"""
    return cs.delete_category(id=id, db=db)


@category_route.put("/{id}")
async def modify_category(id: int, modified_category: CategoryRequest, db: Session = Depends(get_db),
                          cs: CategoryService = Depends(CategoryService)):
    """Modify Category"""

    category = cs.validate_category_id(id, db)
    if category: return cs.modify_category(category, modified_category, db)
