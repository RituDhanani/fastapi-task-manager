from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, task
from app.routers import user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(user_router.router)

@app.get("/")
def home():
    return {"message": "Task Manager API Running"}