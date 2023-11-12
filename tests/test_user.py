from jose import jwt
import pytest
from app.schemas import Token
from app.config import  settings



def test_root(client):
    response = client.get("/")
    assert response.json() == {"message": "Hello World"}
    assert response.status_code == 200

def test_create_user(client):
    response = client.post("/user/", json={"email": "a@b.com", "password": "password"})
    assert response.status_code == 201


def test_login_user(test_user, client):
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    assert test_user["id"] == payload.get("user_id")
    assert login_res.token_type == "bearer"
    assert response.status_code == 200

def test_failed_login(test_user, client):
    response = client.post("/login", data={"username": "euifhew", "password": test_user["password"]})
    print(response.json)
    assert response.status_code == 403

