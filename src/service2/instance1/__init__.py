from src.service2 import Service2

class Service2Instance1(Service2):
    def __init__(self, cfg: dict):
        print(f"init2: {cfg}")

    def work(self):
        print("Service2 work")