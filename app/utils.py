from passlib.context import CryptContext


# create an instance of hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  


# define a function to hash the password
def hash(password: str):
    return pwd_context.hash(password) 


# define a function to compare two passwords 
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) 