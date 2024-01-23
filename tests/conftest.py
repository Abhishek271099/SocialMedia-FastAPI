from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from alembic import command
from app.oauth2 import create_access_token
from app import models
import pytest

SQLALCHEMY_DATABSE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABSE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db        # new database for testing purpose


@pytest.fixture(scope="function") # scope=function- delete TestClient after running the function and create brand new one for the next one.
def client():
    Base.metadata.create_all(bind=engine)
    # run our code before we run our test
    yield TestClient(app) 
    # run our code after our test finishes
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user2(client):
    user_data = {"email": "hello1234@gmail.com", "password": "password1234"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture          # for test_post.py
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture         # for test_post.py
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user["id"]
    }, {
        "title": "second title",
        "content": "second content",
        "owner_id": test_user["id"]
    }, {
        "title": "third title",
        "content": "third title",
        "owner_id": test_user["id"]
    }, {
        "title": "third title",
        "content": "third title",
        "owner_id": test_user2["id"]
    }]
    
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)

    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user["id"]),
    #                  models.Post(title="second title", content="second content", owner_id=test_user["id"]),
    #                  models.Post(title="third title", content="third content", owner_id=test_user["id"])])
    
    session.commit()
    posts = session.query(models.Post).all()
    return posts