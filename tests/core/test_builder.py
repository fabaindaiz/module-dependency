"""Characterisation: a graph built from specs matches the one the decorators mutated.

This is a **characterisation test** (`tests/CLAUDE.md`, the fourth row of the test-first
exceptions): it records what the current implementation does, not what it should do. It
exists so the class-attribute path can be deleted against evidence instead of hope, and it
is meant to die with that path.

The one thing here that is a specification rather than a record is
`test_two_implementations_for_one_component_are_rejected`. That behaviour does not exist in
the old path at all — today the last `@instance` imported wins, silently (D-030).
"""
import pytest
from dependency_injector import providers
from dependency.core.agrupation import Plugin, PluginMeta, Module, module
from dependency.core.declaration import Component, component, instance
from dependency.core.injection.builder import GraphBuilder
from dependency.core.exceptions import DeclarationError

@module()
class BuildPlugin(Plugin):
    meta = PluginMeta(name="build_plugin", version="0.1.0")

@module(
    module=BuildPlugin,
)
class BuildChild(Module):
    pass

@component(
    module=BuildPlugin,
)
class BuildDependency(Component):
    pass

@instance()
class BuildDependencyImpl(BuildDependency):
    pass

@component(
    module=BuildPlugin,
)
class BuildAbsent(Component):
    """Declared and never implemented, which is legal and must stay legal."""

@component(
    module=BuildChild,
    imports=[BuildDependency],
    optional=[BuildAbsent],
    strict_resolution=False,
)
class BuildService(Component):
    pass

@instance(
    provider=providers.Factory,
)
class BuildServiceImpl(BuildService):
    pass

@module()
class BuildAmbiguousPlugin(Plugin):
    meta = PluginMeta(name="build_ambiguous_plugin", version="0.1.0")

@component(
    module=BuildAmbiguousPlugin,
)
class BuildAmbiguous(Component):
    pass

@instance()
class BuildAmbiguousFirst(BuildAmbiguous):
    pass

@instance()
class BuildAmbiguousSecond(BuildAmbiguous):
    pass

def test_container_tree_matches_the_declared_one() -> None:
    graph = GraphBuilder([BuildPlugin]).build()

    assert graph.container_for(BuildPlugin).is_root == BuildPlugin.injection.is_root
    assert graph.container_for(BuildChild).parent is graph.container_for(BuildPlugin)
    assert graph.container_for(BuildChild).reference == BuildChild.injection.reference

def test_provider_nodes_match_the_declared_ones() -> None:
    graph = GraphBuilder([BuildPlugin]).build()

    for component_cls in (BuildDependency, BuildAbsent, BuildService):
        built = graph.node(component_cls)
        legacy = component_cls.injection

        assert built.name == legacy.name
        assert built.strict_resolution == legacy.strict_resolution
        assert {i.name for i in built.imports} == {i.name for i in legacy.imports}
        assert {i.name for i in built.optional_imports} == {i.name for i in legacy.optional_imports}
        assert built.injectable.implementation is legacy.injectable.implementation

def test_the_built_graph_shares_nothing_with_the_declared_one() -> None:
    graph = GraphBuilder([BuildPlugin]).build()

    assert graph.node(BuildService) is not BuildService.injection
    assert graph.node(BuildService).injectable is not BuildService.injectable
    assert not graph.node(BuildService).is_resolved

def test_two_builds_share_no_provider() -> None:
    """The leak that "one Container per test" never covered: the singleton's own cache."""
    first = GraphBuilder([BuildPlugin]).build()
    second = GraphBuilder([BuildPlugin]).build()

    assert first.node(BuildService).provider is not second.node(BuildService).provider
    assert first.node(BuildService).provider is not BuildService.injection.provider

def test_binding_is_scoped_to_what_the_build_can_reach() -> None:
    graph = GraphBuilder([BuildPlugin]).build()

    with pytest.raises(DeclarationError):
        graph.node(BuildAmbiguous)

def test_an_import_pulls_in_a_component_from_outside_the_roots() -> None:
    graph = GraphBuilder([BuildChild]).build()

    assert graph.node(BuildDependency).parent is graph.container_for(BuildPlugin)

def test_two_implementations_for_one_component_are_rejected() -> None:
    """This is the specification, not a characterisation: today the last import wins."""
    with pytest.raises(DeclarationError) as failure:
        GraphBuilder([BuildAmbiguousPlugin]).build()

    message = str(failure.value)
    assert "BuildAmbiguous" in message
    assert "BuildAmbiguousFirst" in message
    assert "BuildAmbiguousSecond" in message

def test_the_old_path_still_binds_the_last_instance_imported() -> None:
    """The behaviour being replaced, recorded so the change is visible in the diff."""
    assert BuildAmbiguous.injectable.implementation is BuildAmbiguousSecond
