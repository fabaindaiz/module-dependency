from dependency.core import dependent
from example.plugins.module1.factory.interfaces import Product

@dependent()
class ProductA(Product):
    def doStuff(self, operation: str) -> None:
        print(f"ProductA works with operation: {operation}")