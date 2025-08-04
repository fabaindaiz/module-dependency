from abc import ABC, abstractmethod
from dependency.core.declaration.component import Component, component
from example.plugins.common import CommonModule

class GeneratorService(ABC):
    @abstractmethod
    def getRandomNumber(self) -> int:
        pass

@component(
    module=CommonModule,
    interface=GeneratorService
)
class GeneratorServiceComponent(Component):
    pass