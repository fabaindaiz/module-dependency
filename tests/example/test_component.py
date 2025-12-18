import pytest
from dependency.core import Container, Entrypoint
from example.plugin.base import BasePlugin
from example.plugin.base.number import NumberService, NumberServiceComponent
from example.plugin.base.number.providers.fake import FakeNumberService

@pytest.fixture
def setup():
    class ExampleApp(Entrypoint):
        def __init__(self) -> None:
            super().__init__(
                container=Container(),
                plugins=[BasePlugin])

    return ExampleApp()

def test_component(setup: object):
    numberService: NumberService = NumberServiceComponent.provide()
    assert isinstance(numberService, NumberService)
    assert numberService.getRandomNumber() == 42
