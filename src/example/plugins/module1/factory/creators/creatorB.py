from dependency.core import provider, providers
from example.plugins.module1.factory import Creator, CreatorComponent
from example.plugins.module1.factory.interfaces import Product
from example.plugins.module1.factory.products.productB import ProductB
from example.plugins.module1.factory.products.productC import ProductC

@provider(
    component=CreatorComponent,
    dependents=[
        ProductB,
        ProductC
    ],
    provider = providers.Singleton
)
class CreatorB(Creator):
    def createProduct(self, product: str) -> Product:
        match product:
            case "B":
                return ProductB()
            case "C":
                return ProductC()
            case _:
                raise ValueError(f"Unknown product type: {product}")