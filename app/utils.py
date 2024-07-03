from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(attempted_password, hashed_password):
    return pwd_context.verify(attempted_password,hashed_password)
# the user attempts a password which is un=hashed
# we first hash it and then compare with the hashed passowrd in our database
# this is done automatically by pwd_context.verify