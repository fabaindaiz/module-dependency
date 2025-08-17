import pytest
from abc import ABC, abstractmethod
from dependency_injector import containers, providers
from dependency.core import Entrypoint
from dependency.core.declaration import Component, component, instance
from dependency.core.exceptions import DependencyError

from example.plugin.base import BasePlugin
from example.plugin.base.number import NumberService, NumberServiceComponent
from example.plugin.base.number.providers.fake import FakeNumberService

class ExampleApp(Entrypoint):
    def __init__(self) -> None:
        pass


def test_example():
    

    numberService: NumberService = NumberServiceComponent.provide()

    assert isinstance(numberService, NumberService)
    assert numberService.getRandomNumber() == 42