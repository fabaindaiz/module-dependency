from dependency_injector import providers
from dependency.core.injection.universal import ContainerInjection, ProviderInjection

class Test: ...

def test_injection1():
    provider1 = ProviderInjection(
        name="provider1",
        provided_cls=Test,
        provider_cls=providers.Singleton,
        wire_cls=None
    )

    container1 = ContainerInjection(name="container1")
    container2 = ContainerInjection(name="container2")
    container1.inject_child(container2)
    container2.inject_child(provider1)

    assert provider1.reference() == "container1.container2.provider1"

def test_injection2():
    provider2 = ProviderInjection(
        name="provider2",
        provided_cls=Test,
        provider_cls=providers.Singleton,
        wire_cls=None
    )

    container1 = ContainerInjection(name="container1")
    container2 = ContainerInjection(name="container2")
    container1.inject_child(container2)
    container2.inject_child(provider2)

    assert provider2.reference() == "container1.container2.provider2"