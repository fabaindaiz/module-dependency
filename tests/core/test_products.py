import pytest
from dependency.core.agrupation import Plugin, PluginMeta, module
from dependency.core.declaration import Component, component, instance
from dependency.core.resolution import Container, ResolutionStrategy
from dependency.core.exceptions import DeclarationError

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
)
class TProduct1(Component):
    pass

@instance(
    component=TComponent1,
    imports=[TComponent2],
    products=[TProduct1],
)
class TInstance1(TComponent1):
    pass

def test_products() -> None:
    container = Container()
    TPlugin.resolve_container(container)
    providers = list(TPlugin.resolve_providers())

    with pytest.raises(DeclarationError):
        ResolutionStrategy.injection(providers)

    ResolutionStrategy.config.resolve_products = False
    injectables = ResolutionStrategy.injection(providers)
    assert injectables == [TComponent1.injection.injectable]
