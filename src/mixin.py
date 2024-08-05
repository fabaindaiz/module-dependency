class Mixin:
    @classmethod
    def _wire(cls, container):
        return container.wire(modules=[cls])