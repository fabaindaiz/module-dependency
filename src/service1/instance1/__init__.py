from src.service1 import Service1

class Service1Instance1(Service1):
    def __init__(self, cfg: dict):
        print(f"init1: {cfg}")

    def init(self, cfg: dict):
        print(f"serv1: {cfg}")

    def work(self):
        print("Service1 work")