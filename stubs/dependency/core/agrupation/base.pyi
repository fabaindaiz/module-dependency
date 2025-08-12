from abc import ABC

class ABCModule(ABC):
    name: str
    def __init__(self, name: str) -> None: ...
