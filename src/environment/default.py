from dependency_injector import containers, providers
from src.services.service1.instance1.container import Service1Provider
from src.services.service2.instance1.container import Service2Provider
from src.container import Container

# Step 1: Container declaration
@containers.override(Container)
class AppContainer(Container):
    config = providers.Configuration()
    service1_container = providers.Container(Service1Provider, config=config)
    service2_container = providers.Container(Service2Provider, config=config)

config = {
    "service1": True,
    "service2": True,
}

# Step 2: Container initialization
container = Container()
container.loader(config)