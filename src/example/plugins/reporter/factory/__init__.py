from abc import ABC, abstractmethod
from dependency.core import Component, component
from example.plugins.reporter.factory.interfaces import Reporter

class ReporterFactory(ABC):
    @abstractmethod
    def createProduct(self, product: str) -> Reporter:
        pass

@component(
    interface=ReporterFactory
)
class ReporterFactoryComponent(Component):
    pass