import logging

import pytest
from pydantic import BaseModel
from dependency.core.agrupation import Plugin, PluginMeta, Module, module
from dependency.core.resolution import Container
from dependency.core.exceptions import ProvisionError


class TPluginConfig(BaseModel):
    field1: str
    field2: int


@module()
class TPlugin(Plugin):
    meta = PluginMeta(name="test_plugin", version="0.1.0")
    config: TPluginConfig


@module()
class TPluginNoConfig(Plugin):
    meta = PluginMeta(name="test_plugin_no_config", version="0.1.0")


@module(module=TPlugin)
class TChildModule(Module):
    pass


def test_agrupation_missing_config_fields() -> None:
    """Config con campos faltantes lanza ProvisionError."""
    container = Container.from_dict({"field1": "value"})  # falta field2

    with pytest.raises(ProvisionError):
        TPlugin.resolve_container(container)


def test_agrupation_correct_config_fields() -> None:
    container = Container.from_dict({"field1": "value", "field2": 100})

    TPlugin.resolve_container(container)
    assert TPlugin.config.field1 == "value" and TPlugin.config.field2 == 100


def test_agrupation_no_config() -> None:
    """Plugin sin config declarada no falla al resolver el container."""
    container = Container.from_dict({"field1": "value", "field2": 100})
    TPluginNoConfig.resolve_container(container)  # no debe lanzar


def test_agrupation_nested_module_reference() -> None:
    """Módulo anidado construye el reference correcto."""
    assert TChildModule.injection.parent == TPlugin.injection
    assert TChildModule.injection.reference == "TPlugin.TChildModule"


# --------------------------------------------------------------------------------------
# A plugin that needs no configuration is the ordinary case, not a mistake (D-054).
# --------------------------------------------------------------------------------------


@module()
class QuietPlugin(Plugin):
    meta = PluginMeta(name="quiet_plugin", version="0.1.0")


@module()
class WrongConfigPlugin(Plugin):
    meta = PluginMeta(name="wrong_config_plugin", version="0.1.0")
    config: int


def test_a_plugin_without_config_does_not_warn(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.WARNING, logger="dependency.loader"):
        QuietPlugin.resolve_container(Container.from_dict({}))

    assert caplog.records == []


def test_a_config_hint_that_is_not_a_basemodel_warns(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.WARNING, logger="dependency.loader"):
        WrongConfigPlugin.resolve_container(Container.from_dict({}))

    assert len(caplog.records) == 1
    assert "never be populated" in caplog.records[0].message
