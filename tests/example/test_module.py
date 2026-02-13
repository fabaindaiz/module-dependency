from dependency.core import Container, InjectionResolver, Module, module
from example.plugin.base.number.fake import NumberService
from example.plugin.base.string.fake import StringService
from example.plugin.hardware.factory.providers.creatorA import HardwareFactory
from example.plugin.hardware.observer.publisherA import HardwareObserver

@module()
class TestingModule(Module):
    pass

def test_change_parent_and_resolve():
    for component in (
        NumberService,
        StringService,
        HardwareFactory,
        HardwareObserver,
    ):
        component.change_parent(TestingModule)

    assert HardwareFactory.injection.parent == TestingModule.injection
    assert HardwareFactory.injection in TestingModule.injection.childs
    assert HardwareFactory.injection.reference == "TestingModule.HardwareFactory"

    container = Container()
    TestingModule.inject_container(container)
    loader = InjectionResolver(
        container=container,
        providers=TestingModule.resolve_providers(),
    )
    injectables = loader.resolve_dependencies()

    assert HardwareFactory.injection.injectable in injectables
    assert HardwareFactory.injection.injectable.is_resolved

    number_service: NumberService = NumberService.provide(starting_number=40)
    assert number_service.getRandomNumber() == 40

    hardware_factory: HardwareFactory = HardwareFactory.provide()
    hardware_a = hardware_factory.createHardware("A")
    hardware_a.doStuff("operation1")

    number_service1: NumberService = NumberService.provide()
    number_service2: NumberService = NumberService.provide()
    assert number_service1.getRandomNumber() == 42
    assert number_service2.getRandomNumber() == 43
