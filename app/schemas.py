from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# Pydantic Schemas

# Requests
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


# Responses


class PostResponse(Post):
    # id: int
    created_at: datetime

    class Config:
        orm_mode = (
            True  # makes pydantic read the fields from the ORM (SQLAlchemy) model
        )
