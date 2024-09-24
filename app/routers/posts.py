
from .. import model,Schemas,utilities
from sqlalchemy.orm import Session
from fastapi import Body, FastAPI, HTTPException ,Response,status,Depends,APIRouter
from ..database import get_db
from typing import Optional,List

#Router will be call from main file
#if we user prefix, all the route operations in decorators can be reduced.
#tags will help with Swagger documentation
router=APIRouter(
    prefix="/posts",
    tags=['Posts'] 
)

#Fetch all the data -----------------------------------------------------------------------------------------
@router.get("/",response_model=List[Schemas.Response])
def get_post(db: Session = Depends(get_db)):
    posts=db.query(model.Post).all()
    return posts

# Fetch data with particular Id------------------------------------------------------------------------------
@router.get("/{id}",response_model=Schemas.Response)
def get_post(id:int,response : Response,db: Session = Depends(get_db)):
    # cursor.execute("""Select * from posts where id = (%s)""",(id,))
    # post=cursor.fetchone()
    post=db.query(model.Post).filter(model.Post.id==id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    post=post.first()
    return post


#Create a new record --------------------------------------------------------------------------------------------
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=Schemas.Response)
def create(data: Schemas.CreatePost,db: Session = Depends(get_db)):
    # cursor.execute("""Insert Into posts (title,content,published) values (%s,%s,%s) returning *""",
    #                (data.title,data.content,data.publish))
    # conn.commit()
    # post=cursor.fetchall()
    
    #below method works but become hassle if we have too many attributes we can unpack dicitionary instead
    #new_post=model.Post(title=data.title,content=data.content,published=data.published)

    #unpack dictionary
    new_post=model.Post(**data.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#Delete Posts ------------------------------------------------------------------------------------
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int,db: Session = Depends(get_db)):
    # cursor.execute("""Delete from posts where id =(%s) returning *""",(id,))
    # deleted=cursor.fetchone()
    # conn.commit()
    post=db.query(model.Post).filter(model.Post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Updating existing records in DB-----------------------------------------------------------
@router.put("/{id}",response_model=Schemas.Post)
def put(id:int,data:Schemas.UpdatePost,db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE  posts set title = %s , content = %s , published = %s where id =(%s) returning *""",
    #                (data.title,data.content,data.publish,id))
    # updated=cursor.fetchone()
    # conn.commit()
    query=db.query(model.Post).filter(model.Post.id==id)
    post=query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    query.update(data.model_dump(),synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
