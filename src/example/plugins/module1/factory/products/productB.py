from dependency.core import dependent
from example.plugins.module1.factory.interfaces import Product

@dependent()
class ProductB(Product):
    def doStuff(self) -> None:
        print("ProductB works")