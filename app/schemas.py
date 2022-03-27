from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint
from pydantic.networks import EmailStr

# Pydantic Schemas

# Requests
# posts
class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = None


class CreatePost(Post):
    pass


class UpdatePost(Post):
    # only fields that can be updated
    # title: Optional[str] = None
    # content: Optional[str] = None
    # is_published: Optional[bool] = None
    # rating: Optional[int] = None
    pass


# users
class User(BaseModel):
    email: EmailStr


class UserInDB(User):
    # is_active: bool
    # is_admin: bool

    class Config:
        orm_mode = True


class CreateUser(User):
    password: str


# login
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str

# votes
class Vote(BaseModel):
    post_id: int
    direction: conint(ge=0, le=1)

# Responses

# posts
class PostResponse(Post):
    # id: int
    created_at: datetime
    user_id: int
    owner: UserInDB

    class Config:
        orm_mode = (
            True  # makes pydantic read the fields from the ORM (SQLAlchemy) model
        )


# users
class CreateUserResponse(User):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class GetUserResponse(User):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# votes
class PostWithVoteResponse(BaseModel):
    Post: PostResponse
    votes: Optional[int]

    class Config:
        orm_mode = True
