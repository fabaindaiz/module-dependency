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
    strategy: ResolutionStrategy = ResolutionStrategy()
    container = Container()

    TPlugin.resolve_container(container)
    injectables = set(TPlugin.collect_providers())
    assert injectables == {TComponent1.injection}

    # TComponent2 is a required import of TProduct1 with no implementation → fails
    with pytest.raises(ResolutionError):
        strategy.expand(injectables)

    # Move TComponent2 to optional: TProduct1 can now resolve without it
    TProduct1.discard_dependencies(imports=[TComponent2])
    TProduct1.update_dependencies(optional=[TComponent2])

    expanded = strategy.expand(injectables)
    strategy.injection(expanded)

    assert TComponent1.injection.is_resolved
    assert TProduct1.injection.is_resolved
