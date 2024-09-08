# every model represents a table in the database
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from .database import Base # local package
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = "posts" # go through all tables in database, if none exists with this name, create one with the following constraints
    # migration should be for Alembic
    post_id = Column(type_=Integer, primary_key=True, nullable=False)
    user_id = Column(ForeignKey("users.user_id", ondelete="CASCADE"),type_=Integer, nullable=False)
    title = Column(type_=String, nullable=False)
    content = Column(type_=String, nullable=True)
    published = Column(type_=Boolean, server_default='TRUE', nullable=False)
    created_at = Column(type_=TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)

class User(Base):
    __tablename__ = "users"
    user_id = Column(type_=Integer, primary_key=True, nullable=False)
    email = Column(type_=String, nullable=True, unique=True)
    password = Column(type_=String, nullable=False)
    username = Column(type_=String, nullable=False)
    role = Column(type_=String, nullable=False)
    created_at = Column(type_=TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
