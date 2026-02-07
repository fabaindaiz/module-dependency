from dependency.core import Component, component, providers
from example.plugin.hardware.interfaces import Hardware

@component(
    provider=providers.Factory,
)
class HardwareC(Hardware, Component):
    def doStuff(self, operation: str) -> None:
        print(f"HardwareC works with operation: {operation}")
