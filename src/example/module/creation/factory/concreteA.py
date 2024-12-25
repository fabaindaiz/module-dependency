from dependency.core import provider, providers
from example.module.creation.factory import Factory, FactoryComponent, FactoryInterface

class ConcreteInterfaceA(FactoryInterface):
    def work(self) -> None:
        print("ConcreteProductA works")

@provider(
    provider=providers.Factory,
    component=FactoryComponent
)
class ConcreteFactoryA(Factory):
    def create(self) -> ConcreteInterfaceA:
        return ConcreteInterfaceA()