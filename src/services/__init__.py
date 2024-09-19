from core import module
from services.factory import Factory
from services.singleton import Singleton

@module(
    declaration=[
        Factory,
        Singleton,
    ]
)
class Services:
    pass