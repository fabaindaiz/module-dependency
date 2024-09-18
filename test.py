from abc import ABC, abstractmethod
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide

def module():
    def wrap(cls):
        class Mixin():
            def __call__(self,
                    service = Provide[f"{cls.__name__}._provider"]) -> cls:
                return service
            
            @property
            def name(self) -> str:
                return cls.__name__
            
            @classmethod
            def wire(cls, container: containers.Container):
                return container.wire(modules=[cls])
        return Mixin()
    return wrap

def provider(
        implements,
        imports: list = [],
        provider = providers.Singleton
    ):
    def wrap(cls):
        class Container(containers.DeclarativeContainer):
            _name = providers.Object(implements.name)
            _wire = providers.Callable(implements.wire)
            _imports = providers.List(*imports)
            _config = providers.Configuration()
            _provider = provider(cls, _config)
        return Container
    return wrap

class Container(containers.DynamicContainer):
    config: providers.Configuration = providers.Configuration()

def populate_container(container: containers.Container, resolved_layer: list):
    for provided_cls in resolved_layer:
        setattr(container, provided_cls._name(), providers.Container(provided_cls, _config=container.config)) # type: ignore
        provided_cls._wire(container)

@module()
class Module(ABC):
    @abstractmethod
    def work(self):
        pass

@provider(
    implements = Module
)
class EModule:
    def __init__(self, cfg: dict):
        pass
    def work(self):
        print("working")

dependencies = [EModule]

container = Container()
container.config.from_json("config/main.json")
populate_container(container, dependencies)

Module().work()