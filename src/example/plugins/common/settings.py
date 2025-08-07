from dependency.core.agrupation.plugin import PluginConfig
from pydantic import BaseModel

class General(BaseModel):
    debug: bool = False

class CommonPluginConfig(PluginConfig):
    general: General = General()