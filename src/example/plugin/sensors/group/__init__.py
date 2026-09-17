from abc import abstractmethod
from dependency.core import component
from dependency.library.components import CompositeComponent
from example.plugin.sensors import SensorsPlugin
from example.plugin.sensors.interfaces import Reading, SensorReader

@component(
    module=SensorsPlugin,
)
class SensorGroup(CompositeComponent[SensorReader]):
    """Every probe that came up, as one thing to read.

    Membership comes from the library contract; read_all is what this domain adds.
    """
    @abstractmethod
    def read_all(self) -> list[Reading]:
        """One measurement from every member, in registration order."""
