"""Contract test against `dependency-injector`'s private API.

`injection/wiring.py` builds `LazyProvide`, `LazyProvider` and `LazyClosing` on top of
`_Marker` — an underscore-prefixed class. An upstream refactor would break every installed
user of this package, and without this file we would hear about it from an issue report
rather than from CI.

The dependency is pinned `>=4.48.2,<5`, which buys time but detects nothing.
"""

import inspect
import pytest
from dependency_injector import providers
from dependency_injector.wiring import Closing, Provide, Provider, _Marker, inject
from dependency.core import (
    Component,
    Container,
    Entrypoint,
    Plugin,
    PluginMeta,
    component,
    instance,
    module,
)
from dependency.core.injection import LazyClosing, LazyProvide, LazyProvider
from dependency.core.injection.wiring import LazyWiring


# ── shape: the names we build on still exist and are still classes ───────────


@pytest.mark.parametrize("marker", [_Marker, Provide, Provider, Closing])
def test_upstream_marker_names_exist(marker: type) -> None:
    assert inspect.isclass(marker)


@pytest.mark.parametrize("lazy", [LazyProvide, LazyProvider, LazyClosing])
def test_lazy_markers_subclass_both_sides(lazy: type) -> None:
    """Each Lazy marker is a LazyWiring *and* the upstream marker it mirrors.

    Losing either half breaks injection silently rather than loudly: the marker would
    still be a valid default value, and `@inject` would simply not replace it.
    """
    assert issubclass(lazy, LazyWiring)
    assert issubclass(lazy, _Marker)


def test_marker_still_supports_class_getitem() -> None:
    """`LazyProvide[X]` and `LazyProvide(X)` must stay equivalent.

    Both spellings appear in the documentation and in the example.
    """
    assert hasattr(_Marker, "__class_getitem__")
    subscript = LazyProvide["some.reference"]
    call = LazyProvide("some.reference")
    assert isinstance(subscript, LazyProvide)
    assert isinstance(call, LazyProvide)


def test_marker_accepts_the_arguments_lazywiring_passes() -> None:
    """LazyWiring.__init__ calls _Marker with (provider, modifier=...)."""
    signature = inspect.signature(_Marker.__init__)
    assert "modifier" in signature.parameters


def test_lazywiring_defers_resolution_to_call_time() -> None:
    """The whole reason the Lazy markers exist.

    The bare markers resolve their reference when the module is imported, before the
    injection tree exists. LazyWiring stores a callable and resolves on access.
    """
    calls: list[int] = []

    def reference() -> str:
        calls.append(1)
        return "resolved.late"

    marker = LazyProvide(reference)
    assert calls == [], "constructing the marker must not resolve the reference"
    assert marker.provider == "resolved.late"
    assert calls == [1]


def test_lazywiring_accepts_a_wiringmixin_class() -> None:
    """Passing a Component class uses its .reference classmethod, not its value."""
    marker = LazyProvide(ContractService)
    assert marker.provider == ContractService.reference()


# ── behaviour: a wired injection actually resolves ───────────────────────────


@module()
class ContractPlugin(Plugin):
    meta = PluginMeta(name="wiring_contract", version="0.1.0")


@component(module=ContractPlugin)
class ContractService(Component):
    def value(self) -> str: ...


@instance(provider=providers.Singleton)
class ContractServiceImpl(ContractService):
    def value(self) -> str:
        return "injected"


@component(module=ContractPlugin, imports=[ContractService])
class ContractConsumer(Component):
    def via_method(self) -> str: ...


@instance(provider=providers.Singleton)
class ContractConsumerImpl(ContractConsumer):
    @inject
    def via_method(
        self, service: ContractService = LazyProvide[ContractService.reference]
    ) -> str:
        return service.value()


@inject
def via_module_function(
    service: ContractService = LazyProvide[ContractService.reference],
) -> object:
    return service


@pytest.fixture(scope="module", autouse=True)
def wired() -> None:
    class App(Entrypoint):
        def __init__(self) -> None:
            super().__init__(Container.from_dict({"config": True}), [ContractPlugin])
            super().initialize()

    App()


def test_a_wired_injection_resolves_end_to_end() -> None:
    """Shape is not enough: the upstream marker has to still be honoured by @inject.

    If this fails while the shape tests pass, the upstream wiring machinery changed
    behaviour rather than its API — the harder case to notice.
    """
    assert ContractConsumer.provide().via_method() == "injected"


def test_inject_does_not_reach_module_level_functions() -> None:
    """A measured limit of this framework, pinned so it is not rediscovered.

    `ResolutionStrategy.wiring` calls `container.wire(modules=injectable.modules_cls)`,
    and `modules_cls` holds the component *classes*, not the modules they live in. So
    dependency-injector wires the members of those classes and nothing else.

    The failure mode is the dangerous kind: no error is raised, the marker object is
    passed through as the argument, and the first sign is an AttributeError somewhere
    else. Put `@inject` on a component method. See D-037.
    """
    result = via_module_function()
    assert isinstance(result, LazyProvide), (
        "module-level @inject appears to work now — if this is intentional, "
        "update D-037 and the wiring notes in docs/architecture.md"
    )
    assert not isinstance(result, ContractService)
