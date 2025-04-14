from typing import Any, Callable, cast
from dependency.core.declaration.base import ABCDependent
from dependency.core.declaration.component import Component

class Dependent(ABCDependent):
    imports: list[Component]

    def __repr__(self) -> str:
        return self.__name__

def dependent(
        imports: list[type[Component]] = [],
    ) -> Callable[[type[Dependent]], type[Dependent]]:
    def wrap(cls: type[Dependent]) -> type[Dependent]:
        _imports = cast(list[Component], imports)
        cls.imports = _imports
        return cls
    return wrap