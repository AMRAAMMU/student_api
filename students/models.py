#models.py
from sqlalchemy import  Column,  Integer, String,DateTime
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    name=Column(String)
    email=Column(String)
    password=Column(String)
    age=Column(Integer)
    department=Column(Integer)
     



class PasswordResetToken(Base):
    __tablename__ = "ResetPassword"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    token = Column(String)