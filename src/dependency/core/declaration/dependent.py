from typing import Callable, cast
from dependency.core.declaration.base import ABCDependent
from dependency.core.declaration.component import Component

class Dependent(ABCDependent):
    """Dependent Base Class
    """
    _imports: list[Component]

def dependent(
        imports: list[type[Component]] = [],
    ) -> Callable[[type[Dependent]], type[Dependent]]:
    """Decorator for Dependent class

    Args:
        imports (list[type[Component]], optional): List of components to be imported by the dependent. Defaults to [].

    Raises:
        TypeError: If the wrapped class is not a subclass of Dependent.

    Returns:
        Callable[[type[Dependent]], type[Dependent]]: Decorator function that wraps the dependent class.
    """
    # Cast due to mypy not supporting class decorators
    _imports = cast(list[Component], imports)
    def wrap(cls: type[Dependent]) -> type[Dependent]:
        if not issubclass(cls, Dependent):
            raise TypeError(f"Class {cls} is not a subclass of Dependent")

        cls._imports = _imports
        return cls
    return wrap