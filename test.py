from abc import ABC, abstractmethod
from test_dep import Container, populate_container
from test_dep import module, provider

@module()
class Module(ABC):
    @abstractmethod
    def work(self):
        pass

@provider(
    implements = Module
)
class EModule(Module):
    def __init__(self, cfg: dict):
        pass

    def work(self):
        print("working")

dependencies = [EModule]

container = Container()
container.config.from_json("config/main.json")
populate_container(container, dependencies)

print(type(Module))
Module.I().work()

def use(m: Module):
    m.work()

use(Module.I())
