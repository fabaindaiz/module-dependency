import pytest
from dependency_injector import providers
from dependency.core.agrupation import Plugin, PluginMeta, module
from dependency.core.declaration import Component, component, instance
from dependency.core.resolution import Container, ResolutionStrategy
from dependency.core.exceptions import ResolutionError

@module()
class TPlugin(Plugin):
    meta = PluginMeta(name="test_plugin", version="0.1.0")

@component(module=TPlugin)
class TComponent1(Component):
    pass

@component(
    imports=[TComponent1],
    module=TPlugin,
    strict_resolution=False,
)
class TComponent2(Component):
    pass

@component(
    optional=[TComponent2],
    provider=providers.Factory,
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


def test_circular_self_import_raises_resolution_error() -> None:
    """TInstance1 imports TComponent1, which TInstance1 itself implements.

    This creates a self-import cycle: the provider depends on its own interface,
    so injection can never settle. Breaking the self-import unblocks resolution.
    """
    strategy: ResolutionStrategy = ResolutionStrategy()
    container = Container()

    TPlugin.resolve_container(container)
    TPlugin.inject_container(container)
    TPlugin.resolve_providers()
    injectables = set(TPlugin.collect_providers())
    assert injectables == {TComponent1.injection}

    injectables = strategy.expand(injectables)
    assert injectables == {TComponent1.injection, TProduct1.injection}

    with pytest.raises(ResolutionError):
        strategy.injection(injectables)

    TComponent1.discard_dependencies(imports=[TComponent1])
    strategy.injection(injectables)
    assert TComponent1.provide()
