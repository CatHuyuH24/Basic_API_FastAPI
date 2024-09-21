# every model represents a table in the database
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base # local package
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = "posts" # go through all tables in database, if none exists with this name, create one with the following constraints
    # migration should be for Alembic
    post_id = Column(type_=Integer, primary_key=True)
    user_id = Column(ForeignKey("users.user_id", ondelete="CASCADE"),type_=Integer, nullable=False)
    title = Column(type_=String, nullable=False)
    content = Column(type_=String, nullable=True)
    published = Column(type_=Boolean, server_default='TRUE', nullable=False)
    created_at = Column(type_=TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)

    owner = relationship("User")
    
class User(Base):
    __tablename__ = "users"
    user_id = Column(type_=Integer, primary_key=True)
    email = Column(type_=String, nullable=True, unique=True)
    password = Column(type_=String, nullable=False)
    username = Column(type_=String, nullable=False)
    role = Column(type_=String, nullable=False)
    created_at = Column(type_=TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(ForeignKey("users.user_id", ondelete="CASCADE"), type_=Integer,primary_key=True)
    post_id = Column(ForeignKey("posts.post_id", ondelete="CASCADE"),type_=Integer, primary_key=True)
    upvote = Column(type_=Boolean, nullable=False)
    created_at = Column(type_=TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)