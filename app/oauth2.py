from jose import JWTError, jwt
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') #endpoint where login is defined and token is generated

# SECRET_KEY, Algorithm (HS256), expiration time (as a user's token shouldn't be valid forever)

SECRET_KEY = '47e5eb2e04dda57f2805e207824797d4912fd8717d6b1b593402a5592752e40f'
# to generate a random hex32 string, run this in the terminal:
# openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # added the expiration time to the dict
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
    
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)): 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials", 
        headers={'WWW-Authenticate':"Bearer"}
        )
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

# basically these two functions work togther and create a dependency injection
# if you use this created dependency in any endpoints (eg: post creation must require user to be logged in), it will verify token, extract user_id and only then allow access

    