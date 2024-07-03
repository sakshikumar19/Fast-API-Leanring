from fastapi import FastAPI
import psycopg2 #sql driver, for talking to database
# you need psycopg for ORM as well (sqlalchemy)
from psycopg2.extras import RealDictCursor
import time
from .database import engine
from .routers import post,user,auth
from . import models
# use the bcrypt hashing algo for passwords
models.Base.metadata.create_all(bind=engine)

app=FastAPI()

# infinite loop if connection fails
# use try-except if there is a chance of some part of code to fail!
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='080509',cursor_factory=RealDictCursor)
        # cursor_factory is just that postgres doesn't return colun names during retreival, so we manually ask it to definitely give col names as wel
        cursor=conn.cursor()
        print("connection successful")
        break
    except Exception as error:
        print("connection failed: error=",error)
        time.sleep(2)
    
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message":"Hello World"}
    