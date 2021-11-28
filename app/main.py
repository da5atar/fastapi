from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor  # to get the columns names
from time import sleep
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

# from random import randrange

app = FastAPI()

# db
models.Base.metadata.create_all(bind=engine)


while True:
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
        break
    except Exception as error:
        print("Unable to connect to the database")
        print("Error:", error)
        sleep(5)
        continue


# test endpoint
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    try:
        posts_query = db.query(models.Post)
        posts = posts_query.all()
        print(posts_query)
        return {"status": "success", "data": posts}
    except Exception as error:
        print(error)
        return {"status": "error"}


# routes (endpoints)
@app.get("/")
async def root():
    return {"message": "Welcome to my API!!"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    requested_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not requested_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    return {"data": requested_post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # to get the new post
    return {"message": "Post created successfully.", "data": new_post}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post_to_delete = post_query.first()
    if not post_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: schemas.UpdatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post_to_update = post_query.first()
    if not post_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    updated_post = post_query.first()
    return {"message": "Post updated successfully.", "data": updated_post}


# helper functions
def get_posts_from_db():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return posts


def get_post_from_db(post_id):
    cursor.execute(
        "SELECT * FROM posts WHERE id = %s", (post_id,)
    )  # comma after post_id is needed for single value
    post = cursor.fetchone()
    return post


def create_post_in_db(post: schemas.Post):
    cursor.execute(
        "INSERT INTO posts (title, content, is_published, rating) VALUES (%s, %s, %s, %s) RETURNING *",
        (post.title, post.content, post.is_published, post.rating),
    )
    created_post = cursor.fetchone()
    conn.commit()
    return {"Post created": created_post}


def delete_post_in_db(post_id):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (post_id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    return deleted_post


def update_post_in_db(post_id, post_update):
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, is_published = %s, rating = %s WHERE id = %s RETURNING *",
        (
            post_update.title,
            post_update.content,
            post_update.is_published,
            post_update.rating,
            post_id,
        ),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    return updated_post
