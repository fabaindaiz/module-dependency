# Which probes this build has. Removing a line here is how a unit ships without a
# sensor; it needs no change to any declaration.
import example.plugin.sensors.probes.temperature
import example.plugin.sensors.probes.humidity
import example.plugin.sensors.probes.pressure
import example.plugin.sensors.group.fitted
import example.plugin.sensors.sampler.periodic

from example.plugin.sensors import SensorsPlugin

__all__ = ["SensorsPlugin"]
