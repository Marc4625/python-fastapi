from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from .. import models, schemas, utils
from .. database import get_db

# create router object and add a prefix 
router = APIRouter(
    prefix="/users",   # this prefix will be automatically appended to any route/link.
    tags=['Users']   # tags will help organize the http requests based on the business logics.
    
)


# Create an http request to send/create users
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut) 
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = utils.hash(user.password) 
    user.password = hashed_password

    # create new user and send it to the database
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 

    return new_user 


# Fetch user by id 
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first() 

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist.")

    return user 