import pytest
from pydantic import BaseModel
from dependency.core.agrupation import Plugin, PluginMeta, module
from dependency.core.resolution import Container, ResolutionStrategy
from dependency.core.declaration import Component, component, instance
from dependency.core.exceptions import ProvisionError

class PluginConfig(BaseModel):
    key: str

@module()
class TPlugin(Plugin):
    config: PluginConfig
    meta = PluginMeta(name="test_plugin", version="0.1.0")

@component(
    module=TPlugin,
)
class TComponent1(Component):
    pass

@instance()
class TInstance1(TComponent1):
    pass

@instance()
class TInstance2(TComponent1):
    pass

def test_validation() -> None:
    strategy: ResolutionStrategy = ResolutionStrategy()
    container = Container()

    with pytest.raises(ProvisionError):
        TPlugin.resolve_container(container)

    container = Container.from_dict({"key": "value"})
    TPlugin.resolve_container(container)
    injectables = list(TPlugin.resolve_injectables())

    strategy.injection(injectables)
    assert TComponent1.injectable.implementation != TInstance1
    assert TComponent1.injectable.implementation == TInstance2

    assert TComponent1.provider() == TInstance2.provider()
    assert TComponent1.provide() == TInstance2.provide()
