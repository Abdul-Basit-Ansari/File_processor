from fastapi import FastAPI
from .db import models
from .db.database import engine
from .routes import file_routes

app = FastAPI(title="FastAPI File Processor")

models.Base.metadata.create_all(bind=engine)
app.include_router(file_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI File Processor!"}