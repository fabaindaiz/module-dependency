import src.environment.default
from src.manager.manager1.mixin import Manager1Mixin


class Worker(Manager1Mixin):
    pass

Worker().manager1.do_work()