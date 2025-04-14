from dependency.core import dependent
from dependency.core.declaration.dependent import Dependent
from example.plugins.module1.factory.interfaces import Product

@dependent()
class ProductC(Product, Dependent):
    def doStuff(self, operation: str) -> None:
        print(f"ProductC works with operation: {operation}")