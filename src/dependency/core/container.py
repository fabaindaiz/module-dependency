from dependency.core.module.component import Component
from dependency_injector import containers, providers

class Container(containers.DynamicContainer):
    config: providers.Configuration = providers.Configuration()

    @staticmethod
    def from_dict(config: dict,
            required: bool = False):
        container = Container()
        container.config.from_dict(config, required)
        return container
    
    @staticmethod
    def from_json(file: str,
            required: bool = False,
            envs_required: bool = False):
        container = Container()
        container.config.from_json(file, required, envs_required)
        return container

class Providable:
    def __init__(self,
            component: Component,
            provided_cls: type,
            provider_cls = providers.Singleton
        ):
        class Container(containers.DynamicContainer):
            config = providers.Configuration()
            service = provider_cls(provided_cls, config)
        self.component = component
        self.container = Container
    
    def populate_container(self, container: Container):
        setattr(container, self.component.base_cls.__name__, providers.Container(self.container, config=container.config))
        container.wire(modules=[self.component.inject_cls()])