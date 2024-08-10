from dependency_injector import containers, providers

class ServiceContainer(containers.DeclarativeContainer):
    name = providers.Object()
    depends = providers.List()
    config = providers.Configuration()
    inject = providers.Callable(containers.DeclarativeContainer)