from dependency_injector import containers, providers
from src.services.service1.instance1.container import Service1Provider
from src.services.service2.instance1.container import Service2Provider
from src.manager.manager1.instance1.container import Manager1Provider
from src.container import Container

config = {
    "service1": True,
    "service2": True,
}

from src.manager.manager1.container import Manager1Container
issubclass(Manager1Provider, Manager1Container)

class AppEnvironment:
    container = Container()
    layer1 = containers.DynamicContainer()
    layer1.config = providers.Configuration()
    layer1.service1_container = providers.Container(Service1Provider, config=layer1.config)
    layer1.service2_container = providers.Container(Service2Provider, config=layer1.config)
    container.override(layer1)

    container.config.from_dict(config)
    container.loader()

    container = Container()
    layer2 = containers.DynamicContainer()
    layer2.config = providers.Configuration()
    layer2.manager1_container = providers.Container(Manager1Provider, config=layer2.config)
    container.override(layer2)

    container.config.from_dict(config)
    container.loader()