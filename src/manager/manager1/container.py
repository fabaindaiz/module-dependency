from dependency_injector import providers
from src.manager.container import ManagerContainer
from src.manager.manager1 import Manager1

class Manager1Container(ManagerContainer):
    service = providers.Singleton(Manager1)