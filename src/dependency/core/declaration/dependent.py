from typing import Any, Callable, cast
from dependency_injector.wiring import Provide
from dependency.core.declaration.base import ABCDependent
from dependency.core.declaration.component import Component

class Dependent(ABCDependent):
    pass

def dependent(
        imports: list[type[Component]] = [],
    ) -> Callable[[type], Dependent]:
    def wrap(cls: type) -> type[Dependent]:
        _imports = cast(list[Component], imports)
        class WrapComponent(cls, Dependent): # type: ignore
            imports = _imports
        return WrapComponent
    return wrap