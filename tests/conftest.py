import pytest

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from database.database import Base, get_db
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient
from main import app 

SQLALCHEMY_SQLITE_MEMORY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
  SQLALCHEMY_SQLITE_MEMORY_DATABASE_URL,
  connect_args={
    "check_same_thread": False
  },
  poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine
)

@pytest.fixture
def db():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)

  db = TestingSessionLocal()

  try: 
    yield db  
  finally:
    db.close() 

@pytest.fixture
def client(db):
  def override_get_db():
    yield db 
  
  app.dependency_overrides[get_db] = override_get_db

  with TestClient(app) as client: 
    yield client 
  
  app.dependency_overrides.clear()