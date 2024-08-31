from src.services.singleton import SingletonService

class Type1SingletonService(SingletonService):
    def __init__(self, cfg: dict, **kwargs):
        super().__init__(**kwargs)
        print(f"Singleton Service init: {cfg}")

    def work(self):
        print("Singleton Service work")