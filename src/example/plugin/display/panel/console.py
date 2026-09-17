from dependency.core import instance, providers
from example.plugin.display import DisplayPlugin
from example.plugin.display.panel import StatusPanel


@instance(
    provider=providers.Singleton,
)
class ConsolePanel(StatusPanel):
    """Stands in for a physical screen."""
    def __init__(self) -> None:
        self.__width: int = DisplayPlugin.config.display.width

    def show(self, line: str) -> None:
        print(f"  [panel] {line[:self.__width]}")
