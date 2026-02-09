from dependency.core import instance, providers
from example.module.structural.bridge.abstraction import Abstraction
from example.module.structural.bridge.implementation import Implementation

@instance(
    imports=[
        Implementation
    ],
    provider=providers.Singleton,
)
class AbstractionImplementation(Abstraction):
    def __init__(self):
        self.implementation: Implementation = Implementation.provide()

    def feature1(self):
        self.implementation.method1()

    def feature2(self):
        self.implementation.method2()
        self.implementation.method3()
