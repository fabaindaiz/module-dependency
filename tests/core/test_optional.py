import pytest
from dependency_injector import providers
from dependency.core.agrupation import Plugin, PluginMeta, module
from dependency.core.declaration import Component, component, instance
from dependency.core.resolution import Container, ResolutionStrategy
from dependency.core.exceptions import ResolutionError


# ── Scenario A: optional dep WITH implementation ──────────────────────────────

@module()
class PluginA(Plugin):
    meta = PluginMeta(name="opt_plugin_a", version="0.1.0")

@component(module=PluginA, provider=providers.Factory)
class AInterface(Component):
    pass

@component(module=PluginA, provider=providers.Factory)
class AOptDep(Component):
    pass

@component(
    module=PluginA,
    optional=[AOptDep],
    provider=providers.Factory,
)
class AConsumer(Component):
    pass


def test_optional_with_impl_both_resolve() -> None:
    """Optional dep that has an implementation: both consumer and dep resolve."""
    strategy = ResolutionStrategy()
    container = Container()

    PluginA.resolve_container(container)
    PluginA.inject_container(container)
    PluginA.resolve_providers()

    injectables = set(PluginA.collect_providers())
    expanded = strategy.expand(injectables)

    assert AConsumer.injection in expanded
    assert AOptDep.injection in expanded


# ── Scenario B: optional dep WITHOUT implementation ───────────────────────────

@module()
class PluginB(Plugin):
    meta = PluginMeta(name="opt_plugin_b", version="0.1.0")

@component(module=PluginB, provider=providers.Factory)
class BInterface(Component):
    pass

@component(module=PluginB)
class BMissingDep(Component):
    pass  # no provider/instance → no implementation

@component(
    module=PluginB,
    optional=[BMissingDep],
    provider=providers.Factory,
)
class BConsumer(Component):
    pass


def test_optional_missing_impl_consumer_still_resolves() -> None:
    """Optional dep with no implementation: consumer still enters resolved set."""
    strategy = ResolutionStrategy()
    container = Container()

    PluginB.resolve_container(container)
    PluginB.inject_container(container)
    PluginB.resolve_providers()

    injectables = set(PluginB.collect_providers())
    expanded = strategy.expand(injectables)

    assert BConsumer.injection in expanded


def test_optional_missing_impl_dep_not_in_resolved() -> None:
    """Optional dep with no implementation is not in the resolved set."""
    strategy = ResolutionStrategy()
    container = Container()

    PluginB.resolve_container(container)
    PluginB.inject_container(container)
    PluginB.resolve_providers()

    injectables = set(PluginB.collect_providers())
    expanded = strategy.expand(injectables)

    assert BMissingDep.injection not in expanded


def test_optional_missing_impl_no_cascade() -> None:
    """Optional import failure does not cascade to the consumer."""
    strategy = ResolutionStrategy()
    container = Container()

    PluginB.resolve_container(container)
    PluginB.inject_container(container)
    PluginB.resolve_providers()

    injectables = set(PluginB.collect_providers())
    # Must not raise ResolutionError
    expanded = strategy.expand(injectables)
    assert BConsumer.injection in expanded


def test_optional_missing_impl_injection_succeeds() -> None:
    """Consumer with absent optional dep satisfies resolve_if_posible."""
    strategy = ResolutionStrategy()
    container = Container()

    PluginB.resolve_container(container)
    PluginB.inject_container(container)
    PluginB.resolve_providers()

    injectables = set(PluginB.collect_providers())
    expanded = strategy.expand(injectables)
    strategy.injection(expanded)

    assert BConsumer.injection.is_resolved


# ── Scenario C: required dep WITHOUT implementation raises error ───────────────

@module()
class PluginC(Plugin):
    meta = PluginMeta(name="opt_plugin_c", version="0.1.0")

@component(module=PluginC, provider=providers.Factory)
class CInterface(Component):
    pass

@component(module=PluginC)
class CMissingDep(Component):
    pass  # no implementation

@component(
    module=PluginC,
    imports=[CMissingDep],  # required, not optional
    provider=providers.Factory,
)
class CConsumer(Component):
    pass


def test_required_missing_impl_raises() -> None:
    """Required dep with no implementation raises ResolutionError."""
    strategy = ResolutionStrategy()
    container = Container()

    PluginC.resolve_container(container)
    PluginC.inject_container(container)
    PluginC.resolve_providers()

    injectables = set(PluginC.collect_providers())
    with pytest.raises(ResolutionError):
        strategy.expand(injectables)


# ── Scenario D: move required → optional at runtime ──────────────────────────

@module()
class PluginD(Plugin):
    meta = PluginMeta(name="opt_plugin_d", version="0.1.0")

@component(module=PluginD, provider=providers.Factory)
class DInterface(Component):
    pass

@component(module=PluginD)
class DMissingDep(Component):
    pass  # no implementation

@component(
    module=PluginD,
    imports=[DMissingDep],
    provider=providers.Factory,
)
class DConsumer(Component):
    pass


def test_move_required_to_optional_resolves() -> None:
    """Moving a dep from required to optional allows resolution to succeed."""
    strategy = ResolutionStrategy()
    container = Container()

    PluginD.resolve_container(container)
    PluginD.inject_container(container)
    PluginD.resolve_providers()

    injectables = set(PluginD.collect_providers())
    with pytest.raises(ResolutionError):
        strategy.expand(injectables)

    DConsumer.discard_dependencies(imports=[DMissingDep])
    DConsumer.update_dependencies(optional=[DMissingDep])

    expanded = strategy.expand(injectables)
    strategy.injection(expanded)
    assert DConsumer.injection.is_resolved


# ── Scenario E: decorator sets optional_imports, not imports ──────────────────

def test_optional_decorator_sets_optional_imports() -> None:
    """@component(optional=[X]) adds X to optional_imports, not imports."""
    assert BMissingDep.injection not in BConsumer.injection.imports
    assert BMissingDep.injection in BConsumer.injection.optional_imports
