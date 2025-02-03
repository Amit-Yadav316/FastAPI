from fastapi import form
from typing import List,Optional
from pydantic import BaseModel

class Blog(BaseModel):
    body: str=form()
    title: str=form()
    user_id:int=form()
    class Config:
        orm_mode = True

class User(BaseModel):
    name:str=form()
    email: str=form()
    password: str=form()
    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    name:str
    email: str
    blogs: List[Blog]

    class Config:
        orm_mode = True

class ShowBlog(BaseModel):
    body: str
    title: str
    user:ShowUser
    class Config:
        orm_mode = True

class Login(BaseModel):
    email:str=form()
    password:str=form()

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    email:Optional[str]=None

class PasswordReset(BaseModel):
    email:str=form()

class PasswordUpdate(BaseModel):
    new_password:str=form()
    confirm_new_password:str=form()

