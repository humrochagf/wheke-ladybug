from coolname import generate
from fastapi.testclient import TestClient
from starlette import status

from .example_app.models import User


def make_user(client: TestClient) -> User:
    data = {
        "name": " ".join(generate(2)),
        "meta": {
            "key1": "value1",
            "key2": "value2",
        },
    }

    response = client.post("/users", json=data)
    assert response.status_code == status.HTTP_201_CREATED

    return User(**response.json())
