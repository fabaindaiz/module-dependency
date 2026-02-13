from dependency_injector.wiring import inject
from dependency.core import Product, product, providers
from dependency.core.injection import LazyProvide
from example.plugin.hardware.interfaces import Hardware
from example.plugin.base.string import StringService

@product(
    imports=[
        StringService,
    ],
    provider=providers.Factory,
)
class HardwareB(Hardware, Product):
    @inject
    def doStuff(self,
            operation: str,
            string: StringService = LazyProvide[StringService.reference],
        ) -> None:
        random_string = string.getRandomString()
        print(f"HardwareB {random_string} works with operation: {operation}")
