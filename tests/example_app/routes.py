from collections.abc import Sequence

from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED

from .models import Post, User
from .service import SocialServiceInjection

router = APIRouter(tags=["social"])


@router.get("/users")
async def list_users(service: SocialServiceInjection) -> Sequence[User]:
    return await service.users.list()


@router.post("/users", status_code=HTTP_201_CREATED)
async def create_user(user: User, service: SocialServiceInjection) -> User:
    await service.users.create(user)
    return user


@router.get("/users/{user_id}/posts")
async def list_posts(
    user_id: int, service: SocialServiceInjection
) -> Sequence[Post]:
    return await service.posts.list(user_id)


@router.post("/users/{user_id}/posts", status_code=HTTP_201_CREATED)
async def create_post(
    user_id: int, post: Post, service: SocialServiceInjection
) -> None:
    await service.posts.create(user_id, post)
