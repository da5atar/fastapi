from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter()


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    requested_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not requested_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    return requested_post


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_posts(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    print(current_user)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # to get the new post
    return new_post


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
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


@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(
    post_id: int,
    post: schemas.UpdatePost,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
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
    return updated_post
