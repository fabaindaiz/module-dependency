from dependency_injector import containers, providers
from dependency.core.container import Container

class Injectable:
    def __init__(self,
            inject_name: str,
            inject_cls: type,
            provided_cls: type,
            provider_cls: type = providers.Singleton
        ) -> None:
        class Container(containers.DynamicContainer):
            config = providers.Configuration()
            service = provider_cls(provided_cls, config)
        self.inject_name = inject_name
        self.inject_cls = inject_cls
        self.container = Container
    
    def populate_container(self, container: Container) -> None:
        setattr(container, self.inject_name, providers.Container(self.container, config=container.config))
        container.wire(modules=[self.inject_cls])