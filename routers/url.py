from typing import Annotated
from sqlalchemy.orm import Session 
from database.database import get_db
from schemas.url import URLCreate, URLResponse 
from fastapi import APIRouter, Depends
from utils.utils import generate_short_code
from models.url import Url

router = APIRouter(
  prefix="/urls",
  tags=["urls"]
)

db_dependency = Annotated[Session, Depends(get_db)]
