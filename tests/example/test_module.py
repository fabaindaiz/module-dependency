from dependency.core import Container, InjectionResolver, Module, module
from example.plugin.base.number.fake import NumberService, NumberServiceComponent
from example.plugin.base.string.fake import StringService, StringServiceComponent
from example.plugin.hardware.factory.providers.creatorA import HardwareFactory, HardwareFactoryComponent
from example.plugin.hardware.observer.publisherA import HardwareObserver, HardwareObserverComponent

@module()
class TestingModule(Module):
    pass

def test_change_parent_and_resolve():
    for component in (
        NumberServiceComponent,
        StringServiceComponent,
        HardwareFactoryComponent,
        HardwareObserverComponent,
    ):
        component.injection.change_parent(TestingModule.injection)

    assert HardwareFactoryComponent.injection.parent == TestingModule.injection
    assert HardwareFactoryComponent.injection in TestingModule.injection.childs
    assert HardwareFactoryComponent.injection.reference == "TestingModule.HardwareFactoryComponent"

    container = Container()
    TestingModule.inject_container(container)
    loader = InjectionResolver(
        container=container,
        injectables=TestingModule.resolve_providers(),
    )
    injectables = loader.resolve_dependencies()

    assert HardwareFactoryComponent.injection.injectable in injectables
    assert HardwareFactoryComponent.injection.injectable.is_resolved

    number_service: NumberService = NumberServiceComponent.provide(starting_number=40)
    assert number_service.getRandomNumber() == 40

    hardware_factory: HardwareFactory = HardwareFactoryComponent.provide()
    hardware_a = hardware_factory.createHardware("A")
    hardware_a.doStuff("operation1")

    number_service1: NumberService = NumberServiceComponent.provide()
    number_service2: NumberService = NumberServiceComponent.provide()
    assert number_service1.getRandomNumber() == 42
    assert number_service2.getRandomNumber() == 43
