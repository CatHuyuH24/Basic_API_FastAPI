from fastapi import FastAPI, status, HTTPException, Response, Depends
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models # local package
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine) # create the tables in the database

# app321 = FastAPI(); technically, app321 is not forbidden when it's about creating a FastAPI instance
app = FastAPI()


class Post(BaseModel): # a schema -> to control what the front-end can send to us (the back-end)
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# CONNECTION TO DB LOGIC
while True:
    # Keep trying to connect to DB, if sucessful then stop, else retry after 3 seconds
    try:
        #later will utilize environment variables
        conn = psycopg2.connect(host='localhost',port=5432,database='API_DB',user='postgres',password='24062004',cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print("DB connection was sucessful")
        break
    except Exception as error:
        print("Connecting to DB failed\nError: ",error)
        time.sleep(3)

# PATH OPERATION LOGIC
@app.get("/") # decorator; referencing to our FastAPI instance ('app')
async def root():
    return {"message": "Hello basic API python course"}

@app.get("/posts")
def get_all_posts():
    cursor.execute("""SELECT * FROM posts LIMIT 100""")
    posts = cursor.fetchall()
    return {"all_posts":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_one_post(JSONdata: Post): # 'JSONdata' means the body of the data wrapped inside the package sent over the Network layer
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (JSONdata.title, JSONdata.content, JSONdata.published)) # (a, b, c) --> create a tuple
    # SQL libraries like Postgres can help to sanitize the input, making sure it's not valid SQL query
    # shouldn't .execute(f"""{JSONdata.title}, {}, {}"""")--> bad practice; does not prevent SQL injection
    newly_created_post = cursor.fetchone()
    conn.commit() # to confirm and finalize the transaction
    return {"new_post": newly_created_post}

# def fetch_post(id: int):
#     for post in _my_posts:
#         if id == post['id']:
#             return post
        
    # this is server-side raising error only
# @app.get("/posts/{id}") #{id} is a 'path parameter', FastAPI will automatically extract this id
# def get_one_post(id):
#     try:
#         id_wanted = int(id)
#         return find_post(id_wanted)
#     except:
#         print("Trying to GET a post with ID:\nException occurred while converting ID to int type")
#         raise ValueError("ID received is not a valid number (not convertable to int)") 

@app.get("/posts/{id}") # with 'path parameter', should be careful with the order of functions defined (FastAPI will go from top to bottom and 'id' in this case is more like a place-holder for an abitrary input after the 'posts/')
def get_one_post(id: int): # this is FastAPI's help to preprocess the input passed from the client
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with ID {id} was NOT FOUND")
    
    return {"post":post}


# def find_index_post(id: int):
#     for i,p in enumerate(_my_posts):
#         if p['id'] == id:
#             return i
        
@app.delete("/posts/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_one_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(id,))
    deleted_post = cursor.fetchone()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does NOT EXIST")
        # return {"message":f"post with id {id} is deleted successfully"} # NO! WE DON'T WANT TO SEND ANY DATA BACK
    
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}")
def update_one_whole_post(id:int, JSONdata: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(JSONdata.title,JSONdata.content, JSONdata.published,id))
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} DOES NOT EXIST')

    conn.commit()
    return {"updated_post":updated_post}

@app.get("/testing")
def test_post(db: Session = Depends(get_db)):
    return {"message":"testing ok"}
