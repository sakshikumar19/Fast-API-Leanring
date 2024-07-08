from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router =APIRouter(
    prefix='/posts',
    tags=['Posts Routes'] # to fix the API documentation by grouping for easier understanding

)
# prefeix ensures you don't need to repeat the same route url everywhere
# ensure that all the decorators start with your prefix and remmove it
    
# @router.get("/", response_model=List[schemas.PostResponse]) # get is for retrieving data
@router.get("/", response_model=List[schemas.PostOut])
# List is specifying that the pydantic model acts on a list of posts
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), Limit: int = 10, skip: int = 0, search: Optional[str] = ""): 
    # Limit is the query parameter for filtering results, here it means get 10 posts as default
    # This skips the first skip number of posts.
    # skip helps in pagination!
    # search just requires keywords matching
    # to perform a search for keypharses, instead os space in URL, use -- %20
    # {{URL}}/posts/limit=7&skip=2&search=xyz%20abc
    # {{URL}}/posts/skip=2&search=xyz -- limit set to default
    
    # cursor.execute("""SELECT * FROM public.posts""")
    # posts=cursor.fetchall()
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    
    # the below code is for joins so that we can count votes on each post
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    # sqlaclchemy has default of inner joins unline psql. So we have to specify that!
    
    return results #fastapi automatically serializes the dict (into json)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) #because fastapi generally ends up sending 200 which is not appropriate
# response_model uses schema deciding what info to send to the user
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published)
    # )
    #   # we need to use format specifiers to avpid sql injection attacks
    # conn.commit()
    # new_post = cursor.fetchone()  
    
    # new_post = models.Post(title=post.title, content=post.content, published = post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # instead of having to type all the fields and pass to the table, we can directly unpack the dictionary
    # pydantic ensures the posts are in the right schema!
    # owner_id is taken from the token itself, cuz like in twitter you don't have to pass in your account details before creating post (after having logged in)
    db.add(new_post)
    db.commit() # cannot create a new entry without commiting
    db.refresh(new_post) # this is a replacement for RETURNING statement in SQL 
    return new_post


@router.get("/{id}", response_model=schemas.PostOut) # id is the path parameter
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)): #converts to int as json always serializes data
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),)) # convert to str to remove potential issues
    # # the comma is quite important, dk why
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first() # instead of all() cuz we know only one post can have that id
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} was not found")
    return post


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),)) 
    # deleted_post = cursor.fetchone() 
    # conn.commit()  
    
    query = db.query(models.Post).filter(models.Post.id == id)
    post_to_delete = query.first()
    
    if post_to_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} does not exist")
    
    if post_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized for performing requested action")
    query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post:schemas.PostBase, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s,content = %s, published = %s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = query.first()
    
    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} does not exist")

    if post_to_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized for performing requested action")

    query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return query.first()
