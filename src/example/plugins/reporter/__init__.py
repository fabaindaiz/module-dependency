from dependency.core import Module, module
from example.plugins.reporter.factory import ReporterFactoryComponent
from example.plugins.reporter.facade import ReportFacadeComponent

@module(
    declaration=[
        ReporterFactoryComponent,
        ReportFacadeComponent
    ],
    bootstrap=[
        ReportFacadeComponent
    ]
)
class ReporterModule(Module):
    def declare_providers(self):
        # Common providers
        from example.plugins.reporter.factory.providers.creatorA import ReporterFactoryCreatorA
        from example.plugins.reporter.facade.providers.facadeA import ReporterFacadeA