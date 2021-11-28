from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post, user

app = FastAPI()

# db
models.Base.metadata.create_all(bind=engine)


# routes (endpoints)
@app.get("/")
async def root():
    return {"message": "Welcome to my API!!"}


# posts
app.include_router(post.router)

# users
app.include_router(user.router)
