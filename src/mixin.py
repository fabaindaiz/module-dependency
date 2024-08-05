class Mixin:
    def _wire(self, container):
        return container.wire(modules=[self.__class__])