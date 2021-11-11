from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


# Create an instance of fastapi
app = FastAPI()

# Build a model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default published value to true
    # rating: Optional[int] = None  # default value to None

# set up a connection to postgres database
while True:
    try:
        conn = psycopg2.connect(host='127.0.0.1', database='PythonFastAPI', user='postgres', password='4625', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break 
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2) 


# save the post in the memory
my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2}
]

# Find a post function
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

#
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 



# Path operation
@app.get("/")
async def root():
    return {"message": "Welcome to Python API Development!"}

# 
@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)  # send sql query to the database 
    posts = cursor.fetchall()   # fetch data from the database
    # print(posts)
    return {"data": posts}

# 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone() 
    conn.commit() 
    #print(post)
    #post_dict = post.dict()   # convert pydantic model to dictionary
    #print(post_dict)  # display the conversion on the console/terminal
    #post_dict['id'] = randrange(0, 1000000)   # randomly generate id
    #my_posts.append(post_dict)
    return {"data": new_post}

#
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone() 
    print(post) 

    # check if post does not exist and throw error/status
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found.')
    
    return {"post_detail": post}

# Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # send query to the database
    cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """, (str(id),)) 
    deleted_post = cursor.fetchone() 
    conn.commit() 

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist.')

    return Response(status_code=status.HTTP_204_NO_CONTENT)  

#
@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    # send update query to the database
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))  
    updated_post = cursor.fetchone() 
    conn.commit() 

    if updated_post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist.')

    return {'data': updated_post}
    
