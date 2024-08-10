from src.services.service1.instance1.container import Service1Provider
from src.services.service2.instance1.container import Service2Provider
from src.manager.manager1.instance1.container import Manager1Provider
from src.dependencies.loader import resolve_dependency, populate_layer

class AppEnvironment:
    config = {
        "service1": True,
        "service2": True,
    }
    
    dependencies = [
        Service1Provider,
        Manager1Provider,
        Service2Provider,
    ]

    #populate_layer(dependencies, config)
    resolve_dependency(dependencies, config)