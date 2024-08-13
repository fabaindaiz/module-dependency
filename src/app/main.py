from src.manager.manager1.container import Manager1Mixin
from src.app import MainEnvironment

class MainApplication(MainEnvironment, Manager1Mixin):
    def __init__(self):
        # Here you can initialize the application
        self.manager1.load()

    def start(self):
        self.manager1.work()