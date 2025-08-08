from typing import cast
from dependency.core.agrupation.plugin import Plugin
from dependency.core.injection.base import ProviderInjection
from dependency.core.injection.container import Container
from dependency.core.injection.loader import InjectionLoader

class Entrypoint():
    def __init__(self, container: Container, plugins: list[type[Plugin]]) -> None:
        _plugins = cast(list[Plugin], plugins)
        for plugin in _plugins:
            plugin.set_container(container)
        providers: list[ProviderInjection] = [
            provider
            for plugin in _plugins
            for provider in plugin.injection.resolve_providers()]

        self.loader = InjectionLoader(
            container=container,
            providers=providers)
        self.loader.resolve_dependencies()