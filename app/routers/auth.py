from msilib import schema
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2

router =APIRouter(
    tags=['Authentication'] 
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # using OAuth2PasswordRequestForm instead of our pydantic schema as it is stadard
    # it returns ONLY username, password
    # now in postman: don't enter data in Body --> raw
    # Body --> form-data --> username (key), email (value) & password (key), 123 (value)
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    return {"access_token":access_token, "token_type":"bearer"}