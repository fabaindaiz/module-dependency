from dependency_injector import containers, providers

class ContainerLoader:
    def __init__(self, container: containers.Container, config: dict):
        container.init_resources()
        container.check_dependencies()
        container.config.from_dict(config)

        for provider in container.traverse(types=[providers.Container]):
            provider.inject(container)