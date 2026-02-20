from abc import ABC, abstractmethod
from dependency_injector import providers
from dependency.core.agrupation import Module, module
from dependency.core.declaration import Component, component, instance
from dependency.core.injection import Injectable
from dependency.core.resolution import Container

@module()
class TModule(Module):
    pass

@component(
    module=TModule,
)
class TComponent(ABC, Component):
    @abstractmethod
    def method(self) -> str:
        pass

@instance(
    provider=providers.Singleton,
)
class TInstance(TComponent):
    def method(self) -> str:
        return "Hello, World!"

def test_declaration() -> None:
    container = Container()
    TModule.inject_container(container)
    injectables: list[Injectable] = list(TModule.resolve_providers())
    for provider in injectables:
        assert provider.check_resolved(injectables)

    assert TComponent.injectable.interface_cls == TComponent
    assert TComponent.injectable.implementation == TInstance

    component: TComponent = TComponent.provide()
    assert isinstance(component, TComponent)
    assert component.method() == "Hello, World!"
