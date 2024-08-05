from dependency_injector import containers, providers

class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    inject = providers.Callable(containers.DeclarativeContainer)