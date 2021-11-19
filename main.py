from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

# from random import randrange

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
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} not found"
    )


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(post)
    post_dict = post.dict()
    post_dict["id"] = len(my_posts) + 1
    my_posts.append(post_dict)
    return {
        "message": "Post created successfully.",
        "data": post_dict,
    }


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    try:
        post_dict = post.dict()
        post_dict["id"] = post_id
        my_posts[post_id - 1] = post_dict
        return {"message": "Post updated successfully.", "data": post_dict}
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} not found"
        )


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    post = [post for post in my_posts if post["id"] == post_id]
    if post:
        my_posts.remove(post[0])
        print(f"post {post_id} was deleted")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} not found"
    )
