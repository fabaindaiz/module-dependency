from abc import ABC, abstractmethod
from dependency_injector.wiring import Provide

class Component(ABC):
    def __init__(self,
            base_cls: type,
        ):
        self.base_cls = base_cls
    
    @staticmethod
    @abstractmethod
    def provide():
        pass

    @classmethod
    def inject_cls(cls):
        return cls

    def __repr__(self) -> str:
        return self.base_cls.__name__

def component(
        interface: type
    ):
    def wrap(cls) -> Component:
        class WrapComponent(Component):
            def __init__(self):
                super().__init__(
                    base_cls=interface)
            
            def provide(self,
                    service = Provide[f"{interface.__name__}.service"]
                ):
                return service
        return WrapComponent()
    return wrap