from dependency.core import dependent
from dependency.core.declaration.dependent import Dependent
from example.plugins.hardware.factory.interfaces import Hardware
from example.plugins.base.string import StringService, StringServiceComponent

@dependent(
    imports=[
        StringServiceComponent
    ],
)
class HardwareB(Hardware, Dependent):
    def __init__(self) -> None:
        self.__string: StringService = StringServiceComponent.provide()

    def doStuff(self, operation: str) -> None:
        random_string = self.__string.getRandomString()
        print(f"HardwareB {random_string} works with operation: {operation}")