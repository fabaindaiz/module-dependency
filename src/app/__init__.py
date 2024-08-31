from src.dependencies.loader import Container, resolve_dependency
from src.manager.type1.container import Type1ManagerProvider
from src.services.factory.type1.container import Type1FactoryServiceProvider
from src.services.singleton.type1.container import Type1SingletonServiceProvider

class AppEnvironment:
    config = {
        "service1": True,
        "service2": True,
    }
    
    dependencies = [
        Type1ManagerProvider,
        Type1FactoryServiceProvider,
        Type1SingletonServiceProvider,
    ]

    container = Container()
    container.config.from_dict(config)
    resolve_dependency(container, dependencies)