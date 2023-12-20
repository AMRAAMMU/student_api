#main.py
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import student, authentication,reset_password

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(student.router)
app.include_router(reset_password.router)