from dependency.core import provider, providers
from example.module.creation.abstract_factory import AbtractFactory, AbtractFactoryComponent, AbtractFactoryInterface1, AbtractFactoryInterface2

class ConcreteInterfaceA1(AbtractFactoryInterface1):
    def work1(self) -> None:
        print("ConcreteProductA1 works")

class ConcreteInterfaceA2(AbtractFactoryInterface2):
    def work2(self) -> None:
        print("ConcreteProductA2 works")

@provider(
    provider=providers.Factory,
    component=AbtractFactoryComponent
)
class ConcreteAbtractFactoryA(AbtractFactory):
    def createType1(self) -> AbtractFactoryInterface1:
        return ConcreteInterfaceA1()
    
    def createType2(self) -> AbtractFactoryInterface2:
        return ConcreteInterfaceA2()