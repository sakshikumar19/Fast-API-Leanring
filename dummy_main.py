from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app=FastAPI()

my_posts=[{"title":"hey","content":"this is sakshi","id":1},{"title":"i love csk","content":"best ever","id":2}]

# Path opertion/Route - function + decorator
# async is optional, technically
# root is an arbitrary name, so keep it as descriptive according to the task it does
# return sends the data to the USER/CLIENT 
# you can check the message delivered on the website
# JSON is the universal language of APIs
# the decorator is v powerful. it is what makes the function a fastapi method
# app is the fastapi instance and get is a HTTP method (get,post,delete,put,head,connect,options,trace,etc)
# "/" is the url a user should hit to "get" the function output
@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/posts") # get is for retrieving data
def get_posts():
    return {"data":my_posts} #fastapi automatically serializes the dict (into json)

# if same URLs wrap different func, the first one will be run!!!
# POSTMAN - APi tester if you don't have a full fledged front end!

class Post(BaseModel):
    title:str
    content:str
    published:bool = True #default value
    rating: Optional[int] = None
    # check docs to see available data types for pdantic schema
# note that even if you enter int in the title, as long as it is convertible to string, all is well
# 
# without schema - just for learning
@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
# payload variable stores the Body info of the post req from user and converts to a python dict
    print(payload)
    return {"Message":"Successfully created post!"}
# go to postman post req url, go to Body--> raw --> json --> type in your post

# pydantic is used to define a schema
# it is not limited to fast API, it can be used in regular python


# with schema
@app.post("/posts", status_code=status.HTTP_201_CREATED) #because fastapi generally ends up sending 200 which is not appropriate
def create_post(new_post: Post):
# validates type of data sent by user. If not correct, it throws an error!
# every new Post object has a method 'dict' to convert to a python dictionary.
    print(new_post.dict())
    print(new_post)
    
    post_dict=new_post.dict()
    post_dict['id']=randrange(0,100000000000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

# CRUD: Create - post, Read - get, Update - put/patch, delete- Delete
# posts/{id} - as fastapi assigns unique id to each new post
# put - all fields need to be sent, even if most fields don't change
# patch - only the fields you want to change

# create collection on postman for saving your requests    

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/posts/{id}") # id is the path parameter
def get_post(id: int, response: Response): #converts to int as json always serializes data
    post=find_post(id)
    
    # this response is needed because otherwise the response of 200 and the user doesn't know what went wrong
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message":f"post with {id} was not found"}
        
    # no need to convert if you've asked fastapi to validate it in args itself
    return {"post details": post}

# Why the error on this URL???
# ORDER MATTERS
# /posts/latest route is actually matching with /posts/{id}
# so the solution is to put this func above the id one
@app.get("/posts/latest")
def get_latest():
    post=my_posts[len(my_posts)-1]
    return {"detail":post}

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i;
        
            

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index=find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} does not exist")
    # you need to do this explicitly as without countering this exception, error raised is 500 internal server error
    # this happens cuz index=None returns error while searching
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
# do not pass any other message when you pass a 204 status


@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    
    index=find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    print(post.dict())
    return {"Msg":f"Updated post as {post_dict}"}

# to see the automatically generated docs, just go to the local_url/docs - uses SWAGGER UI
# local_url/reduc -- different UI docs
