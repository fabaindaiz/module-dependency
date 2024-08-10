from dependency_injector import containers, providers

class ServiceContainer(containers.DeclarativeContainer):
    depends = providers.List()
    config = providers.Configuration()
    inject = providers.Callable(containers.DeclarativeContainer)