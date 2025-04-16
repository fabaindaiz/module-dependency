from dependency.core import provider, providers
from example.plugin.base.number import NumberService, NumberServiceComponent

@provider(
    component=NumberServiceComponent,
    provider = providers.Singleton
)
class FakeNumberService(NumberService):
    def __init__(self, config: dict) -> None:
        pass

    def getRandomNumber(self) -> int:
        return 42