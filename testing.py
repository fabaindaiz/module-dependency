from abc import ABC, abstractmethod
from dependency_injector import providers
from typing import Callable, Self, TypeVar

MODULE = TypeVar('MODULE', bound='type[Providable]')

class Providable(ABC):
    @classmethod
    @abstractmethod
    def declarate(cls) -> None:
        pass

class FactoryProvidable(Providable):
    provider_cls: providers.Factory[Self] | None = None

    @classmethod
    def declarate(cls) -> None:
        cls.provider_cls = providers.Factory(cls)

    @classmethod
    def provider(cls) -> providers.Factory[Self]:
        if cls.provider_cls is None:
            raise RuntimeError(f'{cls.__name__} is not declarated')
        return cls.provider_cls

def module() -> Callable[[MODULE], MODULE]:
    def wrapper(c: MODULE) -> MODULE:
        return c
    return wrapper

def instance() -> Callable[[MODULE], MODULE]:
    def wrapper(c: MODULE) -> MODULE:
        c.declarate()
        return c
    return wrapper

@module()
class Module(FactoryProvidable, ABC):
    @abstractmethod
    def start(self) -> None:
        pass

@instance()
class ProviderModule(Module):
    def start(self) -> None:
        print('ProviderModule started')

test = Module.provider()()
