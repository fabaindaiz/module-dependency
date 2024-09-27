from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar
from dependency_injector.wiring import Provide

T = TypeVar("T")

class Component:
    def __init__(self, base_cls: type[T]):
        self.base_cls = base_cls
    
    @staticmethod
    def provide(service: Any = Provide[""]) -> Any:
        pass
    
    def __repr__(self) -> str:
        return self.base_cls.__name__

def component(interface: type) -> Callable[[type], Component]:
    def wrap(cls: type) -> Component:
        class WrapComponent(Component):
            def __init__(self) -> None:
                super().__init__(base_cls=interface)
            
            @staticmethod
            def provide(self, # type: ignore
                    service: Any = Provide[f"{interface.__name__}.service"]
                ) -> Any:
                return service
        return WrapComponent()
    return wrap