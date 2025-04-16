from typing import Callable, Sequence, cast
from dependency.core.declaration.base import ABCComponent, ABCProvider, ABCDependent

class Dependent(ABCDependent):
    """Dependent Base Class
    """
    _dependency_imports: Sequence[ABCComponent]

    @classmethod
    def resolve_dependent(cls, providers: Sequence[ABCProvider]) -> list[str]:
        return [
            component.__repr__()
            for component in cls._dependency_imports
            if not any(
                issubclass(provider.provided_cls, component.base_cls)
                for provider in providers
            )
        ]

def dependent(
        imports: Sequence[type[ABCComponent]] = [],
    ) -> Callable[[type[Dependent]], type[Dependent]]:
    """Decorator for Dependent class

    Args:
        imports (Sequence[type[Component]], optional): List of components to be imported by the dependent. Defaults to [].

    Raises:
        TypeError: If the wrapped class is not a subclass of Dependent.

    Returns:
        Callable[[type[Dependent]], type[Dependent]]: Decorator function that wraps the dependent class.
    """
    # Cast due to mypy not supporting class decorators
    _imports = cast(Sequence[ABCComponent], imports)
    def wrap(cls: type[Dependent]) -> type[Dependent]:
        if not issubclass(cls, Dependent):
            raise TypeError(f"Class {cls} is not a subclass of Dependent")

        cls._dependency_imports = _imports
        return cls
    return wrap