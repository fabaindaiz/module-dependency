from typing import Any, Callable, Optional
from dependency_injector.wiring import Provide
from dependency.core.declaration.base import ABCComponent, ABCProvider

class Component(ABCComponent):
    def __init__(self, base_cls: type):
        super().__init__(base_cls=base_cls)
        self.__provider: Optional[ABCProvider] = None
    
    @property
    def provider(self) -> Optional[ABCProvider]:
        return self.__provider
    
    @provider.setter
    def provider(self, provider: ABCProvider) -> None:
        if self.__provider:
            raise Exception(f"Component {self} is already provided by {self.__provider}. Attempted to set new provider: {provider}")
        self.__provider = provider
    
    @staticmethod
    def provide(service: Any = None) -> Any: # TODO: provide signature
        pass

def component(interface: type) -> Callable[[type[Component]], Component]:
    def wrap(cls: type[Component]) -> Component:
        class WrapComponent(cls): # type: ignore
            def __init__(self) -> None:
                super().__init__(base_cls=interface)
            
            @staticmethod
            def provide(self, # type: ignore
                    service: Any = Provide[f"{interface.__name__}.service"]
                ) -> Any:
                if issubclass(service.__class__, Provide):
                    raise Exception(f"Component {self} was not provided")
                return service
        return WrapComponent()
    return wrap