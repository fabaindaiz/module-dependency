"""The library ships contracts, not declarations (D-030).

These tests assert both halves: that a contract carries no declaration of its own, and
that two applications declaring from the same contract stay independent.
"""

import asyncio
from enum import Enum
import pytest
from dependency.core import (
    Component,
    Container,
    Entrypoint,
    Plugin,
    PluginMeta,
    component,
    instance,
    module,
    providers,
)
from dependency.library.components import (
    CompositeComponent,
    CompositeMixin,
    EventPublisherMixin,
    ObserverComponent,
    StateComponent,
    StateMixin,
)
from dependency.library.patterns.observer import EventContext, EventSubscriber


# ── the contracts declare nothing ────────────────────────────────────────────


@pytest.mark.parametrize(
    "contract", [ObserverComponent, CompositeComponent, StateComponent]
)
def test_contract_is_not_declared(contract: type[Component]) -> None:
    """A library contract must not carry an injection node of its own.

    If it did, every application declaring from it would share one global provider and
    the last import would decide the implementation. See D-030.
    """
    assert not hasattr(contract, "injection")
    assert not hasattr(contract, "injectable")


# ── Observer ─────────────────────────────────────────────────────────────────


class LibEvent(EventContext):
    def __init__(self, payload: str) -> None:
        self.payload = payload


@module()
class LibObsPluginA(Plugin):
    meta = PluginMeta(name="lib_obs_a", version="0.1.0")


@module()
class LibObsPluginB(Plugin):
    meta = PluginMeta(name="lib_obs_b", version="0.1.0")


@component(module=LibObsPluginA)
class ObserverA(ObserverComponent[LibEvent]):
    pass


@component(module=LibObsPluginB)
class ObserverB(ObserverComponent[LibEvent]):
    pass


@instance(provider=providers.Singleton)
class ObserverAImpl(EventPublisherMixin[LibEvent], ObserverA):
    def update(self, context: LibEvent) -> None:
        asyncio.run(self.publish(context))


@instance(provider=providers.Singleton)
class ObserverBImpl(EventPublisherMixin[LibEvent], ObserverB):
    def update(self, context: LibEvent) -> None:
        asyncio.run(self.publish(context))


def test_two_domains_from_one_contract_get_independent_nodes() -> None:
    """The measurement behind D-030: no shared global provider, no reassignment."""
    assert ObserverA.injection is not ObserverB.injection
    assert ObserverA.reference() == "LibObsPluginA.ObserverA"
    assert ObserverB.reference() == "LibObsPluginB.ObserverB"
    assert ObserverA.injectable.implementation is ObserverAImpl
    assert ObserverB.injectable.implementation is ObserverBImpl


def test_observer_mixin_publishes_to_subscribers() -> None:
    container = Container.from_dict({"config": True})

    class App(Entrypoint):
        def __init__(self) -> None:
            super().__init__(container, [LibObsPluginA, LibObsPluginB])
            super().initialize()

    App()
    observer = ObserverA.provide()
    seen: list[str] = []

    @observer.subscribe(EventSubscriber)
    async def listener(context: LibEvent) -> None:
        seen.append(context.payload)

    observer.update(LibEvent("delivered"))
    assert seen == ["delivered"]


def test_observers_do_not_share_subscribers() -> None:
    seen_a: list[str] = []

    @ObserverA.provide().subscribe(EventSubscriber)
    async def only_a(context: LibEvent) -> None:
        seen_a.append(context.payload)

    ObserverB.provide().update(LibEvent("to-b"))
    assert "to-b" not in seen_a


# ── Composite ────────────────────────────────────────────────────────────────


@module()
class LibCompositePlugin(Plugin):
    meta = PluginMeta(name="lib_composite", version="0.1.0")


@component(module=LibCompositePlugin)
class StringGroup(CompositeComponent[str]):
    pass


@instance(provider=providers.Singleton)
class StringGroupImpl(CompositeMixin[str], StringGroup):
    pass


def test_composite_component_membership() -> None:
    container = Container.from_dict({"config": True})

    class App(Entrypoint):
        def __init__(self) -> None:
            super().__init__(container, [LibCompositePlugin])
            super().initialize()

    App()
    group = StringGroup.provide()
    group.add("first")
    group.add("second")
    assert group.children == ["first", "second"]
    group.remove("first")
    assert group.children == ["second"]


# ── State ────────────────────────────────────────────────────────────────────


class Mode(Enum):
    STARTING = "starting"
    RUNNING = "running"


@module()
class LibStatePlugin(Plugin):
    meta = PluginMeta(name="lib_state", version="0.1.0")


@component(module=LibStatePlugin)
class ModeState(StateComponent[Mode]):
    pass


TRANSITIONS: list[Mode] = []


@instance(provider=providers.Singleton)
class ModeStateImpl(StateMixin[Mode], ModeState):
    def initial_state(self) -> Mode:
        return Mode.STARTING

    def transition(self, state: Mode) -> None:
        """Overriding transition is the point of having it: a move can be observed."""
        TRANSITIONS.append(state)
        super().transition(state)


def test_state_component_starts_at_initial_state_and_announces_moves() -> None:
    container = Container.from_dict({"config": True})

    class App(Entrypoint):
        def __init__(self) -> None:
            super().__init__(container, [LibStatePlugin])
            super().initialize()

    App()
    state = ModeState.provide()
    assert state.state is Mode.STARTING

    state.transition(Mode.RUNNING)
    assert state.state is Mode.RUNNING
    assert TRANSITIONS == [Mode.RUNNING]
