from src.environment.default import AppEnvironment
from src.manager.manager1.mixin import Manager1Mixin

class AppLoader(AppEnvironment):
    pass

class Worker(Manager1Mixin):
    def work(self):
        self.manager1.do_work()

Worker().work()