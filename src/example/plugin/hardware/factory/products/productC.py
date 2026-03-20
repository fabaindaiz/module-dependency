from dependency.core import Product, product, providers
from example.plugin.hardware import HardwarePlugin
from example.plugin.hardware.interfaces import Hardware

@product(
    module=HardwarePlugin,
    provider=providers.Factory,
)
class HardwareC(Hardware, Product):
    def doStuff(self, operation: str) -> None:
        print(f"HardwareC works with operation: {operation}")
