from dependency.core import dependent
from dependency.core.declaration.dependent import Dependent
from example.plugins.module1.factory.interfaces import Product

@dependent()
class ProductA(Product, Dependent):
    def doStuff(self, operation: str) -> None:
        print(f"ProductA works with operation: {operation}")