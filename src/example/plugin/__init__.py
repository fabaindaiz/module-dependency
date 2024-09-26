from dependency.core import module
from example.plugin.client import ClientMixin
from example.plugin.manager import ManagerMixin
from example.plugin.client.type1 import Type1Client
from example.plugin.manager.type1 import Type1Manager

@module(
    declaration=[
        ClientMixin,
        ManagerMixin,
    ],
    providers=[
        Type1Client,
        Type1Manager,
    ],
    bootstrap=[
        ClientMixin,
    ]
)
class Plugin:
    pass