from dependency.core import component, providers
from example.module.creation.abstract_factory import AbtractFactory, AbtractProductA, AbtractProductB

class ConcreteProductA2(AbtractProductA):
    def doStuff(self) -> None:
        print("ConcreteProductA2 works")

class ConcreteProductB2(AbtractProductB):
    def doStuff(self) -> None:
        print("ConcreteProductB2 works")

@component(
    provider=providers.Factory
)
class ConcreteAbtractFactory2(AbtractFactory):
    def createProductA(self) -> ConcreteProductA2:
        return ConcreteProductA2()

    def createProductB(self) -> ConcreteProductB2:
        return ConcreteProductB2()
