from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint


# Build a model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # default published value to true
    # rating: Optional[int] = None  # default value to None


# the class extends PostBase class.
class PostCreate(PostBase):
    pass

# user details to be sent back to the user after creation
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True 

# The response body model extends PostBase class to get its variables
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int 
    owner: UserOut

    class Config:
        orm_mode = True 

#
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True  


# Create user
class UserCreate(BaseModel):
    email: EmailStr
    password: str



# class UserOut(BaseModel):
#     id: int
#     email: EmailStr
#     created_at: datetime

#     class Config:
#         orm_mode = True 

#
class UserLogin(BaseModel):
    email: EmailStr
    password: str


#
class Token(BaseModel):
    access_token: str
    token_type: str

#
class TokenData(BaseModel):
    id: Optional[str] = None


#
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
