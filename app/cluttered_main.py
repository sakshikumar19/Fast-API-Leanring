# this file is the original main.py before I was introduced to routers!

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2 #sql driver, for talking to database
# you need psycopg for ORM as well (sqlalchemy)
from psycopg2.extras import RealDictCursor
import time

from sklearn.utils import deprecated
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List

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
    
@app.get("/")
async def root():
    return {"message":"Hello World"}
    
@app.get("/posts", response_model=List[schemas.PostResponse]) # get is for retrieving data
# List is specifying that the pydantic model acts on a list of posts
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM public.posts""")
    # posts=cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts #fastapi automatically serializes the dict (into json)

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) #because fastapi generally ends up sending 200 which is not appropriate
# response_model uses schema deciding what info to send to the user
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published)
    # )
    #   # we need to use format specifiers to avpid sql injection attacks
    # conn.commit()
    # new_post = cursor.fetchone()  
    
    # new_post = models.Post(title=post.title, content=post.content, published = post.published)
    new_post = models.Post(**post.dict())
    # instead of having to type all the fields and pass to the table, we can directly unpack the dictionary
    # pydantic ensures the posts are in the right schema!
    db.add(new_post)
    db.commit() # cannot create a new entry without commiting
    db.refresh(new_post) # this is a replacement for RETURNING statement in SQL 
    return new_post


@app.get("/posts/{id}", response_model=schemas.PostResponse) # id is the path parameter
def get_post(id: int, response: Response, db: Session = Depends(get_db)): #converts to int as json always serializes data
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),)) # convert to str to remove potential issues
    # # the comma is quite important, dk why
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first() # instead of all() cuz we know only one post can have that id
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} was not found")
    return post


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),)) 
    # deleted_post = cursor.fetchone() 
    # conn.commit()  
    
    query = db.query(models.Post).filter(models.Post.id == id)
    
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} does not exist")
    
    query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post:schemas.PostBase, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s,content = %s, published = %s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = query.first()
    
    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} does not exist")
    
    query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit() 
    db.refresh(new_user) 
    return new_user

@app.get('/users/{id}',response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user =db.query(models.User).filter(models.User.id == id).first()   
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details=f"User with id: {id} does not exist") 
    return user

