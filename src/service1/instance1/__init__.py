from src.service1 import Service1

class Service1Instance1(Service1):
    def init(self, cfg: dict):
        print(f"serv1: {cfg}")

    def work(self):
        print("Service1 work")