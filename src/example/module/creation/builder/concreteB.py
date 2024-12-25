from dependency.core import provider, providers
from example.module.creation.builder import Builder, BuilderComponent, BuilderInterface

class ConcreteInterfaceB(BuilderInterface):
    def __init__(self):
        self.__steps = {}

    def stepA(self) -> None:
        self.__steps.update({'A': True})

    def stepB(self) -> None:
        self.__steps.update({'B': True})
    
    def work(self) -> None:
        print(self.__steps)

@provider(
    provider=providers.Singleton,
    component=BuilderComponent
)
class ConcreteFactoryB(Builder):
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self.__instance = ConcreteInterfaceB()

    def buildStepA(self) -> None:
        self.__instance.stepA()
    
    def buildStepB(self) -> None:
        self.__instance.stepB()

    def result(self) -> BuilderInterface:
        instance = self.__instance
        self.reset()
        return instance