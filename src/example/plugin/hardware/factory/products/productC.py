from dependency.core import Product, product, providers
from example.plugin.hardware.interfaces import Hardware

@product(
    provider=providers.Factory,
)
class HardwareC(Hardware, Product):
    def doStuff(self, operation: str) -> None:
        print(f"HardwareC works with operation: {operation}")
