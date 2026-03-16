from dependency.core import Component, component, providers
from dependency.core.injection import LazyProvider
from example.plugin.reporter import ReporterPlugin
from example.plugin.reporter.interfaces import Reporter
from example.plugin.reporter.factory.productA import ReporterA

@component(
    module=ReporterPlugin,
    imports=[
        ReporterA,
    ],
    provider=providers.Singleton,
)
class ReporterFactory(Component):
    def __init__(self):
        print("Factory initialized")

    def createProduct(self,
        product: str,
        factoryA: providers.Factory[ReporterA] = LazyProvider[ReporterA],
    ) -> Reporter:
        instance: Reporter
        match product:
            case "A":
                instance = factoryA()
                return instance
            case _:
                raise ValueError(f"Unknown product type: {product}")
