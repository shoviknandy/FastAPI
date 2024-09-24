
from datetime import datetime
from pydantic import BaseModel,EmailStr   #Will help with Schema
#Define SChema the pydantic model 
#Pydantic model is the model we send  through API
class Post(BaseModel):
    title: str
    content:str
    published: bool =True

#Schema for creating post
class CreatePost(Post):
    pass


class UpdatePost(Post):
    published: bool



class Response(BaseModel):
    title:str
    content:str
    published:bool
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr #Validates if email syntax is correct
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode = True

