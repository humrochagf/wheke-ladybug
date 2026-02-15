from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from typer.testing import CliRunner
from wheke import WhekeSettings

from wheke_ladybug import LadybugSettings

from .example_app import build_wheke


@pytest.fixture
def settings(tmp_path: Path) -> WhekeSettings:
    ladybug_settings = LadybugSettings(
        connection_string=str(tmp_path / "test.lbug"),
    )
    return WhekeSettings(
        features={
            ladybug_settings.__feature_name__: ladybug_settings.model_dump(),
        }
    )


@pytest.fixture
def client(settings: WhekeSettings) -> Generator[TestClient]:
    wheke = build_wheke(settings)
    runner = CliRunner()
    cli = wheke.create_cli()

    # setup
    result = runner.invoke(cli, ["social", "create-db"])
    assert result.exit_code == 0

    with TestClient(build_wheke(settings).create_app()) as client:
        yield client
