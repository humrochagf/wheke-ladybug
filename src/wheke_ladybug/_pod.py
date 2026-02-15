from wheke import Pod, ServiceConfig

from ._service import LadybugService, ladybug_service_factory

ladybug_pod = Pod(
    "ladybug",
    services=[
        ServiceConfig(
            LadybugService,
            ladybug_service_factory,
            is_singleton=True,
            singleton_cleanup_method="dispose",
        ),
    ],
)
