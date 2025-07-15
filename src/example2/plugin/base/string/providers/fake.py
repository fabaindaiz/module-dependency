from dependency.core import provider, providers
from example.plugin.base.string import StringService, StringServiceComponent

@provider(
    component=StringServiceComponent,
    provider = providers.Singleton
)
class FakeStringService(StringService):
    def __init__(self, config: dict) -> None:
        pass

    def getRandomString(self) -> str:
        return "randomString"