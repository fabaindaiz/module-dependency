import pytest
from dependency_injector import providers
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
    imports=[
        TComponent1,
    ],
    module=TPlugin,
)
class TComponent2(Component):
    pass

@component(
    imports=[
        TComponent2,
    ],
    provider=providers.Factory,
    partial_resolution=True,
)
class TProduct1(Component):
    pass

@instance(
    imports=[
        TComponent1,
        TProduct1,
    ],
)
class TInstance1(TComponent1):
    pass

def test_exceptions() -> None:
    strategy: ResolutionStrategy = ResolutionStrategy()
    container = Container()

    TPlugin.resolve_container(container)
    with pytest.raises(DeclarationError):
        print(TComponent1.provide())

    with pytest.raises(DeclarationError):
        TPlugin.inject_container(container)

    TComponent2.change_parent(None)
    TPlugin.inject_container(container)
    injectables = list(TPlugin.resolve_injectables())
    assert set(injectables) == {TComponent1.injectable}

    injectables = strategy.expand(injectables)
    assert set(injectables) == {TComponent1.injectable, TProduct1.injectable}

    with pytest.raises(ResolutionError):
        strategy.injection(injectables)

    TComponent1.discard_dependencies(
        imports=[TComponent1],
    )
    strategy.injection(injectables)
    assert TComponent1.provide()

    TProduct1.update_dependencies(
        partial_resolution=False,
    )
    with pytest.raises(ResolutionError):
        strategy.injection(injectables)
