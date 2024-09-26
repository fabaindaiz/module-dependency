from dependency.core import module
from example.services.factory import FactoryMixin
from example.services.singleton import SingletonMixin
from example.services.factory.type1 import Type1Factory
from example.services.singleton.type1 import Type1Singleton

@module(
    declaration=[
        FactoryMixin,
        SingletonMixin,
    ],
    providers=[
        Type1Factory,
        Type1Singleton
    ]
)
class Services:
    pass