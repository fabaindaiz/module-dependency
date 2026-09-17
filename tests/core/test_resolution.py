import pytest
from dependency.core.injection import ProviderInjection
from dependency.core.agrupation import Plugin, PluginMeta, module
from dependency.core.declaration import Component, component, instance, providers
from dependency.core.resolution import Container, InjectionResolver, ResolutionStrategy
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
    provider=providers.Factory,
)
class TProduct1(Component):
    pass


@instance(
    imports=[
        TProduct1,
    ],
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


def test_resolution() -> None:
    container = Container.from_json("example/config.json")
    injectables: set[ProviderInjection] = set(TPlugin.collect_providers())
    assert "TInstance1" not in BOOTSTRAPED

    loader = InjectionResolver(container)
    assert "TInstance1" not in BOOTSTRAPED

    loader.resolve_providers(injectables)
    assert "TInstance1" in BOOTSTRAPED
    assert "TInstance2" in BOOTSTRAPED

    assert TComponent1.provide() is not None
    with pytest.raises(CancelInitialization):
        TComponent2.provide()


# --------------------------------------------------------------------------------------
# Bootstrap order: a provider's required imports bootstrap before it (D-053). The scenario
# is self-contained -- it resolves its own plugin -- because asserting on the order left
# behind by another test in this file would make it depend on test execution order.
# --------------------------------------------------------------------------------------

ORDER: list[str] = []


@module()
class OrderPlugin(Plugin):
    meta = PluginMeta(name="order_plugin", version="0.1.0")


@component(module=OrderPlugin)
class OrderFirst(Component):
    pass


@component(module=OrderPlugin)
class OrderSecond(Component):
    pass


@component(module=OrderPlugin)
class OrderThird(Component):
    pass


@instance(bootstrap=True)
class OrderFirstImpl(OrderFirst):
    def __init__(self) -> None:
        ORDER.append("first")


@instance(imports=[OrderFirst], bootstrap=True)
class OrderSecondImpl(OrderSecond):
    def __init__(self) -> None:
        ORDER.append("second")


@instance(imports=[OrderSecond], bootstrap=True)
class OrderThirdImpl(OrderThird):
    def __init__(self) -> None:
        ORDER.append("third")


def test_bootstrap_follows_dependency_order() -> None:
    ORDER.clear()
    container = Container.from_dict({})
    resolver = InjectionResolver(container)
    resolver.resolve_modules(modules=[OrderPlugin])

    resolver.resolve_providers(providers=set(OrderPlugin.collect_providers()))

    assert ORDER == ["first", "second", "third"]


def test_injection_returns_the_order_it_resolved_in() -> None:
    strategy = ResolutionStrategy()
    providers = strategy.expand(set(OrderPlugin.collect_providers()))

    order = strategy.injection(providers=providers)

    names = [provider.name for provider in order]
    assert names.index("OrderFirst") < names.index("OrderSecond") < names.index("OrderThird")
