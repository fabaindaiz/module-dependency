from typing import Callable
from dependency_injector import containers, providers

def container(
        provided_cls: type,
        provider_cls: type
    ) -> type[containers.DynamicContainer]:
    class Container(containers.DynamicContainer):
        config = providers.Configuration()
        service = provider_cls(provided_cls, config)
    return Container

class Injectable:
    def __init__(self,
            inject_name: str,
            inject_cls: type,
            provided_cls: type,
            provider_cls: type = providers.Singleton
        ) -> None:
        self.inject_name = inject_name
        self.inject_cls = inject_cls
        self.provided_cls = provided_cls
        self.provider_cls = provider_cls
    
    def populate_container(self,
            container: containers.DynamicContainer,
            injetion: Callable[[type, type], type[containers.DynamicContainer]] = container,
            **kwargs) -> None:
        container_cls = injetion(self.provided_cls, self.provider_cls)
        setattr(container, self.inject_name, providers.Container(container_cls=container_cls, **kwargs))
        container.wire(modules=[self.inject_cls])