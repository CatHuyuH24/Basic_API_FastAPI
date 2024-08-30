# every model represents a table in the database
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from .database import Base # local package
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = "posts" # go through all tables in database, if none exists with this name, create one with the following constraints
    # migration should be for Alembic
    id = Column(type_= Integer, primary_key = True, nullable = False)
    title = Column(type_= String, nullable = False)
    content = Column(type_= String, nullable = True)
    published  = Column(type_= Boolean,server_default='TRUE', nullable=False)
    created_at = Column(type_ = TIMESTAMP(timezone=True),server_default=text('NOW()'),nullable=False)