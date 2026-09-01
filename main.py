from fastapi import FastAPI
from database.database import Base, engine
from routers.url import url_router, redirect_router

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(url_router)
app.include_router(redirect_router)