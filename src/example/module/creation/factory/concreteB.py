from dependency.core import provider, providers
from example.module.creation.factory import Factory, FactoryComponent, FactoryInterface

class ConcreteInterfaceB(FactoryInterface):
    def work(self) -> None:
        print("ConcreteProductB works")

@provider(
    provider=providers.Factory,
    component=FactoryComponent
)
class ConcreteFactoryB(Factory):
    def create(self) -> ConcreteInterfaceB:
        return ConcreteInterfaceB()