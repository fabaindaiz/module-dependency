from dependency.core import dependent
from dependency.core.declaration.dependent import Dependent
from example.plugins.module1.factory.interfaces import Product

@dependent()
class ProductB(Product, Dependent):
    def doStuff(self, operation: str) -> None:
        print(f"ProductB works with operation: {operation}")