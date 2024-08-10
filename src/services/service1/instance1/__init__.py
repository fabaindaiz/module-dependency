from src.services.service1 import Service1

class Service1Instance1(Service1):
    def __init__(self, cfg: dict, **kwargs):
        print(f"Service1 init: {cfg}")

    def work(self):
        print("Service1 work")