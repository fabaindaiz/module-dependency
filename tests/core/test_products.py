import pytest
from dependency_injector import providers
from dependency.core.agrupation import Plugin, PluginMeta, module
from dependency.core.declaration import Component, component, instance
from dependency.core.resolution import Container, ResolutionStrategy
from dependency.core.exceptions import ResolutionError

@module()
class TPlugin(Plugin):
    meta = PluginMeta(name="test_plugin", version="0.1.0")

@component(
    module=TPlugin,
)
class TComponent1(Component):
    pass

@component()
class TComponent2(Component):
    pass

@component(
    imports=[
        TComponent2,
    ],
    provider=providers.Factory,
)
class TProduct1(Component):
    pass

@instance(
    imports=[
        TProduct1,
    ],
)
class TInstance1(TComponent1):
    pass

def test_products() -> None:
    container = Container()
    TPlugin.resolve_container(container)
    injectables = list(TPlugin.resolve_providers())
    assert injectables == [TComponent1.injection.injectable]

    with pytest.raises(ResolutionError):
        ResolutionStrategy.injection(injectables)

    TProduct1.injection.injectable.partial_resolution = True
    ResolutionStrategy.injection(injectables)

    assert TComponent1.injection.injectable.is_resolved
    assert TProduct1.injection.injectable.is_resolved
