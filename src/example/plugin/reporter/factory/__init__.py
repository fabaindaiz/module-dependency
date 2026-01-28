from dependency.core import Product, product, providers
from example.plugin.reporter import ReporterPlugin
from example.plugin.reporter.interfaces import Reporter
from example.plugin.reporter.factory.productA import ReporterA

@product(
    module=ReporterPlugin,
    products=[
        ReporterA,
    ],
    provider=providers.Singleton,
)
class ReporterFactory(Product):
    def __init__(self):
        print("Factory initialized")

    def createProduct(self, product: str) -> Reporter:
        instance: Reporter
        match product:
            case "A":
                instance = ReporterA()
                return instance
            case _:
                raise ValueError(f"Unknown product type: {product}")
