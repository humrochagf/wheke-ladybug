from pydantic import BaseModel, Json


class User(BaseModel):
    id: int | None = None
    name: str
    meta: dict | Json


class Post(BaseModel):
    id: int | None = None
    message: str
