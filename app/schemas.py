from datetime import datetime
from re import I
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
# you need a schema for everything
# eg: you may not want the user to be allowed to update every field

class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email:EmailStr
    password: str


class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True
    owner: UserOut # this is the user object created using sqlalchemy relationship

class PostOut(BaseModel):
    Post: PostBase
    votes: int
    
    class config:
        from_attributes = True
    

class PostCreate(PostBase):
    pass # inheritance

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int # i want the response model to send back owner_id, however i don't want the user to have to add it himself
    # hence owner_id is in the schema of response only. The token logic handles extracting owner_id from the created posts.
    
    # maybe you may not want to send back created_at and id as user didn't declare those
    # but our frontend definitely wants that
    # no need to mention title, content and published as we inherited PostBase class
    
    class Config:
        from_attributes = True
    # this is basically because when returning data to the user, we return the ORM model
    # however, pydantic expects a python dict
    # this class handles that edge case

# pip install email-validator
class UserCreate(BaseModel):
    email: EmailStr
    password: str
        
class Token(BaseModel):
    access_token: str
    token_type: str # usually bearer

class TokenData(BaseModel):
    id: Optional[int] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
# dir is the direction of vote (either 1 or 0 to like or unlike (not dislike, that would need another class))
# conint is like a validator to ensure that user input is less than or equal to 1
# the issue is it allows -ve values as well but we can sort that out later