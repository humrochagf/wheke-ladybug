from wheke import Pod, ServiceConfig

from .cli import cli
from .routes import router
from .service import SocialService, social_service_factory

social_pod = Pod(
    "social",
    services=[ServiceConfig(SocialService, social_service_factory)],
    router=router,
    cli=cli,
)
