from dependency.core import Module, module
from example.plugin.base.number import NumberServiceComponent
from example.plugin.base.string import StringServiceComponent

@module(
    declaration=[
        NumberServiceComponent,
        StringServiceComponent,
    ],
)
class BaseModule(Module):
    def declare_providers(self):
        # Common providers
        from example.plugin.base.number.providers.fake import FakeNumberService
        from example.plugin.base.string.providers.fake import FakeStringService