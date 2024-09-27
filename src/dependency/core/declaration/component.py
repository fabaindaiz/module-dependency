from abc import ABC
from typing import Any, Callable
from dependency_injector.wiring import Provide

class Component(ABC):
    def __init__(self, base_cls: type):
        self.base_cls = base_cls
    
    @staticmethod
    def provide(service: Any = Provide[""]) -> Any:
        pass
    
    def __repr__(self) -> str:
        return self.base_cls.__name__

def component(interface: type) -> Callable[[type[Component]], Component]:
    def wrap(cls: type[Component]) -> Component:
        class WrapComponent(cls): # type: ignore
            def __init__(self) -> None:
                super().__init__(base_cls=interface)
            
            @staticmethod
            def provide(self, # type: ignore
                    service: Any = Provide[f"{interface.__name__}.service"]
                ) -> Any:
                return service
        return WrapComponent()
    return wrap