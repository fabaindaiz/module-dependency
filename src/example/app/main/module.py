from dependency.core import Module, module
from example.plugins.base import BaseModule
from example.plugins.hardware import HardwareModule
from example.plugins.reporter import ReporterModule

@module(
    imports=[
        BaseModule,
        HardwareModule,
        ReporterModule,
    ],
)
class MainModule(Module):
    pass