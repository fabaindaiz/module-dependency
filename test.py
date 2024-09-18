from dependency_injector import containers, providers

class Component:
    value = 6

def module(
        declaration: list[Component] = None,
        imports: list[Component] = None
    ):
    def wrap(cls):
        class Module:
            def __init__(self) -> None:
                self.imports = imports
                
            def wire(cls, container: containers.Container):
                return container.wire(modules=[cls])
        
        cls._injection = Module
        return cls
    return wrap

@module()
class Module:
    value: int = 5

def provider(
        provider: providers.Singleton,
        implements: Module,
        imports: list[Component]
    ):
    def wrap(cls):
        class Container(containers.DeclarativeContainer):
            _config = providers.Configuration()
            _imports = providers.List(*imports)
            _provider = provider(cls, _config)


        class Provider:
            def __init__(self) -> None:
                pass
        
        cls._injection = Module
        return cls
    return wrap


print(Module.value)