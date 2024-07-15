from fastapi import FastAPI
from .database import engine
from .routers import post,user,auth, vote
from . import models

from fastapi.middleware.cors import CORSMiddleware

# use the bcrypt hashing algo for passwords

# models.Base.metadata.create_all(bind=engine)
# the above command is needed to create tables if you don't use alembic. Right now, we have it in place.

app=FastAPI()

# origins = ["https://www.google.com"]
origins = ["*"]
# apart from domain names, you can also choose what HTTP methods can be accessed, what headers are allowed, etc. Currently, all are allowed.
app.add_middleware(
    CORSMiddleware, # this interacts with requests before the req reaches the routers
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
    
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message":"Hello World"}
