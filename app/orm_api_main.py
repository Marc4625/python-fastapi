from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings 


# create all columns in the models file
models.Base.metadata.create_all(bind=engine) 


# Create an instance of fastapi
app = FastAPI()

origins = ["https://www.google.com"] 

# CORS
app.add_middleware(CORSMiddleware, 
                    allow_origins=origins, 
                    allow_credentials=True, 
                    allow_methods=["*"], 
                    allow_headers=["*"],)





# save the post in the memory
# my_posts = [
#     {"title": "title of post 1", "content": "content of post 1", "id": 1},
#     {"title": "favorite foods", "content": "I like pizza", "id": 2}
# ]


# Find a post function
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p


#
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i 

#
app.include_router(post.router) 
app.include_router(user.router)
app.include_router(auth.router)  
app.include_router(vote.router) 


# Path operation
@app.get("/")
async def root():
    return {"message": "Welcome to Python API Development, and successfully deployed from CI/CD pipeline!"}



    

