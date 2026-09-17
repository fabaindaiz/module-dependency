import pytest
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from dependency.core.injection import ContainerInjection, ProviderInjection, Injectable
from dependency.core.exceptions import DeclarationError, ProvisionError

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

    container1.attach()
    for provider in list(container1.collect_providers()):
        container.wire(provider.injectable.modules_cls)

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


# --------------------------------------------------------------------------------------
# A name under a container belongs to exactly one provider (D-056). It used to be a silent
# overwrite: the runtime resolved one and every caller of the other failed with an error
# naming neither.
# --------------------------------------------------------------------------------------


def _named(name: str) -> ProviderInjection:
    injectable = Injectable(interface_cls=type(name, (), {}))
    injectable.set_implementation(implementation=injectable.interface_cls, modules_cls=())
    node = ProviderInjection(name=name, injectable=injectable)
    node.set_provider(providers.Singleton(injectable.interface_cls))
    return node


def test_two_providers_cannot_claim_one_name_under_one_container() -> None:
    container = containers.DynamicContainer()
    _named("Collide").attach(container=container)

    with pytest.raises(DeclarationError) as failure:
        _named("Collide").attach(container=container)

    assert "Collide" in str(failure.value)


def test_attaching_the_same_provider_twice_is_allowed() -> None:
    """One declared module owns one sub-container; resolving twice is not an error."""
    container = containers.DynamicContainer()
    node = _named("Idempotent")

    node.attach(container=container)
    node.attach(container=container)

    assert container.Idempotent is node.provider


def test_the_same_name_under_different_containers_is_fine() -> None:
    """The 27 duplicate class names across test files rely on exactly this."""
    first = containers.DynamicContainer()
    second = containers.DynamicContainer()

    _named("Shared").attach(container=first)
    _named("Shared").attach(container=second)

    assert first.Shared is not second.Shared
