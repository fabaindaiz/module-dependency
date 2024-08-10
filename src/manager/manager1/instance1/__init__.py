from src.manager.manager1 import Manager1
from src.services.service1.mixin import Service1Mixin
from src.services.service2.mixin import Service2Mixin

class Manager1Instance1(Manager1, Service1Mixin, Service2Mixin):
    def __init__(self, cfg: dict):
        print(f"man1: {cfg}")
        self.service1.work()
    
    def do_work(self):
        self.service1.work()
        self.service2.work()

    