from typing import List,Optional
from pydantic import BaseModel

class Blog(BaseModel):
    body: str
    title: str
    user_id:int
    class Config:
        orm_mode = True

class User(BaseModel):
    name:str
    email: str
    password: str
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
    email:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    email:Optional[str]=None


