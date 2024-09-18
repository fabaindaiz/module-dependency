from dependency_injector import containers, providers
from dependency_injector.wiring import Provide
from typing import TypeVar

def component():
    T = TypeVar('T')
    def wrap(cls: T) -> T:
        class Component:
            _name = cls.__name__

            def __call__(self,
                    service = Provide[f"{cls.__name__}._provider"]):
                return service
            
            @classmethod
            def wire(cls, container: containers.Container):
                return container.wire(modules=[cls])
        
        return Component()
    return wrap

def provider(
        component,
        imports: list = [],
        provider = providers.Singleton
    ):
    def wrap(cls):
        class Container(containers.DeclarativeContainer):
            _config = providers.Configuration()
            _provider = provider(cls, _config)
        class Provider:
            _name = cls.__name__
            _container = Container
            _component = component
            _imports = imports
        return Provider()
    return wrap

def module(
        imports: list = []
    ):
    def wrap(cls):
        return cls
    return wrap