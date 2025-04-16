from dependency.core import Module, module
from example.plugin.reporter.factory import ReporterFactoryComponent
from example.plugin.reporter.facade import ReportFacadeComponent

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
        from example.plugin.reporter.factory.providers.creatorA import ReporterFactoryCreatorA
        from example.plugin.reporter.facade.providers.facadeA import ReporterFacadeA