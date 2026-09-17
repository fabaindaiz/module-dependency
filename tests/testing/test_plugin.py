"""The pytest plugin, and the measurement of what it cannot yet isolate.

The strict xfail below is the repository's answer to the roadmap's open question — *is the
declaration registry resettable at all?* It is not, today, and the test says so with a
number instead of an opinion. When declaration state stops being process-global the xfail
becomes an xpass, `strict=True` turns that into a failure, and whoever lands that change is
forced to delete the marker. That is the definition of done, expressed as a test.
"""

import pytest
from dependency.core.agrupation import Plugin, PluginMeta, module
from dependency.core.declaration import Component, component, instance
from dependency.core.resolution import Container, ResolutionStrategy
from dependency.testing.plugin import declaration_state


@module()
class PlugPlugin(Plugin):
    meta = PluginMeta(name="plugin_fixture_plugin", version="0.1.0")


@component(
    module=PlugPlugin,
)
class PlugService(Component):
    pass


@instance()
class PlugServiceImpl(PlugService):
    pass


def test_dependency_container_is_a_fresh_container(
    dependency_container: Container,
) -> None:
    assert isinstance(dependency_container, Container)
    assert dependency_container.config() == {}


def test_dependency_container_is_not_shared_between_tests(
    dependency_container: Container,
) -> None:
    dependency_container.config.from_dict({"touched": True})

    assert Container.from_dict({}).config() == {}


def test_declaration_state_reports_what_lives_on_the_class() -> None:
    state = declaration_state(PlugService)

    assert set(state) == {
        "PlugService.is_resolved",
        "PlugService.parent",
        "PlugService.implementation",
        "PlugService.provider",
    }
    assert state["PlugService.implementation"] is PlugServiceImpl


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Declaration state is process-global with no teardown: resolving mutates "
        "is_resolved on the class and nothing resets it. Closing that is the point of "
        "the 2.0.0 redesign; when it lands this xpasses and strict=True fails the build."
    ),
)
def test_resolving_leaves_no_trace_on_the_declared_classes() -> None:
    before = declaration_state(PlugService)

    strategy = ResolutionStrategy()
    container = Container.from_dict({})
    PlugPlugin.resolve_container(container)
    strategy.injection(providers=strategy.expand(set(PlugPlugin.collect_providers())))

    assert declaration_state(PlugService) == before
