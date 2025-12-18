from typing import Container
from dependency.core import Container, Module, module
from example.plugin.base.number.providers.fake import NumberService, NumberServiceComponent

@module()
class TestingModule(Module):
    pass

def test_change_parent_and_resolve():
    NumberServiceComponent.injection.change_parent(TestingModule.injection)
    assert NumberServiceComponent.injection.parent == TestingModule.injection
    assert NumberServiceComponent.injection in TestingModule.injection.childs
    assert NumberServiceComponent.reference == "TestingModule.NumberServiceComponent"

    container = Container()
    injectables = TestingModule.resolve_providers(container)
    for injectable in injectables:
        injectable.do_wiring(container)
    assert NumberServiceComponent.injection.injectable in injectables
    assert NumberServiceComponent.injection.injectable.is_resolved

    number_service1: NumberService = NumberServiceComponent.provide()
    number_service2: NumberService = NumberServiceComponent.provide()
    assert number_service1.getRandomNumber() == 42
    assert number_service2.getRandomNumber() == 43
