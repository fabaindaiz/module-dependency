from dependency.core import instance, providers
from example.module.structural.bridge.implementation import Implementation

@instance(
    provider=providers.Singleton,
)
class ConcreteImplementation(Implementation):
    def method1(self):
        pass

    def method2(self):
        pass

    def method3(self):
        pass
