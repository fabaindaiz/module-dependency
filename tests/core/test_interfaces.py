from abc import ABC, abstractmethod
from dependency_injector import providers
from dependency_injector.wiring import inject
from dependency.core.agrupation import Module, module
from dependency.core.declaration import Component, component
from dependency.core.injection import Injectable, LazyProvide
from dependency.core.resolution import Container

@module()
class TModule(Module):
    pass

@component(
    module=TModule,
    provider=providers.Factory,
)
class TStandalone(Component):
    def method(self) -> str:
        return "Hello, World!"

class TProduct(ABC, Component):
    @abstractmethod
    def method(self) -> str:
        pass

@component(
    module=TModule,
    provider=providers.Factory,
)
class TProduct1(TProduct):
    @inject
    def get_standalone(self, standalone: TStandalone = LazyProvide[TStandalone.reference]) -> str:
        return standalone.method()

    def method(self) -> str:
        return self.get_standalone()

@component(
    module=TModule,
    imports=[TProduct1],
    provider=providers.Factory,
)
class TProduct2(TProduct):
    def method(self) -> str:
        return "Hello, World!"

def test_interfaces() -> None:
    container = Container()
    TModule.inject_container(container)

    injectables: list[Injectable] = list(TModule.resolve_providers())
    for injectable in injectables:
        injectable.check_resolved
    assert TProduct1.injection.injectable.check_resolved(injectables)
    assert TProduct2.injection.injectable.check_resolved(injectables)

    for injectable in injectables:
        injectable.wire(container)
    product1: TProduct1 = TProduct1.provide()
    product2: TProduct2 = TProduct2.provide()

    assert isinstance(product1, TProduct1)
    assert isinstance(product2, TProduct2)
    assert product1.method() == "Hello, World!"
    assert product2.method() == "Hello, World!"
