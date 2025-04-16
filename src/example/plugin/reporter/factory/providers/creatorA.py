from dependency.core import provider, providers
from example.plugin.reporter.factory import ReporterFactory, ReporterFactoryComponent
from example.plugin.reporter.factory.interfaces import Reporter
from example.plugin.reporter.factory.products.productA import ReporterA

@provider(
    component=ReporterFactoryComponent,
    dependents=[
        ReporterA,
    ],
    provider = providers.Singleton
)
class ReporterFactoryCreatorA(ReporterFactory):
    def __init__(self, config: dict):
        print("FactoryCreatorA initialized")

    def createProduct(self, product: str) -> Reporter:
        instance: Reporter
        match product:
            case "A":
                instance = ReporterA()
                return instance
            case _:
                raise ValueError(f"Unknown product type: {product}")