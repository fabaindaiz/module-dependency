from collections import deque
from dependency.core.agrupation.module import Module
from dependency.core.injection.container import Container

class Entrypoint():
    def __init__(self, container: Container, modules: list[Module]) -> None:
        for module in modules:
            setattr(container, module.injection.name, module.injection.inject_cls())
            deque(module.injection.child_inject(container), maxlen=0)
            module.injection.child_wire(container)