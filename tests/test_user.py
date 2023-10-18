from tests.test_database import session, client
import pytest

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


def test_root(client):
    response = client.get("/")
    assert response.json() == {"message": "Hello World"}
    assert response.status_code == 200

def test_create_user(client):
    response = client.post("/user/", json={"email": "a@b.com", "password": "password"})
    assert response.status_code == 201

def test_login_user(test_user, client):
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    assert response.status_code == 200