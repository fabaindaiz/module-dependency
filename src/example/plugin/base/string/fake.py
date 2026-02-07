from dependency.core import instance, providers
from example.plugin.base.string import StringService

@instance(
    component=StringService,
    provider=providers.Singleton,
)
class FakeStringService(StringService):
    def getRandomString(self) -> str:
        return "randomString"
