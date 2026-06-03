from ladybug import AsyncConnection, Connection, Database
from svcs import Container
from wheke import WhekeSettings, get_service, get_settings

from ._settings import LadybugSettings


class LadybugService:
    engine: Database
    settings: LadybugSettings

    def __init__(self, *, settings: LadybugSettings) -> None:
        self.engine = Database(settings.connection_string)
        self.settings = settings

    def initialize(self) -> None:
        with self.connection as conn:
            for extension in self.settings.extensions:
                conn.execute(
                    f"INSTALL {extension};"
                    f"LOAD {extension};"
                )

    @property
    def async_connection(self) -> AsyncConnection:
        return AsyncConnection(self.engine)

    @property
    def connection(self) -> Connection:
        return Connection(self.engine)

    def dispose(self) -> None:
        self.engine.close()


def ladybug_service_factory(container: Container) -> LadybugService:
    settings = get_settings(container, WhekeSettings).get_feature(LadybugSettings)
    service = LadybugService(settings=settings)

    service.initialize()

    return service


def get_ladybug_service(container: Container) -> LadybugService:
    return get_service(container, LadybugService)
