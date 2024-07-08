import io
from pathlib import Path
from typing import TYPE_CHECKING, Any, Generator

import pytest
from rich.console import Console


@pytest.fixture(autouse=True)
def snap_env(tmp_path: Path, mocker) -> Generator[dict[str, Any], None, None]:  # type:ignore [no-untyped-def]
    snap_name = "anvil-test"

    real_home = tmp_path / "home/ubuntu"
    snap_user_common = real_home / f"snap/{snap_name}/common"
    snap_user_data = real_home / f"snap/{snap_name}/2"
    snap_path = tmp_path / f"snap/2/{snap_name}"
    snap_common = tmp_path / f"var/snap/{snap_name}/common"
    snap_data = tmp_path / f"var/snap/{snap_name}/2"

    env = {
        "SNAP": str(snap_path),
        "SNAP_COMMON": str(snap_common),
        "SNAP_DATA": str(snap_data),
        "SNAP_USER_COMMON": str(snap_user_common),
        "SNAP_USER_DATA": str(snap_user_data),
        "SNAP_REAL_HOME": str(real_home),
        "SNAP_INSTANCE_NAME": "",
        "SNAP_NAME": snap_name,
        "SNAP_REVISION": "2",
        "SNAP_VERSION": "1.2.3",
    }
    mocker.patch("os.environ", env)
    yield env


@pytest.fixture(autouse=True)
def console() -> Generator[Console, None, None]:
    console = Console(file=io.StringIO())
    yield console
