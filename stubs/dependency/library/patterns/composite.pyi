from typing import Generic, TypeVar

T = TypeVar('T')

class Composite(Generic[T]):
    """Ordered membership of child objects.

    A primitive: it knows nothing about the framework. Wrap it with
    `dependency.library.components.CompositeMixin` to expose it as a component.
    """
    def __init__(self) -> None: ...
    def add(self, component: T) -> None:
        """Append a child."""
    def remove(self, component: T) -> None:
        """Remove a child.

        Raises:
            ValueError: If the child is not present.
        """
    @property
    def children(self) -> list[T]:
        """The current children, in insertion order."""
