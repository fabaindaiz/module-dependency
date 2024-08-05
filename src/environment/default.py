# Step 1: Providers injection
from src.service1.instance1.container import Service1Provider
from src.service2.instance1.container import Service2Provider

from dependency_injector import containers, providers
from src.container import Container

@containers.override(Container)
class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    service1_container = providers.Container(Service1Provider, config=config)
    service2_container = providers.Container(Service2Provider, config=config)

# Step 2: container injection
from src.inject import inject
inject({"config": True})