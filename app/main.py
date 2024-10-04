from fastapi import FastAPI
from fastapi.middleware import cors

from .database import engine
from . import models
from .routers import posts, users, auth, votes

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

models.Base.metadata.create_all(bind=engine) # create the tables in the database using SQLAlchemy

app = FastAPI() # app321 = FastAPI(); technically, app321 is not forbidden when it's about creating a FastAPI instance

origins = ["*"] # anyone can make request to the API
app.add_middleware(cors.CORSMiddleware, 
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

# RAW SQLDatabase Connection Logic
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             port=5432,
#             database='API_DB',
#             user='postgres',
#             password='24062004',
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("DB connection was successful")
#         break
#     except Exception as error:
#         print(f"Connecting to DB failed\nError: {error}")
#         time.sleep(3)

# PATH OPERATION LOGIC
@app.get("/") # decorator; referencing to our FastAPI instance ('router')
async def root():
    return {"message": "Hello basic API python course"}

app.include_router(posts.router)
app.include_router(users.router)    
app.include_router(auth.router)
app.include_router(votes.router)