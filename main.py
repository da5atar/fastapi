from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my API!!"}


@app.get("/posts")
def get_posts():
    return {"data": "These are your posts."}


@app.post("/createpost")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"message": "Post created successfully."}