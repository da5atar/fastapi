from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

my_posts = [
    {"title": "Hello", "content": "World", "id": 1},
    {"title": "favorite foods", "content": "Pizza", "id": 2},
]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Welcome to my API!!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    # print(post)
    print(post.dict())
    return {
        "message": "Post created successfully.",
        "data": post
    }