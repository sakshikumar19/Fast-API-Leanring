from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import time
import psycopg2 #sql driver, for talking to database
# you need psycopg for ORM as well (sqlalchemy)
# ORM = Object Relational Mapping
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# URL FORMAT = postgresql://<username>:<password>@<ip-address>:<postgres_port>/<database>
# postgres_port is always 5432, it was configured during installation

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# for sqlite, you need to add another parameter 'connect_args'
# this is cuz sqlite runs in memory

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()

# dependency
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
# infinite loop if connection fails
# use try-except if there is a chance of some part of code to fail!
