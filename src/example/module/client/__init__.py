from abc import ABC, abstractmethod
from dependency.core import Component, component

class Client(ABC):
    pass

@component(
    interface=Client
)
class ClientMixin(Component):
    pass