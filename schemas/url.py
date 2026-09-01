from datetime import datetime
from pydantic import BaseModel, HttpUrl

class URLCreate(BaseModel):
  original_url: HttpUrl
  expires_at: datetime | None = None

class URLResponse(BaseModel):
  id: int 
  original_url: HttpUrl
  short_code: str 
  created_at: datetime 
  expires_at: datetime | None 
  click_count: int 
  is_active: bool 
  