from abc import ABC, abstractmethod
from dependency.core import Component, component
from example.plugin.reporter import ReporterPlugin

@component(
    module=ReporterPlugin,
)
class ReportFacade(ABC, Component):
    @abstractmethod
    def startModule(self) -> None:
        pass
