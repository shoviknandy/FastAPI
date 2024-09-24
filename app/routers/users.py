
from .. import model,Schemas,utilities
from sqlalchemy.orm import Session
from fastapi import Body, FastAPI, HTTPException ,Response,status,Depends,APIRouter
from ..database import get_db

router=APIRouter(
    prefix="/user",
    tags=['Users']
)
#----------------------------------------- For USers----------------------------------------------------------
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=Schemas.UserResponse)
def create_user(data: Schemas.UserCreate,db: Session = Depends(get_db)):

    hashed_password=utilities.hash(data.password)
    data.password=hashed_password
    new_user=model.User(**data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}",response_model=Schemas.UserResponse)
def get_user(id:int,db: Session = Depends(get_db)):
    user=db.query(model.User).filter(model.User.id==id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id : {id} not found")
    return user