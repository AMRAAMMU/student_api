#schemas.py
from pydantic import BaseModel
from typing import Optional



class User_student(BaseModel):
    name:str
    email:str
    password:str
    age:int
    department:str


class show_user(BaseModel):
    name:str
    email:str
    age:int
    department:str
    class Config():
        orm_mode=True

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class ps(BaseModel):
    password:str
    confirm_password:str
    class Config():
        orm_mode=True 



class TokenData(BaseModel):
    email: Optional[str]=None  


class StudentBase(BaseModel):
    password:str
    confirm_password:str

class Blog(StudentBase):
    class Config():
     orm_mode=True