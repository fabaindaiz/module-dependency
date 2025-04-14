from dependency.core import dependent
from dependency.core.declaration.dependent import Dependent
from example.plugins.hardware.factory.interfaces import Hardware
from example.plugins.base.number import NumberService, NumberServiceComponent

@dependent(
    imports=[
        NumberServiceComponent
    ],
)
class HardwareA(Hardware, Dependent):
    def __init__(self) -> None:
        self.__number: NumberService = NumberServiceComponent.provide()

    def doStuff(self, operation: str) -> None:
        random_number = self.__number.getRandomNumber()
        print(f"HardwareA {random_number} works with operation: {operation}")