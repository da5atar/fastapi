from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# connection string
# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi"

# engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class
Base = declarative_base()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
