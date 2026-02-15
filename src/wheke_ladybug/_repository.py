from ._service import LadybugService


class LadybugRepository:
    db: LadybugService

    def __init__(self, ladybug_service: LadybugService) -> None:
        self.db = ladybug_service
