from dependency.core import provider, providers
from example.plugins.module1.factory import Creator, CreatorComponent
from example.plugins.module1.factory.interfaces import Product
from example.plugins.module1.factory.products.productA import ProductA
from example.plugins.module1.factory.products.productB import ProductB

@provider(
    component=CreatorComponent,
    dependents=[
        ProductA,
        ProductB
    ],
    provider = providers.Singleton
)
class CreatorA(Creator):
    def createProduct(self, product: str) -> Product:
        match product:
            case "A":
                return ProductA()
            case "B":
                return ProductB()
            case _:
                raise ValueError(f"Unknown product type: {product}")