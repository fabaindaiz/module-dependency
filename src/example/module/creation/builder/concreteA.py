from dependency.core import instance, providers
from example.module.creation.builder import Builder, Product

class Product1(Product):
    def __init__(self):
        self._steps: list[str] = []

    def setStep(self, step: str) -> None:
        self._steps.append(step)

    def doStuff(self) -> None:
        print(self._steps)

@instance(
    provider=providers.Factory,
)
class ConcreteBuilder1(Builder):
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._product = Product1()

    def buildStepA(self) -> None:
        self._product.setStep('A1')

    def buildStepB(self) -> None:
        self._product.setStep('B1')

    def buildStepZ(self) -> None:
        self._product.setStep('Z1')

    def result(self) -> Product:
        product = self._product
        self.reset()
        return product
