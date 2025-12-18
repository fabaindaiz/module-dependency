from dependency.core import instance, providers
from example.plugin.base.number import NumberService, NumberServiceComponent

@instance(
    component=NumberServiceComponent,
    provider=providers.Singleton
)
class FakeNumberService(NumberService):
    def __init__(self) -> None:
        self.__number = 41

    def getRandomNumber(self) -> int:
        self.__number += 1
        return self.__number
