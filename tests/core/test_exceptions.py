import pytest
from dependency.core.agrupation import Plugin, PluginMeta, module
from dependency.core.declaration import Component, component, instance
from dependency.core.resolution import Container, ResolutionStrategy
from dependency.core.exceptions import DeclarationError, ResolutionError

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
)
class TProduct1(Component):
    pass

@instance(
    imports=[TComponent2],
    products=[TProduct1],
)
class TInstance1(TComponent1):
    pass

@instance(
    imports=[TComponent1],
)
class TInstance2(TComponent2):
    pass

def test_exceptions() -> None:
    container = Container()
    TPlugin.resolve_container(container)
    providers = list(TPlugin.resolve_providers())

    with pytest.raises(DeclarationError):
        print(TComponent1.provide())
    with pytest.raises(ResolutionError):
        ResolutionStrategy.injection(providers)
