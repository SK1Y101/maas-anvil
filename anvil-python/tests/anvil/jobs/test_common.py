from typing import Any

from click import BadParameter
from click.core import Command, Context
import pytest

from anvil.jobs.common import Role, roles_to_str_list, validate_roles


@pytest.fixture
def context() -> Context:
    return Context(Command("test"))


class TestRoles:
    def test_is_region(self) -> None:
        assert Role.REGION.is_region_node()
        for role in [Role.AGENT, Role.DATABASE, Role.HAPROXY]:
            assert not role.is_region_node()

    def test_is_agent(self) -> None:
        assert Role.AGENT.is_agent_node()
        for role in [Role.REGION, Role.DATABASE, Role.HAPROXY]:
            assert not role.is_agent_node()

    def test_is_database(self) -> None:
        assert Role.DATABASE.is_database_node()
        for role in [Role.REGION, Role.AGENT, Role.HAPROXY]:
            assert not role.is_database_node()

    def test_is_haproxy(self) -> None:
        assert Role.HAPROXY.is_haproxy_node()
        for role in [Role.REGION, Role.AGENT, Role.DATABASE]:
            assert not role.is_haproxy_node()


def test_roles_to_str_list() -> None:
    roles = [Role.AGENT, Role.DATABASE, Role.HAPROXY, Role.REGION]
    role_list = ["agent", "database", "haproxy", "region"]
    assert roles_to_str_list(roles) == role_list


def test_validate_valid_roles(context: Context) -> None:
    roles = [Role.AGENT, Role.DATABASE, Role.HAPROXY, Role.REGION]
    role_tuple: tuple[Any] = (  # type: ignore
        "agent",
        "database",
        "haproxy",
        "region",
    )
    assert (
        validate_roles(
            context,
            "",  # type:ignore [arg-type]
            role_tuple,
        )
        == roles
    )


def test_validate_invalid_roles(context: Context) -> None:
    role_tuple: tuple[Any] = "invalid_role"  # type: ignore
    with pytest.raises(BadParameter):
        validate_roles(context, "", role_tuple)  # type:ignore [arg-type]
