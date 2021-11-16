from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# db
my_posts = [
    {"title": "Hello", "content": "World", "id": 1},
    {"title": "favorite foods", "content": "Pizza", "id": 2},
]

# Pydantic Schema
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


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = [post for post in my_posts if post["id"] == post_id]
    if post:
        return {"post_detail": f"Here is your post {post}"}
    return {"error": "post not found"}


@app.post("/posts")
def create_posts(post: Post):
    # print(post)
    post_dict = post.dict()
    post_dict["id"] = len(my_posts) + 1
    # post_dict["id"] = randrange(1, 10000000) # or generate random id
    my_posts.append(post_dict)
    return {
        "message": "Post created successfully.",
        "data": post_dict,
    }
