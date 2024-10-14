from abc import ABC

class ABCComponent(ABC):
    def __init__(self, base_cls: type):
        self.base_cls = base_cls
    
    def __repr__(self) -> str:
        return self.base_cls.__name__

class ABCProvider(ABC):
    def __init__(self, provided_cls: type):
        self.provided_cls = provided_cls

    def __repr__(self) -> str:
        return self.provided_cls.__name__