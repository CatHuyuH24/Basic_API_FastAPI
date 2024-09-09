from typing import List
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy import and_
from sqlalchemy.orm import Session
from pydantic import ValidationError

from .. import models, schemas
# from ..router.main import router # NOT CORRECT! --> USER ROUTERS
from ..database import get_db
from . import oauth2

router = APIRouter( prefix="/posts", tags=['Posts'])


@router.get("/admin", response_model = list[schemas.PostResponse])
def get_all_posts_for_admin(db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    if user.role != schemas.VALID_ROLES.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    posts = db.query(models.Post).all()
    return posts

# RAW SQL
# def get_all_posts():
#     cursor.execute("""SELECT * FROM posts LIMIT 100""")
#     posts = cursor.fetchall()
#     return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_one_post(post: schemas.PostCreate, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id=user.user_id,**post.model_dump(mode='json'))
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # to get the new post with its ID (like 'RETURNING' at the end in SQL)
    # return {"message":new_post} # with this way of returning, 'response_model' will not work
    return new_post

# RAW SQL
# def create_one_post(JSONdata: Post): # 'JSONdata' means the body of the data wrapped inside the package sent over the Network layer
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (JSONdata.title, JSONdata.content, JSONdata.published)) # (a, b, c) --> create a tuple
#     # SQL libraries like Postgres can help to sanitize the input, making sure it's not valid SQL query
#     # shouldn't .execute(f"""{JSONdata.title}, {}, {}"""")--> bad practice; does not prevent SQL injection
#     newly_created_post = cursor.fetchone()
#     conn.commit() # to confirm and finalize the transaction
#     return {"new_post": newly_created_post}

@router.get("/", response_model=list[schemas.PostResponse])
def get_all_posts_for_user(db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    roles = set(role for role in schemas.VALID_ROLES)
    if user.role not in roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    posts = db.query(models.Post).filter(models.Post.user_id == user.user_id).all()
    return posts

# the following is server-side raising error only
# @router.get("/posts/{id}") #{id} is a 'path parameter', FastAPI will automatically extract this id
# def get_one_post(id):
#     try:
#         id_wanted = int(id)
#         return find_post(id_wanted)
#     except:
#         print("Trying to GET a post with ID:\nException occurred while converting ID to int type")
#         raise ValueError("ID received is not a valid number (not convertable to int)") 

@router.get("/{id}", response_model=schemas.PostResponse)
def get_one_post(id: int, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(and_(models.Post.post_id == id, models.Post.user_id == user.user_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id {user.user_id} does not have any posts with id {id}")
    return post
    
# RAW SQL
# def get_one_post(id: int): # this is FastAPI's help to preprocess the input passed from the client
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with ID {id} was NOT FOUND")
#     return {"post":post}

        
@router.delete("/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_one_post(id: int, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(and_(models.Post.post_id == id, models.Post.user_id == user.user_id))
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id {user.user_id} does not have any posts with id {id}")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# RAW SQL
# def delete_one_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(id,))
#     deleted_post = cursor.fetchone()
#     if deleted_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does NOT EXIST")
#         # return {"message":f"post with id {id} is deleted successfully"} # NO! WE DON'T WANT TO SEND ANY DATA BACK
#     conn.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/{id}", response_model=schemas.PostResponse, status_code=status.HTTP_200_OK)
def update_one_whole_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(and_(models.Post.post_id == id, models.Post.user_id == user.user_id))
    db_post = post_query.first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user.user_id} does not have any posts with id {id}")
    
    post_query.update(post.model_dump(mode='json'), synchronize_session=False)
    db.refresh(db_post)
    db.commit()
    return db_post
    
# RAW SQL
# def update_one_whole_post(id:int, JSONdata: Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(JSONdata.title,JSONdata.content, JSONdata.published,id))
#     updated_post = cursor.fetchone()
#     if not updated_post:
#         raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} DOES NOT EXIST')
#     conn.commit()
#     return {"updated_post": updated_post}
