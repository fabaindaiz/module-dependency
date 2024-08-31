import inspect
from abc import ABC, abstractmethod
from functools import wraps
from typing import Callable

class Injectable(ABC):
    """Required to inject factories in mixins"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._injected = False
    
    @abstractmethod
    def _make_injection(self):
        pass

def use_injection(func: Callable):
    """Use this decorator in all methods that require injection"""
    @wraps(func)
    def wrapper(self: Injectable, *args, **kwargs):
        if not self._injected:
            self._make_injection()
            self._injected = True
        return func(self, *args, **kwargs)
    return wrapper