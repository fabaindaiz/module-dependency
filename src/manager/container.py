from dependency_injector import containers, providers

class ManagerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    inject = providers.Callable(containers.DeclarativeContainer)