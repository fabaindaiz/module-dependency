from dependency_injector import containers, providers

class ContainerLoader:
    def __init__(self, container: containers.Container, *args, **kwargs):
        container.init_resources()
        container.check_dependencies()

        for provider in container.traverse(types=[providers.Container]):
            if provider.last_overriding:
                provider.inject(container) # type: ignore