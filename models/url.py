from datetime import datetime, timezone
from database.database import Base 
from sqlalchemy import Boolean, Column, DateTime, Integer, String

class Url(Base):
  __tablename__ = "url"

  id = Column(Integer, primary_key=True, index=True)
  original_url = Column(String, nullable=False)
  short_code = Column(String, nullable=False, unique=True)
  created_at = Column(DateTime, default=datetime.now(timezone.utc))
  expires_at = Column(DateTime, default=None)
  click_count = Column(Integer, default=0)
  is_active = Column(Boolean, default=True)