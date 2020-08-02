from typing import Optional

from pydantic.main import BaseModel
from sqlalchemy import Column, String, Numeric
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder

from database import engine, SessionLocal, Base
import models
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Path, Body, APIRouter
from routers.books import book_router
from database import get_db



app = FastAPI()

app.include_router(book_router, tags=["books"])
