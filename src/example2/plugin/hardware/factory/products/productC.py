from dependency.core import dependent
from dependency.core.declaration.dependent import Dependent
from example.plugin.hardware.factory.interfaces import Hardware

@dependent()
class HardwareC(Hardware, Dependent):
    def doStuff(self, operation: str) -> None:
        print(f"HardwareC works with operation: {operation}")