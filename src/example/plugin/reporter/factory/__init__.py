from abc import ABC, abstractmethod
from dependency.core.declaration.component import Component, component
from example.plugin.reporter.factory.interfaces import Reporter
from example.plugin.reporter import ReporterPlugin

class ReporterFactory(ABC):
    @abstractmethod
    def createProduct(self, product: str) -> Reporter:
        pass

@component(
    module=ReporterPlugin,
    interface=ReporterFactory,
)
class ReporterFactoryComponent(Component):
    pass