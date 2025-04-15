from dependency.core import Module, module
from example.plugins.base.number import NumberServiceComponent
from example.plugins.base.string import StringServiceComponent

@module(
    declaration=[
        NumberServiceComponent,
        StringServiceComponent,
    ],
)
class BaseModule(Module):
    def declare_providers(self):
        # Common providers
        from example.plugins.base.number.providers.fake import FakeNumberService
        from example.plugins.base.string.providers.fake import FakeStringService