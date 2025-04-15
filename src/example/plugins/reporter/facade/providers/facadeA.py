from dependency.core import provider, providers
from example.plugins.reporter.facade import ReportFacade, ReportFacadeComponent
from example.plugins.reporter.factory import ReporterFactory, ReporterFactoryComponent
from example.plugins.hardware.bridge import HardwareAbstraction, HardwareAbstractionComponent
from example.plugins.hardware.factory.interfaces import Hardware


@provider(
    component=ReportFacadeComponent,
    imports=[
        ReporterFactoryComponent,
        HardwareAbstractionComponent
    ],
    provider = providers.Singleton
)
class ReporterFacadeA(ReportFacade):
    def __init__(self, config: dict) -> None:
        self.__factory: ReporterFactory = ReporterFactoryComponent.provide()
        self.__bridge: HardwareAbstraction = HardwareAbstractionComponent.provide()
        
        self.startModule()
        print("FacadeA initialized")

    def startModule(self) -> None:
        reporter = self.__factory.createProduct(product="A")
        self.__bridge.someOperation(product="A")
        self.__bridge.otherOperation(product="B")
        print("reportProducts:", reporter.reportProducts())
        print("reportOperations:", reporter.reportOperations())
