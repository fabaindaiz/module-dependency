from dependency.core import ProviderModule, module
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
class ReporterModule(ProviderModule):
    def declare_providers(self):
        # Common providers
        from example.plugins.reporter.factory.providers.creatorA import ReporterFactoryCreatorA
        from example.plugins.reporter.facade.providers.facadeA import ReporterFacadeA