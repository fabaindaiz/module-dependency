from abc import ABC, abstractmethod

class Mixin(ABC):
    @classmethod
    def _wire(cls, container):
        return container.wire(modules=[cls])