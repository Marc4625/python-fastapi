from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from typing import List, Optional
from sqlalchemy import func 
from app import oauth2
from .. import models, schemas, oauth2
from .. database import get_db


# create router object and add a prefix
router = APIRouter(
    prefix="/posts",  # this prefix will be automatically appended to any route/link.
    tags=['Posts']  # tags will help organize the http requests based on the business logics.
) 


# 
#
# @router.get("/", response_model=List[schemas.Post]) 
@router.get("/", response_model=List[schemas.PostOut]) 
def get_posts(db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user), 
                limit: int = 10, 
                skip: int = 0, 
                search: Optional[str] = ""):
   
    print(limit) 
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).filter(models.owner_id == current_user.id).all()
    # print(posts)

    # create an Outer Left Join 
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes_count")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)

    # return posts
    return results  


#  
#
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # print(**post.dict())  # unpack the dictionary
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print(current_user.id) 
    print(current_user.email)  
    new_post = models.Post(owner_id=current_user.id, **post.dict())  # unpack the dictionary and pass it to the Post class/model
    db.add(new_post)
    db.commit() 
    db.refresh(new_post) 

    return new_post


#
# get data by id
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id == id).first() 
    
    # create an Outer Left Join  
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes_count")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    # check if post does not exist and throw error/status
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found.')

    # if post.owner_id != oauth2.current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!") 
    
    return {"post_detail": post}


# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # send query to the database
    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """, (str(id),)) 
    # deleted_post = cursor.fetchone() 
    # conn.commit() 

    # define the query
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # get the designated post by its id
    post = post_query.first() 

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist.')

    if post.owner_id != oauth2.current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!") 

    # grab the original query and delete the specific post 
    post_query.delete(synchronize_session=False) 
    db.commit() 

    return Response(status_code=status.HTTP_204_NO_CONTENT)  


# update post by id 
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 

    # send update query to the database
    post_query = db.query(models.Post).filter(models.Post.id == id)  # query to find the specific id
    post = post_query.first()  # grab the specific post correspoding to the found id

    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist.')

    if post.owner_id != oauth2.current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!")  

    post_query.update(updated_post.dict(), synchronize_session=False)  # update the sepcific post corresponding to the id 
    db.commit()  # commit change to the database

    return post_query.first()


