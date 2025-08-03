from collections import deque
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from dependency.core.injection.base import ContainerInjection, ProviderInjection

TEST_REFERENCE = "container1.container2.provider1"

class Provider:
    def test(self) -> str:
        return "Test method called"

class Component:
    @inject
    def test(self, service: Provider = Provide[TEST_REFERENCE]) -> str:
        return f"Injected service: {service.test()}"

def test_injection1():
    provider1 = ProviderInjection(
        name="provider1",
        component=Component,
        provided_cls=Provider,
        provider_cls=providers.Singleton)

    container1 = ContainerInjection(name="container1")
    container2 = ContainerInjection(name="container2")
    container1.child_add(container2)
    container2.child_add(provider1)
    assert provider1.reference == TEST_REFERENCE

    container = containers.DynamicContainer()
    setattr(container, container1.name, container1.inject_cls())
    deque(container1.child_inject(), maxlen=0)
    container1.child_wire(container)
    assert Component().test() == "Injected service: Test method called"