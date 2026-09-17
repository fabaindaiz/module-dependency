from pydantic import BaseModel

class RuntimeSettings(BaseModel):
    """Settings the runtime plugin reads from the application config."""
    thread_pool_workers: int = 4

class RuntimeConfig(BaseModel):
    """A view onto the application config: this plugin only sees its own section.

    Pydantic ignores unknown keys, so every plugin validates the same root dictionary
    and picks out the part it owns. That keeps one config file without letting one
    plugin's settings leak into another's model.
    """
    runtime: RuntimeSettings = RuntimeSettings()
