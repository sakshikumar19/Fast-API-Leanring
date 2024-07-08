from fastapi import FastAPI
from .database import engine
from .routers import post,user,auth, vote
from . import models

# use the bcrypt hashing algo for passwords

# models.Base.metadata.create_all(bind=engine)
# the above command is needed to create tables if you don't use alembic. Right now, we have it in place.

app=FastAPI()

# infinite loop if connection fails
# use try-except if there is a chance of some part of code to fail!
    
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message":"Hello World"}
