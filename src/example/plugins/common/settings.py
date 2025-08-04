from dependency.core.declaration import PluginConfig
from pydantic import BaseModel

class General(BaseModel):
    debug: bool = False

class BasePluginConfig(PluginConfig):
    general: General = General()