from dependency.core import Module, module
from example.module.client import ClientMixin
from example.module.manager import ManagerMixin
from example.module.client.type1 import Type1Client
from example.module.manager.type1 import Type1Manager
from example.module.services import Services

@module(
    declaration=[
        ClientMixin,
        ManagerMixin
    ],
    imports=[
        Services
    ],
    providers=[
        Type1Client,
        Type1Manager
    ],
    bootstrap=[
        ClientMixin
    ]
)
class Plugin(Module):
    pass