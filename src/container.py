from dependency_injector import containers, providers
from src.service1.container import Service1Container
from src.service2.container import Service2Container

# Declare all service providers
class Container(containers.DeclarativeContainer):
    service1_container = providers.Container(Service1Container)
    service2_container = providers.Container(Service2Container)