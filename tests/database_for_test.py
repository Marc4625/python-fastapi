import pytest 
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.orm_api_main import app
from app.config import settings
from app.database import get_db, Base


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:4625@localhost:5432/test_pythonfastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/test_{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL) 

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine) 

# Base = declarative_base()

# create a session to the database
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db 



# client = TestClient(app)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)  
    Base.metadata.create_all(bind=engine) 
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db 
    ### run our code before we run our test
    # Base.metadata.drop_all(bind=engine) ### drop all tables after the tests run. 
    # Base.metadata.create_all(bind=engine)  ### create all tables before the tests run.
    yield TestClient(app)
    ### run our code after our test finishes
    
