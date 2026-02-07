from dependency_injector.wiring import inject
from dependency.core import Component, component, providers
from dependency.core.injection import LazyProvide
from example.plugin.hardware.interfaces import Hardware
from example.plugin.base.number import NumberService

@component(
    imports=[
        NumberService,
    ],
    provider=providers.Factory,
)
class HardwareA(Hardware, Component):
    @inject
    def doStuff(self,
            operation: str,
            number: NumberService = LazyProvide(NumberService.reference),
        ) -> None:
        random_number = number.getRandomNumber()
        print(f"HardwareA {random_number} works with operation: {operation}")
