from src.manager import Manager
from src.services.factory.container import FactoryServiceMixin
from src.services.singleton.container import SingletonServiceMixin

class Type1Manager(Manager, FactoryServiceMixin, SingletonServiceMixin):
    def __init__(self, cfg: dict, **kwargs):
        super().__init__(**kwargs)
        print(f"Manager init: {cfg}")
    
    def load(self):
        print("Manager load")
    
    def work(self):
        print("Manager work")
        self.factory_service.work()
        self.factory_service.work()
        self.singleton_service.work()

from core import provider

@provider(
    implements = Manager,
    imports = [
        FactoryService,
        SingletonService,
    ],
)
class Type1Manager(Manager):
    def __init__(self, cfg: dict, **kwargs):
        super().__init__(**kwargs)
        print(f"Manager init: {cfg}")

    def constructor(self,
        factory_service: FactoryService,
        singleton_service: SingletonService,
        ):
        pass