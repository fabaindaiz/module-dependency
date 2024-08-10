from src.manager.manager1 import Manager1
from src.services.service1.container import Service1Mixin
from src.services.service2.container import Service2Mixin

class Manager1Instance1(Manager1, Service1Mixin, Service2Mixin):
    def __init__(self, cfg: dict):
        print(f"Manager1 init: {cfg}")
        self.service1.work()
        self.service2.work()
    
    def work(self):
        print("Manager1 work")
        self.service1.work()
        self.service2.work()

    