from dependency.core import module
from example.services.factory import Factory
from example.services.singleton import Singleton
from example.services.factory.type1 import Type1Factory
from example.services.singleton.type1 import Type1Singleton

@module(
    declaration=[
        Factory,
        Singleton,
    ],
    providers=[
        Type1Factory,
        Type1Singleton
    ]
)
class Services:
    pass