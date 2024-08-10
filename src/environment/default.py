from src.services.service1.instance1.container import Service1Provider
from src.services.service2.instance1.container import Service2Provider
from src.manager.manager1.instance1.container import Manager1Provider
from src.loader import populate_layers

config = {
    "service1": True,
    "service2": True,
}

class AppEnvironment:
    dependencies = [
        Service1Provider,
        Service2Provider,
        Manager1Provider,
    ]

    populate_layers(dependencies, config)