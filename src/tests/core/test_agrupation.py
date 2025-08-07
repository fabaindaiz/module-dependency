from dependency.core.agrupation.module import module
from dependency.core.agrupation.plugin import Plugin, PluginConfig, PluginMeta
from dependency.core.injection.container import Container

class TPluginConfig(PluginConfig):
    field1: str
    field2: int

@module()
class TPlugin(Plugin):
    meta = PluginMeta(name="test_plugin", version="0.1.0")

    @property
    def config(self) -> TPluginConfig:
        return TPluginConfig(**self.container.config())

def test_agrupation():
    container = Container.from_dict({
        "field1": "value",
        "field2": 100
    })
    TPlugin.set_container(container)
    config: TPluginConfig = TPlugin.config # type: ignore
    assert config.field1 == "value" and config.field2 == 100