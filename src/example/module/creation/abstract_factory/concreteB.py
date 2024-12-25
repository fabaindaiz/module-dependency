from dependency.core import provider, providers
from example.module.creation.abstract_factory import AbtractFactory, AbtractFactoryComponent, AbtractFactoryInterface1, AbtractFactoryInterface2

class ConcreteInterfaceB1(AbtractFactoryInterface1):
    def work1(self) -> None:
        print("ConcreteProductB1 works")

class ConcreteInterfaceB2(AbtractFactoryInterface2):
    def work2(self) -> None:
        print("ConcreteProductB2 works")

@provider(
    provider=providers.Factory,
    component=AbtractFactoryComponent
)
class ConcreteAbtractFactoryA(AbtractFactory):
    def createType1(self) -> AbtractFactoryInterface1:
        return ConcreteInterfaceB1()
    
    def createType2(self) -> AbtractFactoryInterface2:
        return ConcreteInterfaceB2()