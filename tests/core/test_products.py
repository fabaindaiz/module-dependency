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

@component(
)
class TComponent2(Component):
    pass

@component(
    imports=[
        TComponent1,
        TComponent2,
    ],
    provider=providers.Factory,
)
class TProduct1(Component):
    pass

@instance(
    products=[
        TProduct1
    ],
)
class TInstance1(TComponent1):
    pass

def test_products() -> None:
    container = Container()
    TPlugin.resolve_container(container)
    injectables = list(TPlugin.resolve_providers())

    with pytest.raises(ResolutionError):
        ResolutionStrategy.injection(injectables)

    TProduct1.injection.injectable.partial_resolution = True
    injectables = ResolutionStrategy.injection(injectables)

    assert TComponent1.injection.injectable in injectables
    assert TProduct1.injection.injectable in injectables
