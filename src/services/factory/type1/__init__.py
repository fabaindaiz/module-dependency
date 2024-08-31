from src.services.factory import FactoryService

class Type1FactoryService(FactoryService):
    def __init__(self, cfg: dict, **kwargs):
        super().__init__(**kwargs)
        print(f"Factory Service init: {cfg}")

    def work(self):
        print("Factory Service work")