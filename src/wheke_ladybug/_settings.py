from typing import ClassVar

from wheke import FeatureSettings


class LadybugSettings(FeatureSettings):
    __feature_name__: ClassVar[str] = "ladybug"

    connection_string: str = "database.lbug"

    extensions: ClassVar[list[str]] = ["json"]
