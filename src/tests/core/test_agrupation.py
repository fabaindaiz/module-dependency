from pydantic import BaseModel
from dependency.core2.agrupation.module import module
from dependency.core2.agrupation.plugin import Plugin, PluginMeta
from dependency.core2.container import Container

class TPluginConfig(BaseModel):
    field1: str
    field2: int

@module()
class TPlugin(Plugin):
    meta = PluginMeta(name="test_plugin", version="0.1.0")
    config: TPluginConfig

def test_agrupation():
    container = Container.from_dict({
        "field1": "value",
        "field2": 100
    })
    TPlugin.resolve_providers(container) # type: ignore
    assert TPlugin.config.field1 == "value" and TPlugin.config.field2 == 100