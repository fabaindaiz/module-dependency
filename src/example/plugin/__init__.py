from dependency.core import module
from example.plugin.client import Client
from example.plugin.manager import Manager
from example.plugin.client.type1 import Type1Client
from example.plugin.manager.type1 import Type1Manager

@module(
    declaration=[
        Client,
        Manager,
    ],
    providers=[
        Type1Client,
        Type1Manager,
    ]
)
class Plugin:
    pass