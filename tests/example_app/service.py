from typing import Annotated

from fastapi import Depends
from svcs import Container
from svcs.fastapi import DepContainer
from wheke import WhekeSettings, get_service, get_settings

from wheke_ladybug import LadybugService, get_ladybug_service

from .repository import PostRepository, UserRepository


class SocialService:
    settings: WhekeSettings

    users: UserRepository
    posts: PostRepository

    def __init__(
        self,
        *,
        settings: WhekeSettings,
        ladybug_service: LadybugService,
    ) -> None:
        self.settings = settings
        self.users = UserRepository(ladybug_service)
        self.posts = PostRepository(ladybug_service)


def social_service_factory(container: Container) -> SocialService:
    return SocialService(
        settings=get_settings(container, WhekeSettings),
        ladybug_service=get_ladybug_service(container),
    )


def get_social_service(container: Container) -> SocialService:
    return get_service(container, SocialService)


def _social_service_injection(container: DepContainer) -> SocialService:
    return get_social_service(container)


SocialServiceInjection = Annotated[SocialService, Depends(_social_service_injection)]
