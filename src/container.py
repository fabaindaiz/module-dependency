from dependency_injector import containers, providers
from src.service1.container import Service1Container
from src.service2.container import Service2Container

class ContainerLoader:
    def __init__(self, container: containers.Container):
        for provider in container.traverse(types=[providers.Container]):
            provider.inject(container)

# Declare all service providers
class Container(containers.DeclarativeContainer):
    __self__ = providers.Self()
    loader = providers.Singleton(ContainerLoader, __self__)

    config = providers.Dependency(providers.Configuration)
    service1_container = providers.Container(Service1Container)
    service2_container = providers.Container(Service2Container)