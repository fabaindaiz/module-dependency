from abc import abstractmethod
from dependency.core import Component, component
from example.plugin.display import DisplayPlugin


@component(
    module=DisplayPlugin,
)
class StatusPanel(Component):
    """A screen on the front of the unit."""

    @abstractmethod
    def show(self, line: str) -> None:
        """Display one line of status."""
