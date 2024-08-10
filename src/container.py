from dependency_injector import containers, providers
from src.services.service1.container import Service1Container
from src.services.service2.container import Service2Container
from src.manager.manager1.container import Manager1Container

class ContainerLoader:
    def __init__(self, container: containers.Container, *args, **kwargs):
        container.init_resources()
        container.check_dependencies()

        for provider in container.traverse(types=[providers.Container]):
            if provider.last_overriding:
                provider.inject(container) # type: ignore

class Container(containers.DeclarativeContainer):
    __self__ = providers.Self()
    loader = providers.Singleton(ContainerLoader, __self__)
    config: providers.Configuration = providers.Dependency() # type: ignore

    service1_container = providers.Container(Service1Container)
    service2_container = providers.Container(Service2Container)

    manager1_container = providers.Container(Manager1Container)

