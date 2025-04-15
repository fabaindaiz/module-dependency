from abc import ABC, abstractmethod
from dependency.core import Component, component

class ReportFacade(ABC):
    @abstractmethod
    def startModule(self) -> None:
        pass

@component(
    interface=ReportFacade
)
class ReportFacadeComponent(Component):
    pass