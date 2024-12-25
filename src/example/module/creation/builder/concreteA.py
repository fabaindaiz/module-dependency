from dependency.core import provider, providers
from example.module.creation.builder import Builder, BuilderComponent, BuilderInterface

class ConcreteInterfaceA(BuilderInterface):
    def __init__(self):
        self.__steps = []

    def stepA(self) -> None:
        self.__steps.append('A')

    def stepB(self) -> None:
        self.__steps.append('B')
    
    def work(self) -> None:
        print(self.__steps)

@provider(
    provider=providers.Singleton,
    component=BuilderComponent
)
class ConcreteFactoryA(Builder):
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self.__instance = ConcreteInterfaceA()

    def buildStepA(self) -> None:
        self.__instance.stepA()
    
    def buildStepB(self) -> None:
        self.__instance.stepB()

    def result(self) -> BuilderInterface:
        instance = self.__instance
        self.reset()
        return instance