from dependency_injector import containers, providers
from src.service1.container import Service1Provider
from src.service2.container import Service2Provider

# Declare all service providers
class Container(containers.DeclarativeContainer):
    service1_container = providers.Container(Service1Provider)
    service2_container = providers.Container(Service2Provider)