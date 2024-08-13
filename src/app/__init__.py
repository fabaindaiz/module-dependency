from src.services.service1.instance1.container import Service1Provider
from src.services.service2.instance1.container import Service2Provider
from src.manager.manager1.instance1.container import Manager1Provider
from src.dependencies.loader import Container, resolve_dependency

class MainEnvironment:
    config = {
        "service1": True,
        "service2": True,
    }
    
    dependencies = [
        Service1Provider,
        Service2Provider,
        Manager1Provider,
    ]

    container = Container()
    container.config.from_dict(config)
    resolve_dependency(container, dependencies)