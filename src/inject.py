from dependency_injector import providers
from src.container import Container

def inject(config: dict = {}):
    container = Container()
    container.init_resources()
    container.check_dependencies()
    container.config.from_dict(config)

    for provider in container.traverse(types=[providers.Container]):
        provider.inject(container)