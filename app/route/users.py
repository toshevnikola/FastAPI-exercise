from typing import Optional

from app.database import SessionLocal
from app.service import UserService
from sqlalchemy.orm import Session
from fastapi import Depends, Path, APIRouter
from app.dto.request_objects import UserRequest
from app.main import *
from app.database import get_db
from passlib.context import CryptContext

user_route = APIRouter()

user_service = UserService


@user_route.get("")
def get_users(user_filter: Optional[str] = None,
              db: Session = Depends(get_db), us: UserService = Depends(user_service)):
    """Get all or filtered users """
    return us.get_users(db, user_filter=user_filter)


@user_route.post("")
def create_user(user_request: UserRequest, db: Session = Depends(get_db),
                us: UserService = Depends(user_service)):
    """Create new user"""
    return us.create_user(db, user_request)


@user_route.get("/{username}")
def get_user(username: str = Path(Optional[int]), db: Session = Depends(get_db),
             us: UserService = Depends(user_service)):
    """Get user with specified id"""
    return us.get_user(username, db)


@user_route.delete("/{username}")
async def delete_user(username: str = Path(Optional[int]), db: Session = Depends(get_db),
                      us: UserService = Depends(user_service)):
    """Delete user with specified id"""
    return us.delete_user(username, db=db)

