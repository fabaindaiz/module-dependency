from dependency_injector import containers, providers
from dependency_injector.wiring import Provide
from typing import TypeVar, cast

class Container(containers.DynamicContainer):
    config: providers.Configuration = providers.Configuration()

class Providable:
    def __init__(self,
            base_cls: type,
            inject_cls: type,
            provided_cls: type,
            provider_cls: providers.Provider = providers.Singleton
        ):
        self.base_cls = base_cls
        self.inject_cls = inject_cls
        class Container(containers.DeclarativeContainer):
            config = providers.Configuration()
            service = provider_cls(provided_cls, config)
        self.container = Container
    
    def populate_container(self, container: Container):
        setattr(container, self.base_cls.__name__, providers.Container(self.container, config=container.config))
        container.wire(modules=[self.inject_cls])


@staticmethod
def wrap(cls: type):
    T = TypeVar('T')
    class Provider:
        def __call__(self,
                service: type[T] = Provide[f"{cls.__name__}.service"]
            ) -> type[T]:
            return service
    return cast(type[T], Provider())

class WrapComponent(Component):
            _base_cls = cls
            
            def provided(self,
                    service: type[T] = Provide[f"{cls.__name__}.service"]
                ) -> type[T]:
                return service
            
            @classmethod
            def wire(cls, container: containers.Container):
                container.wire(modules=[cls])