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

@router.post("", response_model=URLResponse)
async def create_url(db: db_dependency, url: URLCreate):
  short_code = generate_short_code()

  while db.query(Url).filter(Url.short_code == short_code).first() is not None: 
    short_code = generate_short_code()
  
  new_url = Url(
    original_url = str(url.original_url),
    short_code  = short_code,
    expires_at = url.expires_at
  )

  db.add(new_url)
  db.commit()
  db.refresh(new_url)

  return new_url