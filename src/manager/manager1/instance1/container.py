from dependency_injector import providers
from src.manager.manager1.container import Manager1Container
from src.manager.manager1.instance1 import Manager1Instance1
from src.manager.manager1.mixin import Manager1Mixin

class Manager1Provider(Manager1Container):
    config = providers.Configuration()
    inject = providers.Callable(Manager1Mixin._wire)

    service = providers.Singleton(Manager1Instance1, config)