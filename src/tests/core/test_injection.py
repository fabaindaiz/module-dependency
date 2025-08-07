from collections import deque
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from dependency.core.injection.base import ContainerInjection, ProviderInjection

TEST_REFERENCE = "container1.container2.provider1"

class Instance:
    def test(self) -> str:
        return "Test method called"

class Interface:
    @inject
    def test(self, service: Instance = Provide[TEST_REFERENCE]) -> str:
        return f"Injected service: {service.test()}"

def test_injection1():
    provider1 = ProviderInjection(
        name="provider1",
        interface_cls=Interface,
        provided_cls=Instance,
        provider_cls=providers.Singleton,
        component=Interface())

    container1 = ContainerInjection(name="container1")
    container2 = ContainerInjection(name="container2")
    container1.child_add(container2)
    container2.child_add(provider1)
    assert provider1.reference == TEST_REFERENCE

    container = containers.DynamicContainer()
    deque(container1.child_inject(), maxlen=0)
    setattr(container, container1.name, container1.inject_cls())
    container1.child_wire(container)
    assert Interface().test() == "Injected service: Test method called"