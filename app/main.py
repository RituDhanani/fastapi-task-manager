from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, task

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Task Manager API Running"}