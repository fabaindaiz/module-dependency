from dependency.core.declaration import Module, module
from example.plugins.base.storage.cache import CacheServiceComponent

@module(
    declaration=[
        CacheServiceComponent,
    ],
)
class StorageModule(Module):
    def declare_providers(self) -> None:
        # Common providers for storage services
        from example.plugins.base.storage.cache.redis import RedisCacheService