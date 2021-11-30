from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post, user, auth

app = FastAPI()

# db
models.Base.metadata.create_all(bind=engine)


# routes (endpoints)
@app.get("/")
async def root():
    return {"message": "Welcome to my API!!"}


# posts
app.include_router(post.router, prefix="/posts", tags=["posts"])

# users
app.include_router(user.router, prefix="/users", tags=["users"])

# auth
app.include_router(auth.router, prefix="/login", tags=["login"])
