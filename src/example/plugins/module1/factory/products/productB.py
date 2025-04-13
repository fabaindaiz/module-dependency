from dependency.core import dependent
from example.plugins.module1.factory.interfaces import Product

@dependent()
class ProductB(Product):
    def doStuff(self, operation: str) -> None:
        print(f"ProductB works with operation: {operation}")