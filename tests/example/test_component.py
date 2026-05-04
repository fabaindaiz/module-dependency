import pytest
from dependency.core import Container, Entrypoint
from example.plugin.base import BasePlugin
from example.plugin.base.number.fake import NumberService

@pytest.fixture
def setup():
    import example.plugin.base.deferred.uvloop # type: ignore

    class ExampleApp(Entrypoint):
        def __init__(self) -> None:
            super().__init__(
                container=Container(),
                plugins=[BasePlugin])
            super().initialize()

    return ExampleApp()

def test_component(setup: object):
    numberService1: NumberService = NumberService.provide()
    numberService2: NumberService = NumberService.provide()
    assert numberService1 == numberService2
    assert isinstance(numberService1, NumberService)

    number1 = numberService1.getRandomNumber()
    number2 = numberService2.getRandomNumber()
    assert number1 + 1 == number2
