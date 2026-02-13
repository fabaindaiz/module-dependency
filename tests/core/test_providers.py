from abc import ABC, abstractmethod
from dependency_injector import containers, providers
from dependency.core.agrupation import Module, module
from dependency.core.declaration import Component, component

@module()
class TModule(Module):
    pass

class TProduct(ABC, Component):
    @abstractmethod
    def method(self) -> str:
        pass

@component(
    module=TModule,
    provider=providers.Factory,
)
class TProduct1(TProduct):
    def method(self) -> str:
        return "product1"

@component(
    module=TModule,
    provider=providers.Factory,
)
class TProduct2(TProduct):
    def method(self) -> str:
        return "product2"

@component(
    module=TModule,
    provider=providers.Aggregate({
        "product1": TProduct1.provider(),
        "product2": TProduct2.provider(),

    })
)
class TComponent(TProduct):
    pass

def test_providers() -> None:
    container = containers.DynamicContainer()
    setattr(container, TModule.injection.name, TModule.injection.inject_cls())
    for provider in TModule.injection.resolve_providers():
        provider.inject()

    product1: TProduct1 = TComponent.provide("product1")
    product2: TProduct2 = TComponent.provide("product2")

    assert isinstance(product1, TProduct1)
    assert isinstance(product2, TProduct2)
    assert product1.method() == "product1"
    assert product2.method() == "product2"
