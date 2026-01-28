from dependency.core import Product, product
from example.plugin.hardware.interfaces import Hardware

@product()
class HardwareC(Hardware, Product):
    def doStuff(self, operation: str) -> None:
        print(f"HardwareC works with operation: {operation}")
