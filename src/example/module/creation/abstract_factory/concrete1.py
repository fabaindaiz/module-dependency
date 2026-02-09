from dependency.core import component, providers
from example.module.creation.abstract_factory import AbtractFactory, AbtractProductA, AbtractProductB

class ConcreteProductA1(AbtractProductA):
    def doStuff(self) -> None:
        print("ConcreteProductA1 works")

class ConcreteProductB1(AbtractProductB):
    def doStuff(self) -> None:
        print("ConcreteProductB1 works")

@component(
    provider=providers.Factory,
)
class ConcreteAbtractFactory1(AbtractFactory):
    def createProductA(self) -> ConcreteProductA1:
        return ConcreteProductA1()

    def createProductB(self) -> ConcreteProductB1:
        return ConcreteProductB1()
