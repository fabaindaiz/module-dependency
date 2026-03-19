import pytest
from abc import ABC, abstractmethod
from dependency_injector import providers
from dependency.core.agrupation import Module, module
from dependency.core.declaration import Component, component, instance
from dependency.core.injection import Injectable
from dependency.core.resolution import Container
from dependency.core.exceptions import DeclarationError

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

@component(
    module=TModule,
    provider=providers.Factory,
)
class TComponentInline(Component):
    """Component con provider inline, sin @instance separado."""
    def method(self) -> str:
        return "inline"


def test_declaration() -> None:
    container = Container()
    TModule.inject_container(container)
    injectables: set[Injectable] = set(TModule.resolve_injectables())
    for provider in injectables:
        assert provider.resolve_if_posible(injectables)

    assert TComponent.injectable.interface_cls == TComponent
    assert TComponent.injectable.implementation == TInstance

    component: TComponent = TComponent.provide()
    assert isinstance(component, TComponent)
    assert component.method() == "Hello, World!"

def test_declaration_inline_provider() -> None:
    """@component con provider inline puede proveerse sin @instance."""
    container = Container()
    TModule.inject_container(container)
    TModule.resolve_providers()

    injectables = set(TModule.resolve_injectables())
    for injectable in injectables:
        injectable.resolve_if_posible(injectables)

    result = TComponentInline.provide()
    assert isinstance(result, TComponentInline)
    assert result.method() == "inline"

def test_declaration_reimplementation() -> None:
    """El último @instance declarado para un @component es el que se usa."""
    @instance(
        provider=providers.Singleton,
    )
    class TInstanceSecond(TComponent):
        """Segunda implementación de TComponent — reemplaza a TInstance."""
        def method(self) -> str:
            return "second"

    assert TComponent.injectable.implementation == TInstanceSecond
    assert TComponent.injectable.implementation != TInstance

def test_declaration_provide_before_resolved() -> None:
    """Acceder a .provide() antes de resolver lanza DeclarationError."""
    @component()
    class TUnresolved(Component):
        pass

    with pytest.raises(DeclarationError):
        TUnresolved.provide()
