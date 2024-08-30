from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# 'postgresql://<username>:<password>@<ip address/hostname>/<database name>'
SQL_ALCHEMY_DATABASE_URL = "postgresql://postgres:24062004@localhost/API_DB"
engine =create_engine(SQL_ALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()