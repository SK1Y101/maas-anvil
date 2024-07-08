import textwrap
from typing import Any

from rich.console import Console
from sunbeam.utils import get_local_cidr_by_default_routes

from anvil.provider.local.deployment import LocalDeployment
from anvil.utils import standard_indent


class TestLocalDeployment:
    def test_generate_preseed(
        self, snap_env: dict[str, Any], console: Console
    ) -> None:
        deployment = LocalDeployment()
        result = deployment.generate_preseed(console)
        expected = f"""
        deployment:
            bootstrap:
                # Management networks shared by hosts (CIDRs, separated by comma)
                management_cidr: {get_local_cidr_by_default_routes()}"""
        assert standard_indent(result) == standard_indent(expected)
