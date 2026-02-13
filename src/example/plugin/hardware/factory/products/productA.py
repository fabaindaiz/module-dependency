from dependency_injector.wiring import inject
from dependency.core import Product, product, providers
from dependency.core.injection import LazyProvide
from example.plugin.hardware.interfaces import Hardware
from example.plugin.base.number import NumberService

@product(
    imports=[
        NumberService,
    ],
    provider=providers.Factory,
)
class HardwareA(Hardware, Product):
    @inject
    def doStuff(self,
            operation: str,
            number: NumberService = LazyProvide[NumberService.reference],
        ) -> None:
        random_number = number.getRandomNumber()
        print(f"HardwareA {random_number} works with operation: {operation}")
