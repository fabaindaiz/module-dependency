from dependency_injector import providers
from dependency.core.module.base import Module, module
from dependency.core.module.provider import ProviderModule
from dependency.core.declaration.component import Component, component
from dependency.core.declaration.provider import Provider, provider
from dependency.core.declaration.dependent import Dependent, dependent

__all__ = [
    "providers",
    "Module",
    "module",
    "ProviderModule",
    "Component",
    "component",
    "Provider",
    "provider",
    "Dependent",
    "dependent",
]