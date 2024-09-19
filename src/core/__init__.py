from dependency_injector import containers, providers
from dependency_injector.wiring import Provide
from typing import Type, TypeVar, cast

class Provider:
    _imports: list

def provider(
        imports: list = [],
        provider = providers.Singleton
    ):
    def wrap(cls):
        class Container(containers.DeclarativeContainer):
            _config = providers.Configuration()
            _provider = provider(cls, _config)
        class WrapProvider(Provider):
            def __init__(self, component: "Component"):
                self._component = component
            _name = cls.__name__
            _container = Container
            _imports = imports
        return WrapProvider
    return wrap

class Component:
    _selector: dict[str, Provider]

    def dependencies(self):
        return self._selector["type1"](self)

def component(
        selector: dict[str, Provider] = {}
    ):
    T = TypeVar('T')
    def wrap(cls: Type[T]) -> Type[T]:
        class WrapComponent(Component):
            _selector: dict[str, Provider] = selector
            _name = cls.__name__
            _abc = cls

            def __call__(self,
                    service = Provide[f"{cls.__name__}._provider"]):
                return service
            
            @classmethod
            def wire(cls, container: containers.Container):
                return container.wire(modules=[cls])
        
        return cast(Type[T], WrapComponent())
    return wrap

class Module:
    _declaration: list[Component]
    _imports: list["Module"]
    _bootstrap: list[Component]

    def dependencies(self) -> list[Component]:
        layers = [c.dependencies() for c in self._declaration]
        for module in self._imports:
            layers.extend(module.dependencies())
        return layers

def module(
        declaration: list[Component] = [],
        imports: list[Module] = [],
        providers: list = [],
        bootstrap: list[Component] = [],
    ):
    def wrap(cls):
        class WrapModule(Module):
            _declaration = declaration
            _imports = imports
            _bootstrap = bootstrap
        return WrapModule()
    return wrap