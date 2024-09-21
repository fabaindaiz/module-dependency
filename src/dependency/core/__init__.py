from dependency_injector import containers, providers
from dependency_injector.wiring import Provide
from dependency.core.container import Providable
from typing import TypeVar

class Component:
    _base_cls: type

    def __repr__(self) -> str:
        return self._base_cls.__name__

def component(
    ):
    T = TypeVar('T')
    def wrap(cls: type[T]):
        class WrapComponent(Component):
            _base_cls = cls
            
            def provided(self,
                    service: type[T] = Provide[f"{cls.__name__}.service"]
                ) -> type[T]:
                return service
            
            @classmethod
            def wire(cls, container: containers.Container):
                container.wire(modules=[cls])
        return WrapComponent()
    return wrap

class Provider:
    _provided_cls: type
    _imports: list[Component]
    _provider: Providable

    def __repr__(self) -> str:
        return self._provided_cls.__name__

def provider(
        component: Component,
        imports: list[Component] = [],
        provider: providers.Provider = providers.Singleton
    ):
    def wrap(cls):
        class WrapProvider(Provider):
            _provided_cls = cls
            _imports = imports
            _provider = Providable(
                base_cls=component._base_cls,
                inject_cls=component.__class__,
                provided_cls=cls,
                provider_cls=provider
            )
        return WrapProvider()
    return wrap

class Module:
    _module_cls: type
    _declaration: list[Component]
    _imports: list["Module"]
    _bootstrap: list[Component]

    # TODO: extract to Selector Module
    _providers: list[Provider]
    def providers(self) -> list[Provider]:
        providers = self._providers
        for module in self._imports:
            providers.extend(module.providers())
        return providers
    
    def __repr__(self) -> str:
        return self._module_cls.__name__

def module(
        declaration: list[Component] = [],
        imports: list[Module] = [],
        providers: list = [],
        bootstrap: list[Component] = [],
    ):
    def wrap(cls):
        class WrapModule(Module):
            _module_cls = cls
            _declaration = declaration
            _imports = imports
            _providers = providers
            _bootstrap = bootstrap
        return WrapModule()
    return wrap