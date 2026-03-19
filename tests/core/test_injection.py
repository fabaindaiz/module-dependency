import pytest
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from dependency.core.injection import ContainerInjection, ProviderInjection, Injectable
from dependency.core.exceptions import ProvisionError

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
    setattr(container, container1.name, container1.container)

    container.wire((Interface,))
    with pytest.raises(AttributeError):
        Interface().test()

    container1.resolve_providers()
    for provider in list(container1.resolve_injectables()):
        container.wire(provider.modules_cls)

    container.wire((Interface,))
    assert Interface().test() == "Injected service: Test method called"

def test_injection_change_parent() -> None:
    """change_parent actualiza el reference y desvincula del parent anterior."""
    container1 = ContainerInjection(name="root1")
    container2 = ContainerInjection(name="root2")

    injectable = Injectable(interface_cls=object)
    provider = ProviderInjection(
        name="svc",
        injectable=injectable,
        parent=container1,
    )

    assert provider.reference == "root1.svc"
    assert provider in container1.childs

    provider.change_parent(container2)
    assert provider.reference == "root2.svc"
    assert provider in container2.childs
    assert provider not in container1.childs

def test_injection_orphan_reference_raises() -> None:
    """ProviderInjection sin parent lanza ProvisionError al acceder a .reference."""
    injectable = Injectable(interface_cls=object)
    orphan = ProviderInjection(name="orphan", injectable=injectable)

    with pytest.raises(ProvisionError):
        _ = orphan.reference
