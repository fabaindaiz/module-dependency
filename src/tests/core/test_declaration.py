from abc import ABC, abstractmethod
from collections import deque
from dependency_injector import containers, providers
from dependency.core.declaration.module import Module, module
from dependency.core.declaration.component import Component, component
from dependency.core.declaration.instance import instance

class TInterface(ABC):
    @abstractmethod
    def method(self) -> str:
        pass

@module(
    module=None,
)
class TModule(Module):
    pass

@component(
    module=TModule,
    interface=TInterface,
)
class TComponent(Component):
    pass

@instance(
    component=TComponent,
    imports=[],
    provider=providers.Singleton,
)
class TInstance(TInterface):
    def method(self) -> str:
        return "Hello, World!"

def test_declaration():
    container = containers.DynamicContainer()
    setattr(container, TModule.injection.name, TModule.injection.inject_cls())
    deque(TModule.injection.child_inject(), maxlen=0)
    TModule.injection.child_wire(container)

    component: TInterface = TComponent.provide()
    assert isinstance(component, TInterface)
    assert component.method() == "Hello, World!"