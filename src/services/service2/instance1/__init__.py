from src.services.service2 import Service2
from src.services.service1.container import Service1Mixin

class Service2Instance1(Service2, Service1Mixin):
    def __init__(self, cfg: dict):
        print(f"Service2 init: {cfg}")
        self.service1.work()

    def work(self):
        print("Service2 work")