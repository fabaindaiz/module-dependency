from dependency.core import Container, Entrypoint
from example.plugin.base import BasePlugin
from example.plugin.base.number import NumberService, NumberServiceComponent
from example.plugin.base.number.providers.fake import FakeNumberService

class ExampleApp(Entrypoint):
    def __init__(self) -> None:
        super().__init__(
            container=Container(),
            plugins=[BasePlugin])

app = ExampleApp()
def test_component():
    numberService = NumberServiceComponent.provide()
    assert isinstance(numberService, NumberService)
    assert numberService.getRandomNumber() == 42