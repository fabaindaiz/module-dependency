from dependency.core import module
from example.module.services.factory import FactoryMixin
from example.module.services.singleton import SingletonMixin
from example.module.services.factory.type1 import Type1Factory
from example.module.services.singleton.type1 import Type1Singleton

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