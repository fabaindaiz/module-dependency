from dependency_injector import containers, providers
from src.service1.instance1.container import Service1Provider
from src.service2.instance1.container import Service2Provider
from src.container import Container

# Step 1: Container declaration
@containers.override(Container)
class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    service1_container = providers.Container(Service1Provider, config=config)
    service2_container = providers.Container(Service2Provider, config=config)

config = {
    "service1": True,
    "service2": True,
}

container = Container()
container.init_resources()
container.check_dependencies()
container.config.from_dict(config)

# Step 2: Container initialization
container.loader()