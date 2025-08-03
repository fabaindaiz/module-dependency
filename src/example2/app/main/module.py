from dependency.core import Module, module
from example2.plugin.base import BaseModule
from example2.plugin.hardware import HardwareModule
from example2.plugin.reporter import ReporterModule

@module(
    imports=[
        BaseModule,
        HardwareModule,
        ReporterModule,
    ],
)
class MainModule(Module):
    pass