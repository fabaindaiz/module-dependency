from src.environment.default import AppEnvironment
from src.services.service2.container import Service2Mixin
from src.manager.manager1.container import Manager1Mixin

class Worker(Service2Mixin, Manager1Mixin):
    def work(self):
        self.service2.work()
        self.manager1.work()

class AppLoader(AppEnvironment):
    Worker().work()