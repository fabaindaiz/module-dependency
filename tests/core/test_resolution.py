import pytest
from dependency.core.agrupation import Plugin, PluginMeta, module
from dependency.core.declaration import Component, component, instance, providers
from dependency.core.resolution import Container, InjectionResolver
from dependency.core.exceptions import CancelInitialization

BOOTSTRAPED: list[str] = []

@module()
class TPlugin(Plugin):
    meta = PluginMeta(name="test_plugin", version="0.1.0")

@component(
    module=TPlugin,
)
class TComponent1(Component):
    pass

@component(
    module=TPlugin,
)
class TComponent2(Component):
    pass

@component(
    imports=[TComponent1],
    provider=providers.Factory,
)
class TProduct1(Component):
    pass

@instance(
    products=[TProduct1],
    bootstrap=True,
)
class TInstance1(TComponent1):
    def __init__(self) -> None:
        BOOTSTRAPED.append("TInstance1")

@instance(
    imports=[TComponent1],
    bootstrap=True,
)
class TInstance2(TComponent2):
    def __init__(self) -> None:
        BOOTSTRAPED.append("TInstance2")
        raise CancelInitialization("Failed to initialize TInstance2")

def test_exceptions() -> None:
    container = Container.from_json("example/config.json")
    injectables = TPlugin.resolve_providers()
    assert "TInstance1" not in BOOTSTRAPED

    loader = InjectionResolver(container, injectables)
    assert "TInstance1" not in BOOTSTRAPED

    loader.resolve_dependencies()
    assert "TInstance1" in BOOTSTRAPED
    assert "TInstance2" in BOOTSTRAPED

    assert TComponent1.provide() is not None
    with pytest.raises(CancelInitialization):
        TComponent2.provide()
