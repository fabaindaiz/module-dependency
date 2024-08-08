from dependency_injector import containers, providers
from src.services.service1.instance1.container import Service1Provider
from src.services.service2.instance1.container import Service2Provider
from src.manager.manager1.instance1.container import Manager1Provider
from src.container import Container

config = {
    "service1": True,
    "service2": True,
}

@containers.override(Container)
class Layer1Container(containers.DeclarativeContainer):
    __self__ = providers.Self()
    config: providers.Configuration = providers.Configuration()

    service2_container = providers.Container(Service2Provider, config=config)

container = Container()
container.config.from_dict(config)
container.loader()

@containers.override(Container)
class Layer2Container(containers.DeclarativeContainer):
    __self__ = providers.Self()
    config: providers.Configuration = providers.Configuration()

    service1_container = providers.Container(Service1Provider, config=config)

    manager1_container = providers.Container(Manager1Provider, config=config)

container = Container()
container.config.from_dict(config)
container.loader()