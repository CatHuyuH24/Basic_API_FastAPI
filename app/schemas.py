from enum import Enum
from pydantic import BaseModel, EmailStr
from datetime import datetime

# if expect to return a token from the front-end, it's best to utilize schemas
# schemas -> to control what the front-end can send to us (the back-end) and vice versa
class ResponseModel:
    class Config:
        from_attributes = True # allow Pydantic to work with ORM models (SQLAlchemy)

class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None

class VALID_ROLES(str, Enum):
    user = "user"
    admin = "admin"

class UserCreate(UserBase):
    password: str
    role: VALID_ROLES = VALID_ROLES.user

class UserResponse(UserBase, ResponseModel):
    user_id: int
    role: str
    created_at: datetime

class PostBase(BaseModel): 
    title: str
    content: str
    published: bool

class PostCreate(PostBase):
    pass

class OwnerInfo(UserBase):
    pass
class PostResponse(PostBase, ResponseModel):
    post_id: int
    created_at: datetime
    owner: OwnerInfo

class PostWithVoteCountResponse(BaseModel, ResponseModel):
    Post: PostResponse
    number_of_likes: int
    number_of_dislikes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
    role: str

class Vote(BaseModel):
    post_id: int
    upvote: bool # True for upvote, False for downvote

class VoteResponse(Vote, ResponseModel):
    post_id: int
    user_id: int
    upvote: bool

