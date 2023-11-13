from fastapi.testclient import TestClient
from app.main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from ..app import  models


TESTING_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}' \
                       f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:' \
                          f'{settings.database_password}@{settings.database_hostname}:' \
                          f'{settings.database_port}/{settings.database_name}'

engine = create_engine(TESTING_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print("this code will exicute")




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
    return TestClient(app)

@pytest.fixture()
def test_user(client):
    user_data = {
        "email": "ac@b.com",
        "password": "password"
    }
    res = client.post("/user/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture()
def authorized_client(client, token):

    client.headers = {
        **client.headers,
         "Authorization": f"Bearer {token}"
    }
    print("this is headers", client.headers)
    return client




@pytest.fixture()
def test_posts(test_user,session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        }]

    def create_user_map(post):
        return models.Post(**post)

    post_map = list(map(create_user_map,posts_data))
    session.add_all(post_map)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
@pytest.fixture()
def test_posts(test_user,session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        }]

    def create_user_map(post):
        return models.Post(**post)

    post_map = list(map(create_user_map,posts_data))
    session.add_all(post_map)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
