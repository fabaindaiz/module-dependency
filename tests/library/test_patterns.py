import asyncio
import pytest
from dependency.library.patterns.composite import Composite
from dependency.library.patterns.observer import (
    EventContext,
    EventPublisher,
    EventSubscriber,
)
from dependency.library.patterns.state import StateHolder


# ── Composite ────────────────────────────────────────────────────────────────


def test_composite_preserves_insertion_order() -> None:
    composite: Composite[str] = Composite()
    composite.add("a")
    composite.add("b")
    composite.add("c")
    assert composite.children == ["a", "b", "c"]


def test_composite_remove() -> None:
    composite: Composite[str] = Composite()
    composite.add("a")
    composite.add("b")
    composite.remove("a")
    assert composite.children == ["b"]


def test_composite_remove_absent_raises() -> None:
    composite: Composite[str] = Composite()
    with pytest.raises(ValueError):
        composite.remove("missing")


def test_composite_instances_do_not_share_state() -> None:
    """A mutable default on the class would make every Composite the same list."""
    first: Composite[str] = Composite()
    second: Composite[str] = Composite()
    first.add("only-in-first")
    assert second.children == []


# ── StateHolder ──────────────────────────────────────────────────────────────


def test_state_holder_starts_at_initial_state() -> None:
    holder: StateHolder[str] = StateHolder("idle")
    assert holder.state == "idle"


def test_state_holder_transitions() -> None:
    holder: StateHolder[str] = StateHolder("idle")
    holder.state = "running"
    assert holder.state == "running"


def test_state_holder_instances_are_independent() -> None:
    first: StateHolder[str] = StateHolder("a")
    second: StateHolder[str] = StateHolder("b")
    first.state = "changed"
    assert second.state == "b"


# ── EventPublisher ───────────────────────────────────────────────────────────


class PatternEventA(EventContext):
    def __init__(self, payload: str) -> None:
        self.payload = payload


class PatternEventB(EventContext):
    pass


def test_publisher_delivers_only_to_matching_context_type() -> None:
    publisher = EventPublisher()
    seen: list[str] = []

    @publisher.subscribe(EventSubscriber)
    async def on_a(context: PatternEventA) -> None:
        seen.append(context.payload)

    asyncio.run(publisher.update(PatternEventA("hit")))
    asyncio.run(publisher.update(PatternEventB()))

    assert seen == ["hit"]


def test_publisher_delivers_to_every_subscriber() -> None:
    publisher = EventPublisher()
    seen: list[str] = []

    @publisher.subscribe(EventSubscriber)
    async def first(context: PatternEventA) -> None:
        seen.append("first")

    @publisher.subscribe(EventSubscriber)
    async def second(context: PatternEventA) -> None:
        seen.append("second")

    asyncio.run(publisher.update(PatternEventA("x")))
    assert sorted(seen) == ["first", "second"]


def test_publish_with_no_subscribers_is_a_noop() -> None:
    publisher = EventPublisher()
    asyncio.run(publisher.update(PatternEventA("nobody listening")))


def test_subscribe_rejects_a_callback_with_no_parameters() -> None:
    publisher = EventPublisher()
    with pytest.raises(TypeError):

        @publisher.subscribe(EventSubscriber)
        async def no_params() -> None:  # type: ignore[misc]
            pass


def test_subscribe_rejects_a_callback_whose_parameter_is_not_an_event() -> None:
    publisher = EventPublisher()
    with pytest.raises(TypeError):

        @publisher.subscribe(EventSubscriber)
        async def wrong_type(context: str) -> None:  # type: ignore[arg-type]
            pass


def test_subscribe_rejects_a_callback_annotated_only_with_return() -> None:
    publisher = EventPublisher()
    with pytest.raises(TypeError):

        @publisher.subscribe(EventSubscriber)
        async def only_return() -> None:  # type: ignore[misc]
            pass
