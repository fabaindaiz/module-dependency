from dependency.core import Module, module
from example.plugin.base import BaseModule
from example.plugin.hardware import HardwareModule
from example.plugin.reporter import ReporterModule

@module(
    imports=[
        BaseModule,
        HardwareModule,
        ReporterModule,
    ],
)
class MainModule(Module):
    pass