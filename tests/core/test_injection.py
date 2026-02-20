import pytest
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from dependency.core.injection import ContainerInjection, ProviderInjection, Injectable

TEST_REFERENCE = "container1.container2.provider1"

class Instance:
    def test(self) -> str:
        return "Test method called"

class Interface:
    @inject
    def test(self, service: Instance = Provide[TEST_REFERENCE]) -> str:
        return f"Injected service: {service.test()}"

def test_injection1() -> None:
    container1 = ContainerInjection(name="container1")
    container2 = ContainerInjection(name="container2", parent=container1)

    injectable1 = Injectable(
        interface_cls=Interface,
        implementation=Instance,
    )
    provider1 = ProviderInjection(
        name="provider1",
        injectable=injectable1,
        parent=container2,
        provider=providers.Singleton(Instance),
    )
    assert provider1.reference == TEST_REFERENCE

    container = containers.DynamicContainer()
    setattr(container, container1.name, container1.inject_cls())

    container.wire((Interface,))
    with pytest.raises(AttributeError):
        Interface().test()

    for provider in list(container1.resolve_providers()):
        container.wire(provider.modules_cls)

    container.wire((Interface,))
    assert Interface().test() == "Injected service: Test method called"
