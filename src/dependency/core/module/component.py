
from dependency_injector.wiring import Provide
from typing import Generic, TypeVar


T = TypeVar('T')
class Component(Generic[T]):
    _base_cls: type

    @classmethod
    def cls(cls):
        return cls

    def __repr__(self) -> str:
        return self._base_cls.__name__

def component(
    ):
    def wrap(cls: type[T]) -> Component[T]:
        class WrapComponent(Component, cls):
            _base_cls = cls

            @staticmethod
            def provided(
                    service: type[T] = Provide[f"{cls.__name__}.service"]
                ) -> type[T]:
                return service
        return WrapComponent
    return wrap