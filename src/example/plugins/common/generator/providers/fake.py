from dependency.core.declaration.instance import instance, providers
from example.plugins.common.generator import GeneratorService, GeneratorServiceComponent

@instance(
    component=GeneratorServiceComponent,
    provider=providers.Singleton
)
class FakeGeneratorService(GeneratorService):
    def __init__(self) -> None:
        pass

    def getRandomNumber(self) -> int:
        return 42