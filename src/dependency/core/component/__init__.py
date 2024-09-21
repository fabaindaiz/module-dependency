from dependency_injector import providers
from typing import TypeVar

class Component:
    T = TypeVar('T')
    def __init__(self,
            cls: type
        ):
        self.component_cls = cls

        @classmethod
        def get_class(cls):
            return cls
    
    def __repr__(self) -> str:
        return self.component_cls.__name__
    
    @staticmethod
    def wrap(cls: type[T])
        class WrapComponent(Component):
            

            def __call__(self,
                    service: Type)

class Provider:
    def __init__(self,
            cls: type,
            component: Component,
            imports: list[Component],
            provider: providers.Provider
        ):
        self.cls = cls
        self.
    
    @staticmethod
    def wrap(cls):
        class WarpProvider(Provider):
            def __init__(self,
                    component: Component
                ):
                