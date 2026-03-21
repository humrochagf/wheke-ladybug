from pydantic import BaseModel, ConfigDict


class Meta(BaseModel):
    model_config = ConfigDict(extra="allow")


class User(BaseModel):
    id: int | None = None
    name: str
    meta: Meta


class Post(BaseModel):
    id: int | None = None
    message: str
