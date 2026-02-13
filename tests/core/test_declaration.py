from abc import ABC, abstractmethod
from dependency_injector import containers, providers
from dependency.core.agrupation import Module, module
from dependency.core.declaration import Component, component, instance

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
    container = containers.DynamicContainer()
    setattr(container, TModule.injection.name, TModule.injection.inject_cls())
    for provider in TModule.injection.resolve_providers():
        provider.inject()

    assert TModule.__name__ == "TModule"
    assert TComponent.injection.injectable.interface_cls.__name__ == "TComponent"
    assert TInstance.__name__ == "TInstance"

    component: TComponent = TComponent.provide()
    assert isinstance(component, TComponent)
    assert component.method() == "Hello, World!"
