import pytest
from dependency_injector import providers
from dependency.core.agrupation import Plugin, PluginMeta, module
from dependency.core.declaration import Component, component, instance
from dependency.core.injection import ProviderInjection, Injectable
from dependency.core.resolution import Container, ResolutionStrategy
from dependency.core.resolution.expansion import ProviderExpansion, ResolutionNode
from dependency.core.exceptions import ResolutionError


# ── Scenario A: transitive discovery ─────────────────────────────────────────

@module()
class ExpPluginA(Plugin):
    meta = PluginMeta(name="exp_plugin_a", version="0.1.0")

@component(module=ExpPluginA, provider=providers.Factory)
class ExpAService(Component):
    pass

@component(provider=providers.Factory)
class ExpAProduct(Component):
    pass

@component(
    module=ExpPluginA,
    imports=[ExpAProduct],
    provider=providers.Factory,
)
class ExpAConsumer(Component):
    pass


def test_expansion_discovers_transitive_imports() -> None:
    """Expansion follows imports and adds undeclared providers to resolved set."""
    container = Container()
    ExpPluginA.resolve_container(container)
    ExpPluginA.inject_container(container)
    ExpPluginA.resolve_providers()

    seed = set(ExpPluginA.collect_providers())
    result = ProviderExpansion(modules=[], extra=seed).expand()

    assert ExpAProduct.injection in result.resolved
    assert ExpAConsumer.injection in result.resolved


# ── Scenario B: cascade failure ──────────────────────────────────────────────

@module()
class ExpPluginB(Plugin):
    meta = PluginMeta(name="exp_plugin_b", version="0.1.0")

@component(module=ExpPluginB, provider=providers.Factory)
class ExpBRoot(Component):
    pass

@component(module=ExpPluginB)
class ExpBMissing(Component):
    pass  # no implementation

@component(
    module=ExpPluginB,
    imports=[ExpBMissing],
    provider=providers.Factory,
)
class ExpBMiddle(Component):
    pass

@component(
    module=ExpPluginB,
    imports=[ExpBMiddle],
    provider=providers.Factory,
)
class ExpBLeaf(Component):
    pass


def test_expansion_cascade_fails_dependents() -> None:
    """Failed required dep cascades: Middle fails → Leaf also fails."""
    container = Container()
    ExpPluginB.resolve_container(container)
    ExpPluginB.inject_container(container)
    ExpPluginB.resolve_providers()

    seed = set(ExpPluginB.collect_providers())
    result = ProviderExpansion(modules=[], extra=seed).expand()

    failed_providers = {f.node.provider for f in result.failures}
    assert ExpBMiddle.injection in failed_providers
    assert ExpBLeaf.injection in failed_providers
    assert ExpBRoot.injection not in failed_providers


def test_expansion_raise_if_failed_includes_chain() -> None:
    """raise_if_failed message includes the import chain."""
    container = Container()
    ExpPluginB.resolve_container(container)
    ExpPluginB.inject_container(container)
    ExpPluginB.resolve_providers()

    seed = set(ExpPluginB.collect_providers())
    result = ProviderExpansion(modules=[], extra=seed).expand()

    with pytest.raises(ResolutionError) as exc_info:
        result.raise_if_failed()

    msg = str(exc_info.value)
    assert "→" in msg or "imported via" in msg or "unresolvable" in msg


# ── Scenario C: ExpansionResult structure ────────────────────────────────────

def test_expansion_result_has_resolved_and_failures() -> None:
    """ExpansionResult always exposes both .resolved and .failures."""
    result = ProviderExpansion(modules=[], extra=set()).expand()
    assert isinstance(result.resolved, set)
    assert isinstance(result.failures, list)


def test_expansion_result_no_failures_does_not_raise() -> None:
    """raise_if_failed is a no-op when there are no failures."""
    result = ProviderExpansion(modules=[], extra=set()).expand()
    result.raise_if_failed()  # must not raise


# ── Scenario D: no-impl providers not in seed ────────────────────────────────

@module()
class ExpPluginD(Plugin):
    meta = PluginMeta(name="exp_plugin_d", version="0.1.0")

@component(module=ExpPluginD)
class ExpDInterface(Component):
    pass  # no @instance or provider → not in structural seed


def test_no_impl_provider_not_in_structural_seed() -> None:
    """collect_providers() excludes providers with no implementation."""
    container = Container()
    ExpPluginD.resolve_container(container)
    ExpPluginD.inject_container(container)
    ExpPluginD.resolve_providers()

    seed = set(ExpPluginD.collect_providers())
    assert ExpDInterface.injection not in seed


# ── Scenario E: orphan adoption ──────────────────────────────────────────────

@module()
class ExpPluginE(Plugin):
    meta = PluginMeta(name="exp_plugin_e", version="0.1.0")

@component(module=ExpPluginE, provider=providers.Factory)
class ExpEHost(Component):
    pass

@component(provider=providers.Factory)  # orphan: no module=
class ExpEOrphan(Component):
    pass

@component(
    module=ExpPluginE,
    imports=[ExpEOrphan],
    provider=providers.Factory,
)
class ExpEImporter(Component):
    pass


def test_orphan_adopted_by_importer_context() -> None:
    """Orphan providers are adopted into the importer's container during expansion."""
    container = Container()
    ExpPluginE.resolve_container(container)
    ExpPluginE.inject_container(container)
    ExpPluginE.resolve_providers()

    seed = set(ExpPluginE.collect_providers())
    result = ProviderExpansion(modules=[], extra=seed).expand()

    assert ExpEOrphan.injection in result.resolved
    assert ExpEOrphan.injection.parent is not None


# ── Scenario F: should_resolve never raises DeclarationError ─────────────────

def test_should_resolve_returns_false_for_no_impl() -> None:
    """should_resolve() returns False (no DeclarationError) for unimplemented providers."""
    injectable = Injectable(interface_cls=object)
    provider = ProviderInjection(name="unimplemented", injectable=injectable)

    assert provider.should_resolve() is False


# ── Scenario G: import_chain backtracing ─────────────────────────────────────

def test_import_chain_single_node() -> None:
    """import_chain() for a root node returns a list with just that node."""
    injectable = Injectable(interface_cls=object)
    p = ProviderInjection(name="root", injectable=injectable)
    node = ResolutionNode(provider=p, context=None)

    assert node.import_chain() == [p]


def test_import_chain_multiple_nodes() -> None:
    """import_chain() returns the full path from root to leaf."""
    injectable = Injectable(interface_cls=object)
    p1 = ProviderInjection(name="root", injectable=injectable)
    p2 = ProviderInjection(name="middle", injectable=injectable)
    p3 = ProviderInjection(name="leaf", injectable=injectable)

    root = ResolutionNode(provider=p1, context=None)
    mid = ResolutionNode(provider=p2, context=None, imported_by=root)
    leaf = ResolutionNode(provider=p3, context=None, imported_by=mid)

    assert leaf.import_chain() == [p1, p2, p3]
