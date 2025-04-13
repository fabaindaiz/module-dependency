from typing import Any, Callable, cast
from dependency.core.declaration.base import ABCDependent
from dependency.core.declaration.component import Component

class Dependent(ABCDependent):
    imports: list[Component]

def dependent(
        imports: list[type[Component]] = [],
    ) -> Callable[[type], type[Dependent]]:
    def wrap(cls: type) -> type[Dependent]:
        _imports = cast(list[Component], imports)
        class WrapComponent(cls): # type: ignore
            imports = _imports
        return WrapComponent
    return wrap