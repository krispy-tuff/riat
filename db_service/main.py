from fastapi import FastAPI
from routes import users_router, history_router
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Database Service")

app.include_router(users_router)
app.include_router(history_router)
