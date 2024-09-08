from src.plugin.manager import Manager
from src.services.factory.container import FactoryServiceMixin
from src.services.singleton.container import SingletonServiceMixin

class Type1Manager(Manager, FactoryServiceMixin, SingletonServiceMixin):
    def __init__(self, cfg: dict, **kwargs):
        super().__init__(**kwargs)
        print(f"Manager init: {cfg}")

        print("Manager load")
    
    def work(self):
        print("Manager work")
        self.factory_service.work()
        self.factory_service.work()
        self.singleton_service.work()

    