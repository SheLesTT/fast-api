import pytest
from app import schemas
from app import models
def test_get_all_posts(authorized_client,test_posts):
    response = authorized_client.get("/posts")
    assert len(response.json()) == len(test_posts)
    assert response.status_code ==200


def test_unauthoriezed_user_cannot_get_all_posts(client, test_posts):
    response = client.get("/posts")
    assert response.status_code == 401

def test_unauthoriezed_user_cannot_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_user_cannot_get_nonexistent_post(authorized_client,test_posts):
    response = authorized_client.get(f"/posts/{13}")
    assert response.status_code == 404

def test_get_one_posts(authorized_client,test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.Post(**response.json()["Post"])
    assert post.id == test_posts[0].id
    assert response.status_code == 200


@pytest.mark.parametrize("title", "content", "publisher", [("new tittle", "new content", "new publisher"),
                                                           ("super title","super content", "super publisher")])
def create_post(authorized_client, test_user, test_posts,title, content, publisher):
    res = authorized_client.post("/posts/", json = {'title': title, 'content': content, "publisher" : publisher})
    assert res.status_code == 201