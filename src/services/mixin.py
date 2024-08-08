from dependency_injector import containers

class Mixin:
    @classmethod
    def _wire(cls, container: containers.Container):
        return container.wire(modules=[cls])