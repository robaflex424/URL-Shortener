from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

SAQLALCHEMY_SQLITE_DATABASE_URL = "sqlite:///./url_shortener.db"

engine = create_engine(
  SAQLALCHEMY_SQLITE_DATABASE_URL,
  connect_args={
    "check_same_thread": False
  }
)

SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine
)

def get_db():
  db = SessionLocal() 
  
  try: 
    yield db 
  
  finally: 
    db.close()

Base = declarative_base()