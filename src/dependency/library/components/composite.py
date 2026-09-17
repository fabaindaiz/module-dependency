from abc import abstractmethod
from typing import Any, Generic, TypeVar
from dependency.core import Component
from dependency.library.patterns.composite import Composite

CHILD = TypeVar("CHILD")


class CompositeComponent(Component, Generic[CHILD]):
    """Contract for a component that fans an operation out over its children.

    Not decorated: the application declares its own component from this base, so the
    module, the provider and the child type stay where the domain is.

    Parameterise it with the type being grouped::

        @component(module=SensorsPlugin)
        class SensorGroup(CompositeComponent[SensorReader]):
            pass

    The contract deliberately says nothing about *what* fanning out means — a group of
    readers collects, a group of sinks broadcasts. That belongs to the implementation.
    """

    @abstractmethod
    def add(self, child: CHILD) -> None:
        """Add a child to the group."""

    @abstractmethod
    def remove(self, child: CHILD) -> None:
        """Remove a child from the group. Raises ValueError if absent."""

    @property
    @abstractmethod
    def children(self) -> list[CHILD]:
        """The current children, in insertion order."""


class CompositeMixin(Generic[CHILD]):
    """Implementation body for a `CompositeComponent`.

    Supplies membership over a `Composite`. Mix it in ahead of the component so its
    `__init__` runs::

        @instance(provider=providers.Singleton)
        class SensorGroupAll(CompositeMixin[SensorReader], SensorGroup):
            pass
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._composite: Composite[CHILD] = Composite()

    def add(self, child: CHILD) -> None:
        self._composite.add(child)

    def remove(self, child: CHILD) -> None:
        self._composite.remove(child)

    @property
    def children(self) -> list[CHILD]:
        return self._composite.children
