from abc import ABC, abstractmethod
from core import component
from plugin.client.type1 import Type1Client

@component(
    selector={
        "type1": Type1Client
    }
)
class Client(ABC):
    pass