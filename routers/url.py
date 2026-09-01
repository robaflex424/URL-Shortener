import datetime
from time import timezone
from typing import Annotated
from sqlalchemy.orm import Session 
from database.database import get_db
from schemas.url import (
  URLCreate, 
  URLResponse
  ) 
from fastapi import (
  APIRouter, 
  Depends, 
  HTTPException
  )
from utils.utils import (
  generate_short_code
  )
from models.url import Url
from fastapi.responses import RedirectResponse

url_router = APIRouter(
  prefix="/urls",
  tags=["urls"]
)

redirect_router = APIRouter(
  tags=["redirect"]
)

db_dependency = Annotated[Session, Depends(get_db)]

@url_router.post("", response_model=URLResponse)
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

@redirect_router.get("{short_code}", response_model=URLResponse)
async def redirect_user_to_url(db: db_dependency, short_code: str):
  url = db.query(Url).filter(Url.short_code == short_code).first()

  if url is None:
    raise HTTPException(
      status_code=404,
      detail="URL not found"
    )
  
  if url.is_active is False: 
    raise HTTPException(
      status_code=404,
      detail="URL is inactive"
    )
  
  if url.expires_at is not None and url.expires_at <= datetime.now(timezone.utc):
    raise HTTPException(
      status_code=404,
      detail="URL is expired"
    )
  
  url.click_count += 1

  db.commit() 

  return RedirectResponse(
    url=url.original_url,
    status_code=307
  )

@url_router.get("/{short_code}", response_model=URLResponse)
async def return_url_information(db: db_dependency, short_code: str):
  url = db.query(Url).filter(Url.short_code == short_code).first()

  if url is None:
    raise HTTPException(
      status_code=404,
      detail="URL not found"
    )

  if url.is_active is False: 
    raise HTTPException(
      status_code=404,
      detail="URL is inactive"
    )
  
  if url.expires_at is not None and url.expires_at <= datetime.now(timezone.utc):
    raise HTTPException(
      status_code=404,
      detail="URL is expired"
    )  

  return url