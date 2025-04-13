from dependency.core import dependent
from example.plugins.module1.factory.interfaces import Product

@dependent()
class ProductA(Product):
    def doStuff(self) -> None:
        print("ProductA works")