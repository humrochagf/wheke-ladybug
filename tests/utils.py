from coolname import generate
from fastapi.testclient import TestClient
from starlette import status

from .example_app.models import User

# Big ActivityPub Actor payload to ensure
# ladybug json storing is working as expected
META = {
    "id": "http://localhost:8000/actors/testuser",
    "ap_data": {
        "id": "http://localhost:8000/actors/testuser",
        "type": "Person",
        "name": "",
        "summary": "",
        "username": "testuser",
        "inbox": "http://localhost:8000/actors/testuser/inbox",
        "outbox": "http://localhost:8000/actors/testuser/outbox",
        "public_key": {
            "id": "http://localhost:8000/actors/testuser#main-key",
            "owner": "http://localhost:8000/actors/testuser",
            "public_key_pem": (
                "-----BEGIN PUBLIC KEY-----\n"
                "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAni2p5Ni2mVmHKFlOFA5w\n"
                "zBLTZS3cEdiQ/IBqeSKYcKU4TFEhaFaVy3Be4pL+vFwX+iEXpvAznEhaC6oTU2zC\n"
                "EaXFhmVInsZ3kzrz2vTeXsOIwJ4auR8fFziwewXYXUgT0/KmSlNaYMz1PbXxPS+P\n"
                "DHL7E6ovJSau8Hj7UMDpF6W0Xty8PoU/Kw9Fyt3SXBHz6h5hvNXTiqS2HxWDbtz/\n"
                "j5tZlpvxiZ/sFN2w/bsotlbe2QOF5HuLA/w7B3E1Tan8jLNO4qXEHffdUZEl92ad\n"
                "dqnhsH9MJbRp6YfNnRMd1NaHu+rDUjTur34r5oVEz766oU/ZnGlGpJsvaQmUiMW8\n"
                "XQIDAQAB\n"
                "-----END PUBLIC KEY-----\n"
            ),
        },
        "manually_approve_followers": False,
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
            {"manuallyApprovesFollowers": "as:manuallyApprovesFollowers"},
        ],
    },
    "is_local": True,
    "created_at": "2026-02-25T00:54:29.987623Z",
}


def make_user(client: TestClient) -> User:
    data = {
        "name": " ".join(generate(2)),
        "meta": META,
    }

    response = client.post("/users", json=data)
    assert response.status_code == status.HTTP_201_CREATED

    return User(**response.json())
