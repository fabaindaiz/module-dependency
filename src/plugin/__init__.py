from core import module
from plugin.client import Client
from plugin.manager import Manager

@module(
    declaration=[
        Client,
        Manager,
    ]
)
class Plugin:
    pass