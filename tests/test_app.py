from fastapi import status
from fastapi.testclient import TestClient

from .utils import make_user


def test_list_users(client: TestClient) -> None:
    make_user(client)

    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert len(response_data) == 1

    assert response_data[0]["meta"]["key1"] == "value1"


def test_create_post(client: TestClient) -> None:
    user = make_user(client)

    response = client.post(f"/users/{user.id}/posts", json={"message": "hello"})
    assert response.status_code == status.HTTP_201_CREATED


def test_list_posts(client: TestClient) -> None:
    user = make_user(client)

    response = client.post(f"/users/{user.id}/posts", json={"message": "hello"})
    assert response.status_code == status.HTTP_201_CREATED

    response = client.get(f"/users/{user.id}/posts")
    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 1
