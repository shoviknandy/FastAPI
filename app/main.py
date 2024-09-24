from random import randint, randrange
import time
from typing import Optional,List
from fastapi import Body, FastAPI, HTTPException ,Response,status,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model,Schemas,utilities
from .database import engine,get_db
from sqlalchemy.orm import Session

from .routers import posts,users


model.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(posts.router)
app.include_router(users.router)

# while True:
#     try:
#         conn=psycopg2.connect(host='localhost',database='fastapi',
#                             user='postgres',password='password',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("DB Connected")
#         break
#     except Exception as error:
#         print(f"Connection failed with Exception : {error}")
#         time.sleep(2)

@app.get("/")
def root():
    return {"Message": "API"}










  

