from abc import ABC, abstractmethod
from dependency_injector import providers
from dependency.core.agrupation import Module, module
from dependency.core.declaration import Component, component, instance
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
    for provider in TModule.injection.resolve_providers():
        assert provider.check_resolved

    assert TComponent.injection.injectable.interface_cls == TComponent
    assert TComponent.injection.injectable.implementation == TInstance

    component: TComponent = TComponent.provide()
    assert isinstance(component, TComponent)
    assert component.method() == "Hello, World!"
