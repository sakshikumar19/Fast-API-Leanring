from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# ORM = Object Relational Mapping

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:080509@127.0.0.1:5432/fastapi'

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
