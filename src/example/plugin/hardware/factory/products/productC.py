from example.plugin.hardware.factory.interfaces import Hardware

class HardwareC(Hardware):
    def doStuff(self, operation: str) -> None:
        print(f"HardwareC works with operation: {operation}")