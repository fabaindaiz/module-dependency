from typing import TypeVar

T = TypeVar('T')

class Decorator(T):
    def __init__(self, component: T) -> None:
        self._wrappee = component