from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor  # to get the columns names

# from random import randrange

app = FastAPI()

# db
my_posts = [
    {"title": "Hello", "content": "World", "id": 1},
    {"title": "favorite foods", "content": "Pizza", "id": 2},
]

try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="postgres",
        cursor_factory=RealDictCursor,
    )
    print("Connected to database")
    cursor = conn.cursor()
except (Exception, psycopg.Error) as error:
    print("Unable to connect to the database")
    print("Error:", error)


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
    post = find_post_by_id(post_id)
    return post


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
    post_index = find_post_index(post_id)
    my_posts[post_index] = post.dict()
    return {"message": "Post updated successfully.", "data": my_posts[post_index]}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    try:
        my_posts.pop(find_post_index(post_id))
        print(f"post {post_id} was deleted")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except:
        raise


# helper functions
def find_post_by_id(post_id: int):
    post = [post for post in my_posts if post["id"] == post_id]
    if post:
        return post[0]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} not found"
    )


def find_post_index(post_id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == post_id:
            return index
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"post {post_id} not found"
    )
