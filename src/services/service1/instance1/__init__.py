from src.services.service1 import Service1
from src.services.service2.mixin import Service2Mixin, Service2

class Service1Instance1(Service1, Service2Mixin):
    def __init__(self, cfg: dict, **kwargs):
        print(f"init1: {cfg}")

    def work(self):
        print("Service1 work")